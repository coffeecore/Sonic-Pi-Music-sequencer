# Sonic Pi Music sequencer OSC driven

## :musical_keyboard: Intro

Goal is to build a music box with Raspberry Pi, E-Ink screen, somes buttons and potars.

For now, it's the Sonic Pi part.

:rocket: by [Sonic Pi](https://sonic-pi.net/ "Sonic Pi - The Live Coding Music Synth for Everyone").

## How to

Just type `run_file "/absolute/path/to/seq.rb"` in Sonic Pi editor

To run Python script, install [python-osc](https://pypi.org/project/python-osc/ "python-osc · PyPI").

:heavy_exclamation_mark: To limit if statment in Sonic Pi, you must control variables on your OSC app.

## OSC Commands

### General

General command of sequencer

| Feature |   OSC URI     | Parameters  |
| ------------- | ---------------- | ----------------------     |
| Play          | `/start`         |                            |
| Stop          | `/stop`          |                            |
| Pause         | `/pause`         |                            |
| Global volume | `/volume`        | Between `0` and `5` (default)        |
| Eighth        | `/eighth`        | Number (default : 4)                  |
| Debug mode    | `/debug`         | `0` : disable (default) `1` : enable |
| Sequencer mod | `/sequencer_mod` | `0` : step (default) `1` : tracker   |
| Metronome     | `/metronome`      | `0` : disable `1` : enable (default) |
| Set BPM     | `/bpm`      | Number (default : 60) |

:heavy_exclamation_mark: Sequencer mod : `tracker` mod is work in progress

### Instruments (Synths and Samples)

Manage instruments, can be synth or sample.

| Feature |   OSC URI     | Parameters  |
| -------------- | ---------------- | ----------------------                 |
| Add instrument | `/instru/add`    | instruType, instruName |

`instruType` :
 - `synth`
 - `sample`
 - `external_sample`

`instruName` : Name of synth, sample or path to sample to use for this channel

| Feature |   OSC URI     | Parameters  |
| --------------    | ---------------- | ---------------------- |
| Remove instrument | `/instru/remove` | instruPosition         |
| Change instrument | `/instru/change` | instruType, instruPosition, instruName |
| Change instrument options | `/instru/options/change` | instruPosition, optionName, optionValue... |

`instruPosition` : Channel position. Will use it to add beats, FXs, options etc. `-1` to change or delete at (see below) last position

`optionName, optionValue...` : example : `[1, 'amp', 0.5, 'attack', 0.1]`

| Feature |   OSC URI     | Parameters  |
| --------------            | ----------------         | ----------------------        |
| Remove instrument options | `/instru/options/remove` | instruPosition, optionName... |

`optionName...` : example : `[1, 'amp', 'attack']`

| Feature |   OSC URI     | Parameters  |
| --------------                | ----------------             | ---------------------- |
| Remove all instrument options | `/instru/options/remove/all` | instruPosition         |

### Steps

Add step

| Feature |   OSC URI     | Parameters  |
| --------------                | ----------------             | ---------------------- |
| Add step | `/instru/step/add` | instruPosition, stepPosition, note        |

`stepPosition` : Position on your channel

`note` : Note synth plays. Send any value (except null) for sample

| Feature |   OSC URI     | Parameters  |
| --------------                | ----------------             | ---------------------- |
| Remove step | `/instru/step/remove` | instruPosition, stepPosition        |

### FXs

Add Sonic Pi Fxs

| Feature |   OSC URI     | Parameters  |
| --------------                | ----------------             | ---------------------- |
| Add FX | `/instru/fx/add` | instruPosition, fxName, fxOptionName, fxOptionValue...        |

`fxName` : FX name

`fxOptionName, fxOptionValue...` : FX options. Example `[3, 0, 'reverb', 'mix', 1, 'room', 1]`

| Feature |   OSC URI     | Parameters  |
| --------------                | ----------------             | ---------------------- |
| Change FX options | `/instru/fx/change` | instruPosition, fxPosition, fxOptionName, fxOptionValue...        |
| Remove FX | `/instru/fx/remove` | instruPosition, fxPosition...        |
| Remove all FXs | `/instru/fx/remove/all` | instruPosition      |

`fxPosition` : FX position. `-1` to change or delete at last position.

