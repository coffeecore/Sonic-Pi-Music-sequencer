# :musical_keyboard: Sonic Pi Json Sequencer

Launch Sonic Pi `live_loop` from json.

## Todo

- [ ] Run on RPi...
    - [x] Test with Rpi3 : `test.py` file works. Must try more heavy file
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
        "synth": "tb303",
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
            []
        ]
    },
    {
        "type": "sample",
        "sample": "drum_cymbal_closed",
        "opts": {
        },
        "fxs": {
        },
        "patterns": [
            []
        ]
    },
    {
        "type": "external_sample",
        "sample": "/home/pi/mysample.ext",
        "opts": {
        },
        "fxs": {
        },
        "patterns": [
            []
        ]
    }
]
```

Will result `live_loop` name to :
- synth_0
- sample_1
- external_sample_2

See begin of `compo.py` for example.

## OSC commands

| Feature                 | OSC URI              | Parameters                                                  |
| ----------------------- | -------------------- | ----------------------------------------------------------- |
| Set global volume       | /volume              | Number between `0` and `5`                                  |
| Set playback state      | /state               | String `stop`, `play` or `pause`                            |
| Set bpm                 | /settings            | ['bpm', Integer]                                            |
| Set eighth              | /settings            | ['eighth', Integer]                                         |
| Set max pattern to play | /settings            | ['pmax', Integer] (default : 4)                             |
| Kill a loop             | /kill                | String `live_loop` name                                     |
| Set patterns            | /patterns            | Json                                                        |
| Set pattern             | /pattern             | [Integer `position`, Json]                                  |
| Start record            | /record/start        | Start to record                                             |
| Stop record             | /record/stop         | Stop record                                                 |
| Save record             | /record/save         | Save record (Change `FILE_PATH` constant in `main.rb` file) |

## Run

`run_file "/absolute/path/to/main.rb"`
