# -*- coding: utf-8 -*-

import os
import re
import shutil
import tempfile
import unittest
from glob import glob
import argparse
import multiprocessing
from pathlib import Path
import pandas as pd
import soundfile as sf
from time import time
import numpy as np
import tqdm
import yaml

from constants import DEFAULT_MAX_GAIN, DEFAULT_TREBLE_F_LOWER, DEFAULT_TREBLE_F_UPPER, \
    DEFAULT_TREBLE_GAIN_K, DEFAULT_FS, DEFAULT_BIT_DEPTH, DEFAULT_PHASE, DEFAULT_F_RES, DEFAULT_BASS_BOOST_GAIN, \
    DEFAULT_BASS_BOOST_FC, DEFAULT_BASS_BOOST_Q, DEFAULT_SMOOTHING_WINDOW_SIZE, \
    DEFAULT_TREBLE_SMOOTHING_WINDOW_SIZE, PEQ_CONFIGS
from frequency_response import FrequencyResponse


def batch_processing(input_dir=None, output_dir=None, new_only=False, standardize_input=False, compensation=None,
                     equalize=False, parametric_eq=False, fixed_band_eq=False, rockbox=False,
                     ten_band_eq=False, parametric_eq_config=None, fixed_band_eq_config=None, convolution_eq=False,
                     fs=DEFAULT_FS, bit_depth=DEFAULT_BIT_DEPTH, phase=DEFAULT_PHASE, f_res=DEFAULT_F_RES,
                     bass_boost_gain=DEFAULT_BASS_BOOST_GAIN, bass_boost_fc=DEFAULT_BASS_BOOST_FC,
                     bass_boost_q=DEFAULT_BASS_BOOST_Q, tilt=None, sound_signature=None, max_gain=DEFAULT_MAX_GAIN,
                     window_size=DEFAULT_SMOOTHING_WINDOW_SIZE, treble_window_size=DEFAULT_TREBLE_SMOOTHING_WINDOW_SIZE,
                     treble_f_lower=DEFAULT_TREBLE_F_LOWER, treble_f_upper=DEFAULT_TREBLE_F_UPPER,
                     treble_gain_k=DEFAULT_TREBLE_GAIN_K, show_plot=False, thread_count=1):
    """Parses files in input directory and produces equalization results in output directory."""
    if convolution_eq and not equalize:
        raise ValueError('equalize must be True when convolution_eq is True.')

    # Dir paths to absolute
    input_dir = os.path.abspath(input_dir)
    glob_files = glob(os.path.join(input_dir, '**', '*.csv'), recursive=True)
    if len(glob_files) == 0:
        raise FileNotFoundError(f'No CSV files found in "{input_dir}"')

    if compensation:
        # Creates FrequencyResponse for compensation data
        compensation_path = os.path.abspath(compensation)
        compensation = FrequencyResponse.read_from_csv(compensation_path)
        compensation.interpolate()
        compensation.center()

    if bit_depth == 16:
        bit_depth = "PCM_16"
    elif bit_depth == 24:
        bit_depth = "PCM_24"
    elif bit_depth == 32:
        bit_depth = "PCM_32"
    else:
        raise ValueError('Invalid bit depth. Accepted values are 16, 24 and 32.')

    if sound_signature is not None:
        sound_signature = FrequencyResponse.read_from_csv(sound_signature)
        if len(sound_signature.error) > 0:
            # Error data present, replace raw data with it
            sound_signature.raw = sound_signature.error
        sound_signature.interpolate()
        sound_signature.center()

    if parametric_eq_config is not None:
        if type(parametric_eq_config) is str and os.path.isfile(parametric_eq_config):
            # Parametric EQ config is a file path
            with open(parametric_eq_config) as fh:
                parametric_eq_config = yaml.safe_load(fh)
        else:
            if type(parametric_eq_config) is str:
                parametric_eq_config = [parametric_eq_config]
            parametric_eq_config = [
                PEQ_CONFIGS[config] if type(config) is str else config for config in parametric_eq_config]

    if fixed_band_eq_config is not None and os.path.isfile(fixed_band_eq_config):
        # Parametric EQ config is a file path
        with open(fixed_band_eq_config) as fh:
            fixed_band_eq_config = yaml.safe_load(fh)

    # Prepare list of arguments for all the function calls to generate results.
    n_total = 0
    file_paths = []
    args_list = []
    for input_file_path in glob_files:
        relative_path = os.path.relpath(input_file_path, input_dir)
        output_file_path = os.path.join(output_dir, relative_path) if output_dir else None
        output_file_dir = os.path.split(output_file_path)[0]
        if not new_only or not os.path.isdir(output_file_dir) or not len(os.listdir(output_file_dir)):
            # Not looking for only new ones or the output directory doesn't exist or it's empty
            file_paths.append((input_file_path, output_file_path))
            n_total += 1
            args = (input_file_path, output_file_path, bass_boost_fc, bass_boost_gain, bass_boost_q, bit_depth,
                    compensation, convolution_eq, equalize, f_res, fixed_band_eq, fs, parametric_eq_config,
                    fixed_band_eq_config, max_gain, window_size, treble_window_size,
                    parametric_eq, phase, rockbox, show_plot, sound_signature, standardize_input,
                    ten_band_eq, tilt, treble_f_lower, treble_f_upper, treble_gain_k)
            args_list.append(args)

    if not thread_count:
        thread_count = multiprocessing.cpu_count()

    with multiprocessing.Pool(thread_count) as pool:
        results = []
        for result in tqdm.tqdm(
                pool.imap_unordered(process_file_wrapper, args_list, chunksize=1), total=len(args_list)):
            results.append(result)
        return results


