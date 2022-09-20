# AutoEQ (NekoAlosama's mod)
First name was "AutoEq-optimized".

Changed results are found [here.](./results)
If the upstream repo updates, I will commit the results of that repo into this one before generating and commiting my version.

Differences from source\*:
- Set `--max_gain`/`DEFAULT_MAX_GAIN` to `sys.float_info.max`.\*\*
- Used the default Harman target curve for adding bass instead of using `--bass_boost`.\*\*
- Increased decimal precision of some constants in `constants.py`.
- Increased decimal precision of generated results.

\*Crinacle results are the same as jaakkopasanen's because the source measurements are paywalled behind [Crinacle's Patreon.](https://www.patreon.com/crinacle)
\*\*Use an amplifier or adjust output values when neccessary because of `--max_gain`/`DEFAULT_MAX_GAIN` and bass changes.


## Example with Sennheiser HD 800
### Graph difference (for equalization differences)
| jaakkopasanen/AutoEq | NekoAlosama/AutoEQ-NekoMod |
| :------------------: | :------------------------: |
| ![jaakkopasanen/AutoEq](https://gitcdn.link/cdn/jaakkopasanen/AutoEq/master/results/oratory1990/harman_over-ear_2018/Sennheiser%20HD%20800/Sennheiser%20HD%20800.png) | ![NekoAlosama/AutoEQ-NekoMod](./results/oratory1990/harman_over-ear_2018/Sennheiser%20HD%20800/Sennheiser%20HD%20800.png) |

### Fixed Band EQ result difference (for equalization display)

| Type    | Fc       |    Q | Gain JP | Gain NA  |
|--------:|---------:|-----:|--------:|---------:|
| Preamp  |          |      | -6.4 dB | -9.11 dB |
| Peaking | 31 Hz    | 1.41 |  5.8 dB |  8.31 dB |
| Peaking | 62 Hz    | 1.41 |  2.6 dB |  3.89 dB |
| Peaking | 125 Hz   | 1.41 | -0.5 dB | -0.35 dB |
| Peaking | 250 Hz   | 1.41 | -1.8 dB | -1.99 dB |
| Peaking | 500 Hz   | 1.41 |  0.0 dB | -0.04 dB |
| Peaking | 1000 Hz  | 1.41 | -0.2 dB | -0.06 dB |
| Peaking | 2000 Hz  | 1.41 |  4.2 dB |  3.96 dB |
| Peaking | 4000 Hz  | 1.41 | -1.4 dB | -1.38 dB |
| Peaking | 8000 Hz  | 1.41 | -2.5 dB | -2.69 dB |
| Peaking | 16000 Hz | 1.41 | -7.3 dB | -7.52 dB |

## Original README.md
...is seen [here.](https://github.com/jaakkopasanen/AutoEq/blob/master/README.md)
