# :musical_keyboard: Sonic Pi Json

Launch `live_loop` with Json.

:warning: Not work on Rpi3. Must try on Rpi4

## Todo

[ ] Run on RPi...

## Json

```
[
    {
        // Loop name : synth_0
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
        // Loop name : sample_1
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
        // Loop name : external_sample_2
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

## OSC commands

| Feature                 | OSC URI              | Parameters                                                  |
| ----------------------- | -------------------- | ----------------------------------------------------------- |
| Set global volume       | /volume              | Number between `0` and `5`                                  |
| Set bpm                 | /bpm                 | Integer                                                     |
| Set playback state      | /state               | String `stop`, `play` or `pause`                            |
| Set eighth              | /measure             | ['eighth', integer]                                         |
| Set bar                 | /measure             | ['bar', integer]                                            |
| Kill a loop             | /kill                | String loop name                                            |
| Set patterns            | /patterns            | Json                                                        |
| Set pattern             | /pattern             | [Integer `position`, Json]                                  |
| Start record            | /record/start        | Start to record                                             |
| Stop record             | /record/stop         | Stop record                                                 |
| Save record             | /record/save         | Save record (Change `FILE_PATH` constant in `main.rb` file) |

## Run

`run_file "/absolute/path/to/main.rb"`
