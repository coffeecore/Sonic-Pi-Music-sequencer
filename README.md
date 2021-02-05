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

See begin of `test.py` for example.

## OSC commands

| Feature                            | OSC URI          | Parameters                                                  |
| ---------------------------------- | ---------------- | ----------------------------------------------------------- |
| Set global volume                  | /volume          | Number between `0` and `5`                                  |
| Set playback state                 | /state           | String `stop`, `play` or `pause`                            |
| Set bpm                            | /settings        | ['bpm', Integer] (default : 60)                             |
| Set eighth                         | /settings        | ['eighth', Integer] (default : 4)                           |
| Set bar (Sleep between patterns)   | /settings        | ['bar', Integer] (default : 1)                              |
| Set max pattern to play            | /settings        | ['pmax', Integer] (default : 4)                             |
| Kill a loop                        | /kill            | String `live_loop` name                                     |
| Set channels                       | /channels        | Json                                                        |
| Set channel                        | /channel         | [Integer `position`, Json]                                  |
| [WIP] Channel opts                 | /channel/options | [String `live_loop` name, Json]                             |
| Start record                       | /record/start    | Start to record                                             |
| Stop record                        | /record/stop     | Stop record                                                 |
| Save record                        | /record/save     | Save record (Change `FILE_PATH` constant in `main.rb` file) |

Record features are commented in `main.rb`, some time issues on Rpi 3 for the moment.

## Run

`run_file "/absolute/path/to/main.rb"`
