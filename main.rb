PLAY_STATE    = ['stop', 'play', 'pause']
SEQUENCER_MOD = ['sequencer', 'single']
FILE_PATH     = "/Users/antoine/Music/Sonic Pi"
# FILE_PATH     = "/home/pi/Desktop/sonic-pi-music-step-sequencer"

define :reset_f do
  set :instrus, []
  # Result 4/4 with sixteenth note.
  # To have 3/4 with eighth note set "eighth" to 2 and "bar" to 3
  set :startBar, 0
  set :eighth, 1
  set :bar, 4
  set :endBar, ((get(:eighth)*get(:bar))-1)
  #
  set :n, -1 # Increment step position
  set :pmax, 1 # Max patterns to play in sequencer mod
  set :p, -1 # Pattern to play in single mod
  set :bpm, 60
  set :volume, 5
  # set :debug, false
  # set :cue_logging, false
  set :metronome_state, false
  set :play_state, 0 #stop
  set :sequencer_mod, 0 #sequencer
  set :metronome_options, {
    'release' => 0.001
  }
end

reset_f

use_osc "127.0.0.1", 7000

set_volume! get(:volume)

live_loop :set do
  use_real_time
  osc = sync "/osc*/set"
  name = osc[0]

  case name
  when 'eighth'
    set :eighth, osc[1]
    set(:endBar, ((osc[1]*get(:bar))-1))
  when 'bar'
    set :bar, osc[1]
    set(:endBar, ((get(:eighth)*osc[1])-1))
  when 'bpm'
    set :bpm, osc[1]
  when 'metronome_state'
    if osc[1] == 1 then
      set :metronome_state, true
    else
      set :metronome_state, false
    end
  when 'pattern'
    set :p, osc[1]
  when 'pattern_max'
    set :pmax, osc[1]
  when 'volume'
    set :volume, volume
    set_volume! get(:volume)
  when 'sequencer_mod'
    set :sequencer_mod, osc[1]
    puts "SEQUENCER MODE : #{SEQUENCER_MOD[osc[1]]}"
  end
end

run_file "#{FILE_PATH}/sonic-pi/Json.rb"
run_file "#{FILE_PATH}/sonic-pi/PlayState.rb"
# run_file "#{FILE_PATH}/sonic-pi/Record.rb"
run_file "#{FILE_PATH}/sonic-pi/TimeHandler.rb"
run_file "#{FILE_PATH}/sonic-pi/Loop.rb"