def process_file_wrapper(params):
    return process_file(*params)


def process_file(input_file_path, output_file_path, bass_boost_fc, bass_boost_gain, bass_boost_q, bit_depth,
                 compensation, convolution_eq, equalize, f_res, fixed_band_eq, fs, parametric_eq_config,
                 fixed_band_eq_config, max_gain, window_size, treble_window_size, parametric_eq, phase, rockbox,
                 show_plot, sound_signature, standardize_input, ten_band_eq, tilt, treble_f_lower, treble_f_upper,
                 treble_gain_k):
    start_time = time()
    # Read data from input file
    fr = FrequencyResponse.read_from_csv(input_file_path)

    if standardize_input:
        # Overwrite input data in standard sampling and bias
        fr.interpolate()
        fr.center()
        fr.write_to_csv(input_file_path)

    if ten_band_eq:
        fixed_band_eq = True

    # Process and equalize
    parametric_eq_peqs, fixed_band_eq_peq = fr.process(
        compensation=compensation,
        min_mean_error=True,
        equalize=equalize,
        parametric_eq=parametric_eq,
        fixed_band_eq=fixed_band_eq,
        ten_band_eq=ten_band_eq,
        parametric_eq_config=parametric_eq_config,
        fixed_band_eq_config=fixed_band_eq_config,
        bass_boost_gain=bass_boost_gain,
        bass_boost_fc=bass_boost_fc,
        bass_boost_q=bass_boost_q,
        tilt=tilt,
        sound_signature=sound_signature,
        max_gain=max_gain,
        window_size=window_size,
        treble_window_size=treble_window_size,
        treble_f_lower=treble_f_lower,
        treble_f_upper=treble_f_upper,
        treble_gain_k=treble_gain_k,
        fs=fs[0] if type(fs) == list else fs
    )

    if output_file_path is not None:
        # Copy relative path to output directory
        output_dir_path, _ = os.path.split(output_file_path)
        os.makedirs(output_dir_path, exist_ok=True)

        if equalize:
            # Write EqualizerAPO GraphicEq settings to file
            fr.write_eqapo_graphic_eq(output_file_path.replace('.csv', ' GraphicEQ.txt'), normalize=True)
            if parametric_eq:
                # Write ParametricEq settings to file
                fr.write_eqapo_parametric_eq(output_file_path.replace('.csv', ' ParametricEQ.txt'), parametric_eq_peqs)

            # Write fixed band eq
            if fixed_band_eq or ten_band_eq:
                # Write fixed band eq settings to file
                fr.write_eqapo_parametric_eq(output_file_path.replace('.csv', ' FixedBandEQ.txt'), fixed_band_eq_peq)

            # Write 10 band fixed band eq to Rockbox .cfg file
            if rockbox and ten_band_eq:
                # Write fixed band eq settings to file
                fr.write_rockbox_10_band_fixed_eq(
                    output_file_path.replace('.csv', ' RockboxEQ.cfg'),
                    fixed_band_eq_peq)

            # Write impulse response as WAV
            if convolution_eq:
                for _fs in fs:
                    if phase in ['linear', 'both']:
                        # Write linear phase impulse response
                        linear_phase_ir = fr.linear_phase_impulse_response(fs=_fs, f_res=f_res, normalize=True)
                        linear_phase_ir = np.tile(linear_phase_ir, (2, 1)).T
                        sf.write(
                            output_file_path.replace('.csv', f' linear phase {_fs}Hz.wav'),
                            linear_phase_ir,
                            _fs,
                            bit_depth
                        )
                    if phase in ['minimum', 'both']:
                        # Write minimum phase impulse response
                        minimum_phase_ir = fr.minimum_phase_impulse_response(fs=_fs, f_res=f_res, normalize=True)
                        minimum_phase_ir = np.tile(minimum_phase_ir, (2, 1)).T
                        sf.write(
                            output_file_path.replace('.csv', f' minimum phase {_fs}Hz.wav'),
                            minimum_phase_ir,
                            _fs,
                            bit_depth
                        )

        # Write results to CSV file
        fr.write_to_csv(output_file_path)

        # Write plots to file and optionally display them
        fr.plot_graph(
            show=show_plot,
            close=not show_plot,
            file_path=output_file_path.replace('.csv', '.png'),
        )

        # Write README.md
        fr.write_readme(
            os.path.join(output_dir_path, 'README.md'),
            parametric_eq_peqs=parametric_eq_peqs,
            fixed_band_eq_peq=fixed_band_eq_peq[0] if fixed_band_eq else None)

    elif show_plot:
        fr.plot_graph(show=True, close=False)

    return fr


