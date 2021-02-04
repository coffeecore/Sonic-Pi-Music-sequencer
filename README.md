# :musical_keyboard: Sonic Pi Json Sequencer

Launch Sonic Pi `live_loop` from json.

:warning: Not work on Rpi3.

## Todo

- [ ] Run on RPi...
    - [x] Test with Rpi3 : __Not work__
    - [ ] Test with RPi4
- [ ] Python part :
    - [ ] Piano HAT
    - [ ] Potards
    - [ ] E-ink display

## Json

```json
[
    {
        "type": "synth",
        "synth": "", // synth name (ex: tb303)
        "opts": {
            "release": 0.125,
            "cutoff": 120,
            "res": 0.5
        },
        "fxs": {
            "distortion": {
                "distort": 0.99
            }
        },
        "patterns": [
            "(chord :e3, :minor)", ":g3", [":g3", ":g4"], null
        ]
    },
    {
        "type": "sample",
        "sample": "", // sample name (ex: drum_cymbal_closed)
        "opts": {
        },
        "fxs": {
        },
        "patterns": [
            true, false, null
        ]
    },
    {
        "type": "external_sample",
        "sample": "", // path to external sample (ex: /home/pi/mysample.ext)
        "opts": {
        },
        "fxs": {
        },
        "patterns": [
            true, false, null
        ]
    }
]
```

Will result `live_loop` name to :
- synth_0
- sample_1
- external_sample_2

## OSC commands

| Feature                 | OSC URI              | Parameters                                                  |
| ----------------------- | -------------------- | ----------------------------------------------------------- |
| Set global volume       | /volume              | Number between `0` and `5`                                  |
| Set bpm                 | /bpm                 | Integer                                                     |
| Set playback state      | /state               | String `stop`, `play` or `pause`                            |
| Set eighth              | /measure             | ['eighth', integer]                                         |
| Set bar                 | /measure             | ['bar', integer]                                            |
| Kill a loop             | /kill                | String `live_loop` name                                     |
| Set patterns            | /patterns            | Json                                                        |
| Set pattern             | /pattern             | [Integer `position`, Json]                                  |
| Start record            | /record/start        | Start to record                                             |
| Stop record             | /record/stop         | Stop record                                                 |
| Save record             | /record/save         | Save record (Change `FILE_PATH` constant in `main.rb` file) |

## Run

`run_file "/absolute/path/to/main.rb"`
