PLAY_STATE    = ['stop', 'play', 'pause']
SEQUENCER_MOD = ['sequencer', 'single']
FILE_PATH     = "/Users/antoine/Music/Sonic Pi"

define :reset_f do
  set :instrus, []
  # Result 4/4 with sixteenth note.
  # To have 3/4 with eighth note set "eighth" to 2 and "bar" to 3
  set :startBar, 0
  set :eighth, 4
  set :bar, 4
  set :endBar, ((get(:eighth)*get(:bar))-1)
  #
  set :n, 0 # Increment step position
  set :pmax, 1 # Max patterns to play in sequencer mod
  set :p, 0 # Pattern to play in single mod
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

live_loop :reset do
  use_real_time
  osc    = sync "/osc*/reset"
  reset_f
end

live_loop :global_volume do
  use_real_time
  osc    = sync "/osc*/volume"
  volume = osc[0]
  set :volume, volume

  set_volume! get(:volume)
end

# live_loop :set_debug do
#   use_real_time
#   osc = sync "/osc*/debug"

#   if osc[0] == 1 then
#     puts "DEBUG MODE ENABLING..."
#     set :debug, true
#     puts "DEBUG MODE ENABLED"
#   else
#     puts "DEBUG MODE DISABLING..."
#     set :debug, false
#     puts "DEBUG MODE DISABLED"
#   end
# end

live_loop :set_sequencer_mod do
  use_real_time
  osc = sync "/osc*/sequencer_mod"
  set :sequencer_mod, osc[0]
  puts "SEQUENCER MODE : #{SEQUENCER_MOD[osc[0]]}"
end

live_loop :set_max_pattern do
  use_real_time
  osc = sync "/osc*/pattern/max"
  set :pmax, osc[0]
end

live_loop :set_pattern do
  use_real_time
  osc = sync "/osc*/pattern"
  set :p, osc[0]
end
run_file "#{FILE_PATH}/sonic-pi/functions.rb"
run_file "#{FILE_PATH}/sonic-pi/FXs.rb"
run_file "#{FILE_PATH}/sonic-pi/Instruments.rb"
run_file "#{FILE_PATH}/sonic-pi/Loop.rb"
run_file "#{FILE_PATH}/sonic-pi/PlayState.rb"
# run_file "#{FILE_PATH}/sonic-pi/Record.rb"
run_file "#{FILE_PATH}/sonic-pi/Steps.rb"
run_file "#{FILE_PATH}/sonic-pi/Patterns.rb"
run_file "#{FILE_PATH}/sonic-pi/TimeHandler.rb"