def cli_args():
    """Parses command line arguments."""
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--input_dir', type=str, required=True,
                            help='Path to input data directory. Will look for CSV files in the data directory and '
                                 'recursively in sub-directories.')
    arg_parser.add_argument('--output_dir', type=str, default=argparse.SUPPRESS,
                            help='Path to results directory. Will keep the same relative paths for files found '
                                 'in input_dir.')
    arg_parser.add_argument('--standardize_input', action='store_true',
                            help='Overwrite input data in standardized sampling and bias?')
    arg_parser.add_argument('--new_only', action='store_true',
                            help='Only process input files which don\'t have results in output directory.')
    arg_parser.add_argument('--compensation', type=str,
                            help='File path to CSV containing compensation (target) curve. Compensation is '
                                 'necessary when equalizing because all input data is raw microphone data. See '
                                 '"compensation", "innerfidelity/resources" and "headphonecom/resources".')
    arg_parser.add_argument('--equalize', action='store_true',
                            help='Will run equalization if this parameter exists, no value needed.')
    arg_parser.add_argument('--parametric_eq', action='store_true',
                            help='Will produce parametric eq settings if this parameter exists, no value needed.')
    arg_parser.add_argument('--fixed_band_eq', action='store_true',
                            help='Will produce fixed band eq settings if this parameter exists, no value needed.')
    arg_parser.add_argument('--rockbox', action='store_true',
                            help='Will produce a Rockbox .cfg file with 10 band eq settings if this parameter exists,'
                                 'no value needed.')
    arg_parser.add_argument('--ten_band_eq', action='store_true',
                            help='Shortcut parameter for activating standard ten band eq optimization.')
    arg_parser.add_argument('--parametric_eq_config', type=str,
                            default='4_PEAKING_WITH_LOW_SHELF,4_PEAKING_WITH_HIGH_SHELF',
                            help='Name of parametric equalizer configuration or a path to a configuration file. '
                                 'Available named configurations are "10_PEAKING" for 10 peaking filters, '
                                 '"8_PEAKING_WITH_SHELVES" for 8 peaking filters and a low shelf at 105 Hz for bass '
                                 'adjustment and a high shelf at 10 kHz for treble adjustment, '
                                 '"4_PEAKING_WITH_LOW_SHELF" for 4 peaking filters and a low shelf at 105 Hz for bass '
                                 'adjustment, "4_PEAKING_WITH_HIGH_SHELF" for 4 peaking filters and a high shelf '
                                 'at 10 kHz for treble adjustments. You can give multiple named configurations by '
                                 'separating the names with commas and filter sets will be built on top of each other. '
                                 'When the value is a file path, the file will be read and used as a configuration. '
                                 'The file needs to be a YAML file with "filters" field as a list of filter '
                                 'configurations, each of which can define "fc", "min_fc", "max_fc", "q", "min_q", '
                                 '"max_q", "gain", "min_gain", "max_gain" and "type" fields. When the fc, q or gain '
                                 'value is given, the parameter won\'t be optimized for the filter. "type" needs to '
                                 'be either "LOW_SHELF", "PEAKING" or "HIGH_SHELF". Also "filter_defaults" field is '
                                 'supported on the top level and it can have the same fields as the filters do. '
                                 'All fields missing from the filters will be read from "filter_defaults". '
                                 'Defaults to "4_PEAKING_WITH_LOW_SHELF,4_PEAKING_WITH_HIGH_SHELF". '
                                 'Optimizer behavior can be adjusted by defining "optimizer" field which has fields '
                                 '"min_f" and "max_f" for lower and upper bounds of the optimization range, "max_time" '
                                 'for maximum optimization duration in seconds, "target_loss" for RMSE target level '
                                 'upon reaching which the optimization is ended, "min_change_rate" for minimum rate '
                                 'of improvement in db/s and "min_std" for minimum standard deviation of the last few '
                                 'loss values. "min_change_rate" and "min_std" end the optimization when further time '
                                 'spent optimizing can\'t be expected to improve the results dramatically. See '
                                 'peq.yaml for an example.'),
    arg_parser.add_argument('--fixed_band_eq_config', type=str, default='10_BAND_GRAPHIC_EQ',
                            help='Path to fixed band equalizer configuration. The file format is the same YAML as '
                                 'for parametric equalizer.')
    arg_parser.add_argument('--convolution_eq', action='store_true',
                            help='Will produce impulse response for convolution equalizers if this parameter exists, '
                                 'no value needed.')
    arg_parser.add_argument('--fs', type=str, default=str(DEFAULT_FS),
                            help='Sampling frequency in Hertz for impulse response and parametric eq filters. Single '
                                 'value or multiple values separated by commas eg 44100,48000. When multiple values '
                                 'are given only the first one will be used for parametric eq. '
                                 f'Defaults to {DEFAULT_FS}.')
    arg_parser.add_argument('--bit_depth', type=int, default=DEFAULT_BIT_DEPTH,
                            help='Number of bits for every sample in impulse response. '
                                 f'Defaults to {DEFAULT_BIT_DEPTH}.')
    arg_parser.add_argument('--phase', type=str, default=DEFAULT_PHASE,
                            help='Impulse response phase characteristic. "minimum", "linear" or "both". '
                                 f'Defaults to "{DEFAULT_PHASE}"')
    arg_parser.add_argument('--f_res', type=float, default=DEFAULT_F_RES,
                            help='Frequency resolution for impulse responses. If this is 20 then impulse response '
                                 'frequency domain will be sampled every 20 Hz. Filter length for '
                                 f'impulse responses will be fs/f_res. Defaults to {DEFAULT_F_RES}.')
    arg_parser.add_argument('--bass_boost', type=str, default=argparse.SUPPRESS,
                            help='Bass boost shelf. Sub-bass frequencies will be boosted by this amount. Can be '
                                 'either a single value for a gain in dB or a comma separated list of three values '
                                 'for parameters of a low shelf filter, where the first is gain in dB, second is '
                                 'center frequency (Fc) in Hz and the last is quality (Q). When only a single '
                                 'value (gain) is given, default values for Fc and Q are used which are '
                                 f'{DEFAULT_BASS_BOOST_FC} Hz and {DEFAULT_BASS_BOOST_Q}, '
                                 'respectively. For example "--bass_boost=6" or "--bass_boost=9.5,150,0.69".')
    arg_parser.add_argument('--iem_bass_boost', type=float, default=argparse.SUPPRESS,
                            help='iem_bass_boost argument has been removed, use "--bass_boost" instead!')
    arg_parser.add_argument('--tilt', type=float, default=argparse.SUPPRESS,
                            help='Target tilt in dB/octave. Positive value (upwards slope) will result in brighter '
                                 'frequency response and negative value (downwards slope) will result in darker '
                                 'frequency response. 1 dB/octave will produce nearly 10 dB difference in '
                                 'desired value between 20 Hz and 20 kHz. Tilt is applied with bass boost and both '
                                 'will affect the bass gain.')
    arg_parser.add_argument('--sound_signature', type=str,
                            help='File path to a sound signature CSV file. Sound signature is added to the '
                                 'compensation curve. Error data will be used as the sound signature target if '
                                 'the CSV file contains an error column and otherwise the raw column will be used. '
                                 'This means there are two different options for using sound signature: 1st is '
                                 'pointing it to a result CSV file of a previous run and the 2nd is to create a '
                                 'CSV file with just frequency and raw columns by hand (or other means). The Sound '
                                 'signature graph will be interpolated so any number of point at any frequencies '
                                 'will do, making it easy to create simple signatures with as little as two or '
                                 'three points.')
    arg_parser.add_argument('--max_gain', type=float, default=DEFAULT_MAX_GAIN,
                            help='Maximum positive gain in equalization. Higher max gain allows to equalize deeper '
                                 'dips in  frequency response but will limit output volume if no analog gain is '
                                 'available because positive gain requires negative digital preamp equal to '
                                 f'maximum positive gain. Defaults to {DEFAULT_MAX_GAIN}.')
    arg_parser.add_argument('--window_size', type=float, default=DEFAULT_SMOOTHING_WINDOW_SIZE,
                            help='Smoothing window size in octaves.')
    arg_parser.add_argument('--treble_window_size', type=float, default=DEFAULT_TREBLE_SMOOTHING_WINDOW_SIZE,
                            help='Smoothing window size in octaves in the treble region.')
    arg_parser.add_argument('--treble_f_lower', type=float, default=DEFAULT_TREBLE_F_LOWER,
                            help='Lower bound for transition region between normal and treble frequencies. Treble '
                                 'frequencies can have different max gain and gain K. Defaults to '
                                 f'{DEFAULT_TREBLE_F_LOWER}.')
    arg_parser.add_argument('--treble_f_upper', type=float, default=DEFAULT_TREBLE_F_UPPER,
                            help='Upper bound for transition region between normal and treble frequencies. Treble '
                                 'frequencies can have different max gain and gain K. Defaults to '
                                 f'{DEFAULT_TREBLE_F_UPPER}.')
    arg_parser.add_argument('--treble_gain_k', type=float, default=DEFAULT_TREBLE_GAIN_K,
                            help='Coefficient for treble gain, affects both positive and negative gain. Useful for '
                                 'disabling or reducing equalization power in treble region. Defaults to '
                                 f'{DEFAULT_TREBLE_GAIN_K}.')
    arg_parser.add_argument('--show_plot', action='store_true',
                            help='Plot will be shown if this parameter exists, no value needed.')
    arg_parser.add_argument('--thread_count', default=1,
                            help='Amount of threads to use for processing results. If set to "max" all the threads '
                                 'available will be used. Using more threads result in higher memory usage. '
                                 'Defaults to 1.')
    args = vars(arg_parser.parse_args())
    if 'iem_bass_boost' in args:
        raise TypeError('iem_bass_boost argument has been removed, use "--bass_boost" instead!')
    if 'bass_boost' in args:
        bass_boost = args['bass_boost'].split(',')
        if len(bass_boost) == 1:
            args['bass_boost_gain'] = float(bass_boost[0])
            args['bass_boost_fc'] = DEFAULT_BASS_BOOST_FC
            args['bass_boost_q'] = DEFAULT_BASS_BOOST_Q
        elif len(bass_boost) == 3:
            args['bass_boost_gain'] = float(bass_boost[0])
            args['bass_boost_fc'] = float(bass_boost[1])
            args['bass_boost_q'] = float(bass_boost[2])
        else:
            raise ValueError('"--bass_boost" must have one value or three values separated by commas!')
        del args['bass_boost']

    if 'parametric_eq_config' in args:
        if not os.path.isfile(args['parametric_eq_config']):
            # Named configurations, split by commas
            args['parametric_eq_config'] = args['parametric_eq_config'].split(',')

    if 'fs' in args and args['fs'] is not None:
        args['fs'] = [int(x) for x in args['fs'].split(',')]

    if thread_count := args.get('thread_count'):
        if thread_count == 'max':
            args['thread_count'] = multiprocessing.cpu_count()
        else:
            try:
                thread_count = int(thread_count)
            except ValueError:
                raise ValueError('"--thread_count" must have a value greater than 0 or equal to "max"!')
            if thread_count <= 0:
                raise ValueError('"--thread_count" must have a value greater than 0 or equal to "max"!')
            args['thread_count'] = thread_count
    return args


