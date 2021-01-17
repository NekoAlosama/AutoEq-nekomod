# AutoEQ (NekoAlosama's mod)
First name was "AutoEq-optimized".


Changed results are found [here.](./results)
Default results for headphones in ['Problems caused'](#problems-caused) or ['Error-causing-headphones'](#error-causing-headphones) are found on the [source repo.](https://github.com/jaakkopasanen/AutoEq/tree/master/results)
If the source repo updates and it affects the results, I will commit the results of the source into this repo before generating and commiting my version.


Differences from souce:
- Recalculated most headphones with changes below.
  - Problems documented further below.
- Changed `--max_gain` from 6.0 to `NaN`.
  - This effectively disables the limit for positive gain values.
- Increased `--bass_boost` to slightly higher Harman target levels.
  - On-ear: 4.0 to 7.2.
  - In-ear: 6.0 to 10.8.
- Changed a few constants.
- Increased decimal precision of a few values.
- ~~GraphicEQ uses 127 samples from 20 to 20000.~~
  - Default uses 127 samples from 20 to 19871.
  - Removed for compatibility with Wavelet (since last checked).


Use an amplifier or adjust output values when neccessary, because of `--max_gain` and `--bass_boost` changes.


Crinacle results aren't changed because the source measurements are locked behind [Crinacle's Patreon.](https://www.patreon.com/crinacle)


## Problems caused
Default results for headphones in ['Problems caused'](#problems-caused) or ['Error-causing-headphones'](#error-causing-headphones) are found on the [source repo.](https://github.com/jaakkopasanen/AutoEq/tree/master/results)
Warnings, errors, and additional effects documented below. Errors usually caused by a very high output value.
Ordered by provider recommendation priority (oratory1990 > Crinacle > Innerfidelity > Rtings > Headphone.com > Reference Audio Analyzer). Asterisks (`*`) after any name means that they are listed as the recommended verison in [results/README.md](./results/README.md). 


- Beyerdynamic DT 48 S 5 Ohm (Innerfidelity on-ear)`*`
- Soul by Ludacris SL300 (Innerfidelity on-ear)`*`
- Comradz NW-STUDIO (Innerfidelity earbud)`*`
  - Missing Fixed Band EQ values, `nan dB` gains and `nandB` preamp.
  - Missing Fixed Band EQ line on graph.
- Jabra Elite Active 45e (Rtings in-ear)`*`
- Koss KDE250 (Headphone.com on-ear)`*`
- Pioneer HDJ-1000 (Headphone.com on-ear)
- Yuin PK1 (Headphone.com earbud)
- AKG K80 (Reference Audio Analyzer HDM-X on-ear)`*`
- Maxell Ear Bud (Reference Audio Analyzer SIEC in-ear)`*`
- Tansio Mirai TSMR-4 Pro (off-off-off) (Reference Audio Analyzer SIEC in-ear)`*`
  - Missing Fixed Band EQ values, `nan dB` gains and `nandB` preamp.
  - Missing Fixed Band EQ line on graph.
- Effects: None unless identified above.
```
C:\*\AutoEq-optimized\frequency_response.py:542: RuntimeWarning: invalid value encountered in greater
  if min_loss is None or min_loss - step_loss > threshold:
```


- Apple EarPods (oratory1990 earbud)`*`
- Koss KPH7 (Innerfidelity on-ear)`*`
- Edifier P180 (Innerfidelity earbud)`*`
- Apple EarPods (Headphone.com earbud)
  - Missing Fixed Band EQ values, `nan dB` gains and `nandB` preamp.
  - Missing Fixed Band EQ line on graph.
- Effects: None unless identified above.
```
C:\*\AutoEq-optimized\frequency_response.py:542: RuntimeWarning: invalid value encountered in greater
  if min_loss is None or min_loss - step_loss > threshold:
C:\*\AutoEq-optimized\frequency_response.py:542: RuntimeWarning: invalid value encountered in greater
  if min_loss is None or min_loss - step_loss > threshold:
```


- Beats Studio (Innerfidelity on-ear)`*`
- Venture Electronics Monk Plus (Innerfidelity earbud)`*`
  - Missing Fixed Band EQ value, `nandB` preamp.
  - Broken Fixed Band EQ line on graph.
- Effects: None unless identified above.
```
C:\*\AutoEq-optimized\frequency_response.py:542: RuntimeWarning: invalid value encountered in greater
  if min_loss is None or min_loss - step_loss > threshold:
C:\*\AutoEq-optimized\biquad.py:129: RuntimeWarning: invalid value encountered in log10
  (a0 + a1 + a2) ** 2 + (a0 * a2 * phi - (a1 * (a0 + a2) + 4 * a0 * a2)) * phi
```


- Stax SR-40 Electret SR4 Adapter (Innerfidelity on-ear)`*`
- Effects:
  - Missing Fixed Band EQ value, `nandB` preamp.
  - Broken Fixed Band EQ line on graph.
```
C:\*\AutoEq-optimized\frequency_response.py:542: RuntimeWarning: invalid value encountered in greater
  if min_loss is None or min_loss - step_loss > threshold:
C:\*\AutoEq-optimized\frequency_response.py:542: RuntimeWarning: invalid value encountered in greater
  if min_loss is None or min_loss - step_loss > threshold:
C:\*\AutoEq-optimized\biquad.py:129: RuntimeWarning: invalid value encountered in log10
  (a0 + a1 + a2) ** 2 + (a0 * a2 * phi - (a1 * (a0 + a2) + 4 * a0 * a2)) * phi
```


- Sony XEA20 Xperia Ear Duo (oratory1990 earbud)`*`
- Howard Leight Sync (Innerfidelity on-ear)`*`
- Walmart Three DOllar Buds (Innerfidelity earbud)`*`
- Yuin PK2 (Innerfidelity earbud)`*`
- AfterShokz Aeropex (Rtings earbud)`*`
  - Missing Fixed Band EQ values, `nan dB` gains and `nandB` preamp.
  - Missing Fixed Band EQ line on graph.
- AfterShokz Trekz Air (Rtings earbud)`*`
  - Missing Fixed Band EQ values, `nan dB` gains and `nandB` preamp.
  - Missing Fixed Band EQ line on graph.
- Bose SoundWear (Rtings earbud)`*`
  - Missing Fixed Band EQ values, `nan dB` gains and `nandB` preamp.
  - Missing Fixed Band EQ line on graph.
- AKG K120 (Reference Audio Analyzer HDM1 on-ear)`*`
- Audio-Technica ATH-SJ1 (Reference Audio Analyzer HDM1 on-ear)`*`
- Beyerdynamic DT 48 E 200 Ohm (Reference Audio Analyzer HDM1 on-ear)`*`
- Beyerdynamic DTX 300p (Reference Audio Analyzer HDM1 on-ear)
- 64 Audio U4 (vent open) (Reference Audio Analyzer SIEC in-ear)`*`
  - Missing Fixed Band EQ values, `nan dB` gains and `nandB` preamp.
  - Missing Fixed Band EQ line on graph.
- Effects:
  - Missing Parametric EQ values, no filters and `-0.60` preamp.
  - Parametric EQ line on graph is flat.
```
C:\*\AutoEq-optimized\frequency_response.py:542: RuntimeWarning: invalid value encountered in greater
  if min_loss is None or min_loss - step_loss > threshold:
C:\*\AutoEq-optimized\frequency_response.py:566: RuntimeWarning: invalid value encountered in greater
  sl = np.logical_and(np.abs(_gain) > 0.1, _fc > 10)
C:\*\AutoEq-optimized\frequency_response.py:542: RuntimeWarning: invalid value encountered in greater
  if min_loss is None or min_loss - step_loss > threshold:
C:\*\AutoEq-optimized\frequency_response.py:566: RuntimeWarning: invalid value encountered in greater
  sl = np.logical_and(np.abs(_gain) > 0.1, _fc > 10)
C:\*\AutoEq-optimized\frequency_response.py:542: RuntimeWarning: invalid value encountered in greater
  if min_loss is None or min_loss - step_loss > threshold:
```


- Sennheiser MX 560 (Innerfidelity earbud)`*`
- Sennheiser MX 680 (Innerfidelity earbud)`*`
- Google Pixel Buds (Rtings earbud)`*`
- Sennheiser MX 560 (Headphone.com earbud)
- Yuin PK2 (Headphone.com earbud)
- Audio-Technica ATH-ES3 (Reference Audio Analyzer HDM1 on-ear)`*`
- Final Audio MURAMASA VIII (Reference Audio Analyzer HDM1 on-ear)`*`
- Effects:
  - Missing Fixed Band EQ value, `nandB` preamp.
  - Broken Fixed Band EQ line on graph.
  - Missing Parametric EQ values, no filters and `-0.60` preamp.
  - Parametric EQ line on graph is flat.
```
C:\*\AutoEq-optimized\frequency_response.py:542: RuntimeWarning: invalid value encountered in greater
  if min_loss is None or min_loss - step_loss > threshold:
C:\*\AutoEq-optimized\frequency_response.py:566: RuntimeWarning: invalid value encountered in greater
  sl = np.logical_and(np.abs(_gain) > 0.1, _fc > 10)
C:\*\AutoEq-optimized\frequency_response.py:542: RuntimeWarning: invalid value encountered in greater
  if min_loss is None or min_loss - step_loss > threshold:
C:\*\AutoEq-optimized\frequency_response.py:566: RuntimeWarning: invalid value encountered in greater
  sl = np.logical_and(np.abs(_gain) > 0.1, _fc > 10)
C:\*\AutoEq-optimized\frequency_response.py:542: RuntimeWarning: invalid value encountered in greater
  if min_loss is None or min_loss - step_loss > threshold:
C:\*\AutoEq-optimized\biquad.py:129: RuntimeWarning: invalid value encountered in log10
  (a0 + a1 + a2) ** 2 + (a0 * a2 * phi - (a1 * (a0 + a2) + 4 * a0 * a2)) * phi
```


### Error-causing headphones 
Default results for headphones in ['Problems caused'](#problems-caused) or ['Error-causing-headphones'](#error-causing-headphones) are found on the [source repo.](https://github.com/jaakkopasanen/AutoEq/tree/master/results)
These headphones are placed in ['bad headphones' folder.](./measurements/bad%20headphones)
- Beats Studio (Innerfidelity On-ear)
- Koss KPH7 (Innerfidelity On-ear)
- Stax SR-3 (Innerfidelity On-ear)
- Soul by Ludacris SL300 (Innerfidelity On-ear)
- Stax SR-40 Electret SR4 Adapter (Innerfidelity On-ear)
- Apple iPod Ear Buds (sample B) (Innerfidelity Earbud)
- Yuin PK2 (Innerfidelity Earbud)
- Jabra Elite Active 45e (Rtings In-ear)
- AfterShokz Trekz Air (Rtings Earbud)
- Beats by Dr (Headphone.com On-ear)
- Sennheiser HD R 130 (Headphone.com On-ear)
- Sennheiser RS 130 (Headphone.com On-ear)
- Sony MDR-7502 (Headphone.com On-ear)
- JVC HA-SR500 (Reference Audio Analyzer HDM1 On-ear)
- Stax SR-303 (Reference Audio Analyzer HDM1 On-ear)
- Effects: No output for these headphones.
```
C:\*\AutoEq-optimized\frequency_response.py:542: RuntimeWarning: invalid value encountered in greater
  if min_loss is None or min_loss - step_loss > threshold:
C:\*\AutoEq-optimized\biquad.py:129: RuntimeWarning: invalid value encountered in log10
  (a0 + a1 + a2) ** 2 + (a0 * a2 * phi - (a1 * (a0 + a2) + 4 * a0 * a2)) * phi
Traceback (most recent call last):
  File "results\update_results.py", line 246, in <module>
    main()
  File "results\update_results.py", line *, in main // * = Line for kwargs
    **eq_kwargs // kwargs dependent from headphone type
  File "C:\*\AutoEq-optimized\autoeq.py", line 100, in batch_processing
    fs=fs[0] if type(fs) == list else fs
  File "C:\*\AutoEq-optimized\frequency_response.py", line 1649, in process
    peq_filters, n_peq_filters, peq_max_gains = self.optimize_parametric_eq(max_filters=max_filters, fs=fs)
  File "C:\*\AutoEq-optimized\frequency_response.py", line 627, in optimize_parametric_eq
    fs=fs
  File "C:\*\AutoEq-optimized\frequency_response.py", line 298, in optimize_biquad_filters
    fr_target.smoothen_fractional_octave(window_size=1 / 7, iterations=1000)
  File "C:\*\AutoEq-optimized\frequency_response.py", line 1190, in smoothen_fractional_octave
    treble_f_upper=treble_f_upper
  File "C:\*\AutoEq-optimized\frequency_response.py", line 1139, in _smoothen_fractional_octave
    raise ValueError('None values present, cannot smoothen!')
ValueError: None values present, cannot smoothen!
```


## Original README.md
...is seen [here.](https://github.com/jaakkopasanen/AutoEq/blob/master/README.md)
