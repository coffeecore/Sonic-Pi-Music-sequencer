# :musical_keyboard: Sonic Pi Music step sequencer OSC driven

## Intro

Goal is to build a music box with Raspberry Pi, E-ink screen, somes buttons and potards.

For now, it's the Sonic Pi part. To manage buttons etc. python will be used.

:rocket: Powered by [Sonic Pi](https://sonic-pi.net/ "Sonic Pi - The Live Coding Music Synth for Everyone").

## Planned components

 - Raspberry Pi
 - Piano HAT
 - E-ink 2.13" screen
 - 6 potards
 - 6-8 buttons
 - 4 leds
 - Maybe battery

## What can it do ?

- Add sample or synth (I must try the limit)
- Sample/synth options
- FXs
- Change some parameters (BPM for example)
- Metronome
- Step sequencer
- Can play one pattern in loop or loop on many patterns

## How to

Open `seq.rb` file and change value of `FILE_PATH` constant.

Just type `run_file "/absolute/path/to/seq.rb"` or open `seq.rb` file in Sonic Pi editor.

To run Python script, install [python-osc](https://pypi.org/project/python-osc/ "python-osc · PyPI").

## Limitations

:heavy_exclamation_mark: To limit if statment in Sonic Pi, you must control variables on your OSC app to avoid errors

:heavy_exclamation_mark: Don't forget to add `time.sleep(float)` between OSC message in Python script. To investigate

:heavy_exclamation_mark: Limit use of FXs

## Todo

- Test real performances :sweat_smile:
- OSC return messages
- Python part
- Arrange patterns system

## OSC Commands

- [General](#general)
- [Instruments (Synths and Samples)](#instruments-synths-and-samples)
- [Steps](#steps)
- [FXs](#fxs)

### General

| Feature                                  | OSC URI              | Parameters                           |
| ---------------------------------------- | -------------------- | ------------------------------------ |
| Play                                     | `/start`             | 1                                    |
| Stop                                     | `/stop`              | 1                                    |
| Pause                                    | `/pause`             | 1                                    |
| Global volume                            | `/volume`            | Between `0` and `5` (default)        |
| Eighth                                   | `/eighth`            | Integer (default : 4)                |
| Bar                                      | `/bar`               | Integer (default : 4)                |
| Debug mode                               | `/debug`             | `0` : disable (default) `1` : enable |
| Sequencer mod                            | `/sequencer_mod`     | `0` : bank `1` : single    |
| Metronome                                | `/metronome`         | `0` : disable `1` : enable (default) |
| Set metronome note options               | `/metronome/options` | optionName, optionValue...           |
| Set BPM                                  | `/bpm`               | Integer (default : 60)               |
| Set pattern to play on `single` mod      | `/pattern`           | Integer (default : 0)                |
| Set total patterns to play on `step` mod | `/pattern/max`       | Integer (default : 1)                |
| Reset all Time State var                 | `/reset`             | 1                                    |

`/sequencer_mod` _Features in progress_ :
 - sequencer : play all patterns from single mod position to `/pattern/max` setting and loop from 0
 - single : loop on pattern at this position

### Instruments (Synths and Samples)

| Feature                                       | OSC URI                   | Parameters                                                                      |
| --------------------------------------------- | ----------------- | ---------------------- |
| Add instrument with options, steps and FXs    | `/instru/add/complete`    | See Python script for example. Format must be JSON and complete to avoid errors |
| Change instrument with options, steps and FXs | `/instru/change/complete` | JSON, instruPosition                                                            |
| Remove instrument                             | `/instru/remove`          | instruPosition                                                                  |
| Change instrument                             | `/instru/change`          | instruType, instruPosition, instruName                                          |
| Change instrument options                     | `/instru/options/change`  | instruPosition, optionName, optionValue...                                      |

`instruPosition` : Channel position. Will use it to add beats, FXs, options etc. Negative integer to change or delete (see below) from the end

`optionName, optionValue...` : example : `[1, 'amp', 0.5, 'attack', 0.1]`

| Feature                   | OSC URI                  | Parameters                    |
| ------------------------- | ------------------------ | ----------------------------- |
| Remove instrument options | `/instru/options/remove` | instruPosition, optionName... |

`optionName...` : example : `[1, 'amp', 'attack']`

| Feature                       | OSC URI                      | Parameters             |
| ----------------------------- | ---------------------------- | ---------------------- |
| Remove all instrument options | `/instru/options/remove/all` | instruPosition         |

### Steps

| Feature        | OSC URI            | Parameters                         |
| -------------- | ------------------ | ---------------------------------- |
| Add step       | `/instru/step/add` | instruPosition, patternPosition, stepPosition, note |

`stepPosition` : Position on your channel

`patternPosition` : Pattern position

`note` : Note synth plays. Send any value (except null) for sample

| Feature        | OSC URI               | Parameters                   |
| -------------- | --------------------- | ---------------------------- |
| Remove step    | `/instru/step/remove` | instruPosition, patternPosition, stepPosition |

### FXs

| Feature        | OSC URI          | Parameters                                             |
| -------------- | ---------------- | ------------------------------------------------------ |
| Add FX         | `/instru/fx/add` | instruPosition, fxName, fxOptionName, fxOptionValue... |

`fxName` : FX name

`fxOptionName, fxOptionValue...` : FX options. Example `[3, 'reverb', 'mix', 1, 'room', 1]`

| Feature           | OSC URI                 | Parameters                                                 |
| ----------------- | ----------------------- | ---------------------------------------------------------- |
| Change FX options | `/instru/fx/change`     | instruPosition, fxPosition, fxOptionName, fxOptionValue... |
| Remove FX         | `/instru/fx/remove`     | instruPosition, fxPosition...                              |
| Remove all FXs    | `/instru/fx/remove/all` | instruPosition                                             |

`fxPosition` : FX position. Negative integer to change or delete from the end.

