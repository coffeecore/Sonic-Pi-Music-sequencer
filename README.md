# :musical_keyboard: Sonic Pi sequencer with Piano HAT

A very simple step pattern and music instrument powered by [Sonic Pi](https://sonic-pi.net/ "Sonic Pi - The Live Coding Music Synth for Everyone") and controled by a [Piano HAT](https://github.com/pimoroni/Piano-HAT "Python library and examples for Piano HAT Raspberry Pi Add-on board") ~, some potards, buttons and with a E-Ink screen~ (N/A) 

- 40 patterns (more if you use Sonic Pi part only)
- 8 steps by pattern (more if you use Sonic Pi part only)
    - WIP to have 32 steps by pattern
- instrument mode
- Sonic Pi Synth
- Samples
- Options
- FXs
- ~Midi note~ (N/A)

## UI (WIP)

![ui_preview](https://github.com/coffeecore/sonic-pi-json-sequencer/raw/master/ui.png)

## Todo

- [ ] Platforms :
    - [x] Rpi3 : [2021-03-24] Project runs
        - Reverb FX consumes too many resources
        - Remove some commands (see strikethrough lines below)
    - [ ] RPi4 (don't own for the moment)
    - [x] Mac OS X (10.14.6) :
        - All commands work
- [x] Sonic Pi part :
    - [x] Add code live play
        - [x] Add FX
        - [x] Add options
    - [x] Optimize for Rpi
- [ ] Python part :
    - [ ] Clean code...
    - [ ] Piano HAT (WIP) [2021-03-24] Major features made
        - [x] Config file for channels configuration
        - [x] ~Change JSON format to MessagePack~ (Impossible to use Ruby Gem on Sonic Pi)
        - [x] ~Add default live options~
        - [x] ~Add defaults live FXs~
        - [ ] Add more steps with black keys
    - [ ] Potards / Buttons
        - [ ] Add channel on the fly
        - [ ] Change channel sample/synth
        - [ ] Add/remove FXs
        - [ ] Add/remove default channel options
        - [ ] Add/remove default live options
        - [ ] Add/remove default live Fxs
        - [ ] Add/remove step options
        - [ ] Control live played note
    - [ ] E-ink display
    - [ ] Use keyboard to replace Piano HAT if you don't have one

## OSC commands

| Feature                            | OSC URI          | Parameters                                                  |
| ---------------------------------- | ---------------- | ----------------------------------------------------------- |
| Set global volume                  | /settings        | ['volume', Float] between 0 and 5                |
| Set playback state                 | /settings        | ['state', value] `stop` (default), `play` or `pause`        |
| Set bpm                            | /settings        | ['bpm', Integer] default : 60                               |
| ~Set eighth (One sleep divided by)~  | ~/settings~        | ~['eighth', Integer] default : 4~                             |
| Set bar (Sleeps between patterns)  | /settings        | ['bar', Integer] default : 1                                |
| Set max pattern to play            | /settings        | ['pmax', Integer] default : 4                               |
| Kill a loop                        | /kill            | String `live_loop` name                                     |
| ~Set channels~                     | ~/channels~      | ~Json~                                                      |
| ~Send signal to read json channel file~  | ~/channel/json/file~         | ~[Integer `position`]~                                  |
| Set channel                        | /channel/json         | [Integer `position`, Json]       |
| Play a note on channel  | /channel/play         | [Integer `position`, note]       |
| ~Channel opts~                       | ~/channel/options~ | ~[String `live_loop` name, Json]~                             |
| ~Channel FXs~                        | ~/channel/fxs~     | ~[String `live_loop` name, String FX name, Json]~             |
| Start record (*Experimental*)      | /record/start    | Start to record                                             |
| Stop record (*Experimental*)       | /record/stop     | Stop record                                                 |
| Save record (*Experimental*)       | /record/save     | Save record (Change `FILE_PATH` constant in `main.rb` file) |

Record features are commented in `main.rb`, some time issues on Rpi 3 for the moment.

## Run

Change IP in `python/main.py`

### Sonic Pi

`run_file "/absolute/path/to/main.rb"`

### Python

- [python-osc](https://pypi.org/project/python-osc/)
- [PianoHAT](https://github.com/pimoroni/Piano-HAT/)

`python3 python/main.py`