if __name__ == '__main__':
    batch_processing(**cli_args())


class TestAutoEq(unittest.TestCase):
    def setUp(self):
        self._root = Path(tempfile.gettempdir()).joinpath(os.urandom(24).hex())
        self._input = self._root.joinpath('input')
        self._output = self._root.joinpath('output')
        for i in range(1, 3):
            path = self._input.joinpath(f'Headphone {i}', f'Headphone {i}.csv')
            path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, 'w') as fh:
                fh.write('frequency,raw\n20,2\n50,2\n200,0\n1000,1\n3000,10\n10000,0\n20000,-15')
        self._compensation = self._root.joinpath('compensation.csv')
        with open(self._compensation, 'w') as fh:
            fr = FrequencyResponse(
                name='compensation',
                frequency=[20, 50, 200, 1000, 3000, 10000, 20000],
                raw=[6, 6, -1, 0, 8, 1, -10])
            fr.interpolate(pol_order=2)
            fr.smoothen_fractional_octave(window_size=2, treble_window_size=2)
            fr.center()
            fr.write_to_csv(self._compensation)
        self._sound_signature = self._root.joinpath('sound_signature.csv')
        with open(self._sound_signature, 'w') as fh:
            fh.write('frequency,raw\n20.0,0\n10000,0.0\n20000,3')

    def tearDown(self):
        shutil.rmtree(self._root)

    def test_batch_processing(self):
        self.assertTrue(self._input.joinpath('Headphone 1', 'Headphone 1.csv').exists())
        self.assertTrue(self._input.joinpath('Headphone 2', 'Headphone 2.csv').exists())
        frs = batch_processing(
            input_dir=self._input, output_dir=self._output, standardize_input=True, compensation=self._compensation,
            equalize=True, parametric_eq=True, fixed_band_eq=True, rockbox=True,
            ten_band_eq=True,
            parametric_eq_config=['4_PEAKING_WITH_LOW_SHELF', PEQ_CONFIGS['4_PEAKING_WITH_HIGH_SHELF']],
            fixed_band_eq_config=None, convolution_eq=True,
            fs=[44100, 48000], bit_depth=DEFAULT_BIT_DEPTH, phase='both', f_res=DEFAULT_F_RES,
            bass_boost_gain=DEFAULT_BASS_BOOST_GAIN, bass_boost_fc=DEFAULT_BASS_BOOST_FC,
            bass_boost_q=DEFAULT_BASS_BOOST_Q, tilt=-0.2, sound_signature=self._sound_signature,
            max_gain=DEFAULT_MAX_GAIN,
            window_size=DEFAULT_SMOOTHING_WINDOW_SIZE, treble_window_size=DEFAULT_TREBLE_SMOOTHING_WINDOW_SIZE,
            treble_f_lower=DEFAULT_TREBLE_F_LOWER, treble_f_upper=DEFAULT_TREBLE_F_UPPER,
            treble_gain_k=DEFAULT_TREBLE_GAIN_K, show_plot=False, thread_count=1
        )
        self.assertEqual(len(frs), 2)

        self.assertTrue(self._output.joinpath('Headphone 1', 'Headphone 1.png').exists())

        # CSV file
        self.assertTrue(self._output.joinpath('Headphone 1', 'Headphone 1.csv').exists())
        df = pd.read_csv(self._output.joinpath('Headphone 1', 'Headphone 1.csv'))
        columns = 'frequency,raw,error,smoothed,error_smoothed,equalization,parametric_eq,fixed_band_eq,' \
                  'equalized_raw,equalized_smoothed,target'.split(',')
        self.assertEqual(list(df.columns), columns)
        self.assertEqual(df.size, 695 * len(columns))

        # Graphic equalizer
        self.assertTrue(self._output.joinpath('Headphone 1', 'Headphone 1 GraphicEQ.txt').exists())
        with open(self._output.joinpath('Headphone 1', 'Headphone 1 GraphicEQ.txt')) as fh:
            self.assertRegexpMatches(fh.read().strip() + '; ', r'GraphicEQ: \d{2,5} (-?\d(\.\d+)?; )+')

        # Fixed band equalizer
        self.assertTrue(self._output.joinpath('Headphone 1', 'Headphone 1 FixedBandEq.txt').exists())
        with open(self._output.joinpath('Headphone 1', 'Headphone 1 FixedBandEq.txt')) as fh:
            lines = fh.read().strip().split('\n')
        self.assertTrue(re.match(r'Preamp: -?\d+(\.\d+)? dB', lines[0]))
        for line in lines[1:]:
            self.assertRegexpMatches(line, r'Filter \d{1,2}: ON PK Fc \d{2,5} Hz Gain -?\d(\.\d+)? dB Q 1.41')

        # Parametric equalizer
        self.assertTrue(self._output.joinpath('Headphone 1', 'Headphone 1 ParametricEq.txt').exists())
        with open(self._output.joinpath('Headphone 1', 'Headphone 1 ParametricEq.txt')) as fh:
            lines = fh.read().strip().split('\n')
        self.assertTrue(re.match(r'Preamp: -?\d+(\.\d+)? dB', lines[0]))
        for line in lines[1:]:
            self.assertRegexpMatches(
                line, r'Filter \d{1,2}: ON (PK|LS|HS) Fc \d{2,5} Hz Gain -?\d(\.\d+)? dB Q \d(\.\d+)?')

        # Convolution (FIR) filters
        for phase in ['minimum', 'linear']:
            for fs in [44100, 48000]:
                fp = self._output.joinpath('Headphone 1', f'Headphone 1 {phase} phase {fs}Hz.wav')
                self.assertTrue(fp.exists())
                # Frequency resolution is 10, 2 channels, 16 bits per sample, 8 bits per byte
                # Real file size has headers
                min_size = fs / 10 * 2 * 16 / 8
                self.assertGreater(os.stat(fp).st_size, min_size)

        # README
        self.assertTrue(self._output.joinpath('Headphone 1', 'README.md').exists())
        with open(self._output.joinpath('Headphone 1', 'README.md')) as fh:
            s = fh.read().strip()
        self.assertTrue('# Headphone 1' in s)
        self.assertTrue('### Parametric EQs' in s)
        self.assertTrue('### Fixed Band EQs' in s)
        self.assertTrue('### Graphs' in s)
