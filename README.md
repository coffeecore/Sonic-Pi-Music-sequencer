# Sonic Pi Music sequencer OSC driven

## Intro

To limit if statment in Sonic Pi, you must control variables on your OSC app.

## OSC Commands

### General
|               |                  |                            |
| ------------- | ---------------- | ----------------------     |
| Play          | `/start`         |                            |
| Stop          | `/stop`          |                            |
| Pause         | `/pause`         |                            |
| Global volume | `/volume`        | Between `0` and `5`        |
| Eighth        | `/eighth`        | Number                     |
| Debug mode    | `/debug`         | `0` : disable `1` : enable |
| Sequencer mod | `/sequencer_mod` | `0` : step `1` : tracker   |
| Metronome     | `metronome`      | `0` : disable `1` : enable |

### Instruments (Synths and Samples)

| -------------- | ---------------- | ----------------------                 |
| Add instrument | `/instru/add`    | instruType, instruPosition, instruName |

`instruType` : `synth` if add synth or `sample` for sample
`instruPosition` : Number of instrument channel position. Will use it to add beats, FXs, options etc.
`instruName` : Name of synth or sample to use for this channel

| --------------    | ---------------- | ---------------------- |
| Remove instrument | `/instru/remove` | instruPosition         |

`instruPosition` : Number of instrument channel position to delete

| --------------    | ---------------- | ----------------------                 |
| Change instrument | `/instru/change` | instruType, instruPosition, instruName |

| --------------            | ----------------         | ----------------------                     |
| Change instrument options | `/instru/options/change` | instruPosition, optionName, optionValue... |

`optionName, optionValue...` : example : `[1, 'amp', 0.5, 'attack', 0.1]`

| --------------            | ----------------         | ----------------------        |
| Remove instrument options | `/instru/options/remove` | instruPosition, optionName... |

`optionName...` : example : [1, 'amp', 'attack']

| --------------                | ----------------             | ---------------------- |
| Remove all instrument options | `/instru/options/remove/all` | instruPosition         |

### Steps

| --------------                | ----------------             | ---------------------- |
| Add step | `/instru/step/add` | instruPosition, stepPosition, note        |

`stepPosition` : Position on your channel
`note` : Note synth plays. Send any value (except null) for sample

| --------------                | ----------------             | ---------------------- |
| Remove step | `/instru/step/remove` | instruPosition, stepPosition        |

### FXs

| --------------                | ----------------             | ---------------------- |
| Add FX | `/instru/fc/add` | instruPosition, fxPosition, fxName, fxOptionName, fxOptionValue...        |

`fxPosition` : FX position. High is last to play
`fxName` : FX name
`fxOptionName, fxOptionValue...` : FX options. Example `[3, 0, 'reverb', 'mix', 1, 'room', 1]`
