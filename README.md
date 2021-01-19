# AutoEQ (NekoAlosama's mod)
First name was "AutoEq-optimized".

Changed results are found [here.](./results)
Default results for headphones in ['Problems caused'](#problems-caused) or ['Error-causing-headphones'](#error-causing-headphones) are found on the [source repo.](https://github.com/jaakkopasanen/AutoEq/tree/master/results)
If the source repo updates and it affects the results, I will commit the results of the source into this repo before generating and commiting my version.

Differences from souce:
- Recalculated most headphones with changes below.
  - Problems documented further below.
- Changed `--max_gain` from 6.0 to `sys.float_info.max`.
  - This effectively disables the limit for positive gain values.
  - `float('NaN')` doesn't work for the current limited slope equalization.
- Used the default Harman target curve for adding bass instead of using `--bass_boost`.
- Changed a few constants.
- Increased the decimal precision of a few values, at most to 2 decimal places.
- ~~GraphicEQ uses 127 samples from 20 to 20000.~~
  - Default uses 127 samples from 20 to 19871.
  - Removed for compatibility with Wavelet (since last checked).

Use an amplifier or adjust output values when neccessary because of `--max_gain` and bass changes.

Crinacle results aren't changed because the source measurements are paywalled behind [Crinacle's Patreon.](https://www.patreon.com/crinacle)

## Example with Sennheiser HD 800
### Graph difference (for equalization differences)
| jaakkopasanen/AutoEq | NekoAlosama/AutoEQ-NekoMod |
| -------------------: | :------------------------- |
| ![jaakkopasanen/AutoEq](https://gitcdn.xyz/repo/jaakkopasanen/AutoEq/master/results/oratory1990/harman_over-ear_2018/Sennheiser%20HD%20800/Sennheiser%20HD%20800.png) | ![NekoAlosama/AutoEQ-NekoMod](https://gitcdn.xyz/repo/NekoAlosama/AutoEQ-NekoMod/master/results/oratory1990/harman_over-ear_2018/Sennheiser%20HD%20800/Sennheiser%20HD%20800.png) |

### Fixed Band EQ result difference (for equalization display)

| Type    | Fc       |    Q | Gain JP | Gain NA  |
|:--------|:---------|:-----|--------:|---------:|
| Preamp  |          |      | -5.8 dB | -8.01 dB |
| Peaking | 31 Hz    | 1.41 | 5.2 dB  | 7.38 dB  |
| Peaking | 62 Hz    | 1.41 | 2.0 dB  | 3.33 dB  |
| Peaking | 125 Hz   | 1.41 | -0.9 dB | -0.60 dB |
| Peaking | 250 Hz   | 1.41 | -2.2 dB | -2.40 dB |
| Peaking | 500 Hz   | 1.41 | -0.3 dB | -0.38 dB |
| Peaking | 1000 Hz  | 1.41 | -0.2 dB | -0.23 dB |
| Peaking | 2000 Hz  | 1.41 | 5.1 dB  | 5.05 dB  |
| Peaking | 4000 Hz  | 1.41 | -1.6 dB | -1.67 dB |
| Peaking | 8000 Hz  | 1.41 | -1.7 dB | -1.80 dB |
| Peaking | 16000 Hz | 1.41 | -5.7 dB | -5.84 dB |

## Problems caused
Default results for headphones in ['Problems caused'](#problems-caused) or ['Error-causing-headphones'](#error-causing-headphones) are found on the [source repo.](https://github.com/jaakkopasanen/AutoEq/tree/master/results)
Warnings, errors, and additional effects documented below. Errors usually caused by a very high output value.
Ordered by provider recommendation priority (oratory1990 > Crinacle > Innerfidelity > Rtings > Headphone.com > Reference Audio Analyzer).

- Jabra Elite Active 45e (rtings\inear)
- AfterShokz Aeropex (rtings\earbud)
- Sony MDR-7502 (headphonecom\onear)
- Apple EarPods (headphonecom\earbud)
  - `.csv` contains only zeros in the `parametric_eq` category.
  - No Parametric EQ due to above.
- AKG K120 (referenceaudioanalyzer\onear\HDM1)
  - `.csv` contains only zeros in the `parametric_eq` category.
  - No Parametric EQ due to above.
- Beyerdynamic DT 48 E 200 Ohm (referenceaudioanalyzer\onear\HDM1)
- Effects:
  - `.csv` contains empty boxes in the `fixed_band_eq` category, only around the 31.25Hz band.
  - `.png` has the 'Fixed Band EQ' line broken due to above.
  
```
[repo]\biquad.py:128: RuntimeWarning: invalid value encountered in log10
  ) - 10 * np.log10(
```

### Error-causing headphones 
Default results for headphones in ['Problems caused'](#problems-caused) or ['Error-causing-headphones'](#error-causing-headphones) are found on the [source repo.](https://github.com/jaakkopasanen/AutoEq/tree/master/results)
These headphones are placed in ['error_causers' folder.](./measurements/error_causers)

- Koss KPH7 (error_causers\innerfidelity\onear)
- Stax SR-3 (error_causers\innerfidelity\onear)
- Apple iPod Ear Buds (sample A) (error_causers\innerfidelity\earbud)
- Yuin PK2 (error_causers\innerfidelity\earbud)
- AfterShokz Trekz Air (error_causers\rtings\earbud)
- Sennheiser HD R 130 (error_causers\headphonecom\onear)
- Sennheiser RS 130 (error_causers\headphonecom\onear)
- JVC HA-SR500 (error_causers\referenceaudioanalyzer\onear\HDM1)
- Effects: No output for these headphones.

```
[repo]\biquad.py:128: RuntimeWarning: invalid value encountered in log10
  ) - 10 * np.log10(
Traceback (most recent call last):
  File "results\update_results.py", line 253, in <module>
    main()
  File "results\update_results.py", line 76, in main
    batch_processing(
  File "[repo]\autoeq.py", line 83, in batch_processing
    peq_filters, n_peq_filters, peq_max_gains, fbeq_filters, n_fbeq_filters, fbeq_max_gain = fr.process(
  File "[repo]\frequency_response.py", line 1888, in process
    peq_filters, n_peq_filters, peq_max_gains = self.optimize_parametric_eq(max_filters=max_filters, fs=fs)
  File "[repo]\frequency_response.py", line 626, in optimize_parametric_eq
    _eq, rmse, _fc, _Q, _gain, _coeffs_a, _coeffs_b = self.optimize_biquad_filters(
  File "[repo]\frequency_response.py", line 301, in optimize_biquad_filters
    fr_target.smoothen_fractional_octave(window_size=1 / 7, iterations=1000)
  File "[repo]\frequency_response.py", line 1214, in smoothen_fractional_octave
    self.smoothed = self._smoothen_fractional_octave(
  File "[repo]\frequency_response.py", line 1170, in _smoothen_fractional_octave
    raise ValueError('None values present, cannot smoothen!')
ValueError: None values present, cannot smoothen!
```

## Original README.md
...is seen [here.](https://github.com/jaakkopasanen/AutoEq/blob/master/README.md)
