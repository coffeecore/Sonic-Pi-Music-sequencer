PLAY_STATE    = ['stop', 'play', 'pause']
SEQUENCER_MOD = ['sequencer', 'single']
FILE_PATH     = "/Users/antoine/Music/Sonic Pi"

set :instrus, []
set :startBar, 0
set :eighth, 4
set :bar, 4
set :endBar, ((get(:eighth)*get(:bar))-1)
set :n, 0
set :pmax, 2
set :p, 0
set :bpm, 60
set :volume, 5
set :debug, false
set :metronome_state, true
set :play_state, PLAY_STATE[0]
set :sequencer_mod, SEQUENCER_MOD[0]
set :metronome_options, {
  'release' => 0.01
}
sleep 0.01
use_osc "127.0.0.1", 7000

set_volume! get(:volume)

# Set play state on "start"
#
live_loop :start_play do
  use_real_time
  osc = sync "/osc*/start"

  set :play_state, 1
end

# Set play state on "stop"
#
live_loop :stop_play do
  use_real_time
  osc = sync "/osc*/stop"

  set :n, 0
  set :play_state, 0
end


# Set play state on "pause"
#
live_loop :pause_play do
  use_real_time
  osc = sync "/osc*/pause"

  set :play_state, 2
end


# Set global volume
#
# Parameter :
# - integer between 0 and 5
#
live_loop :global_volume do
  use_real_time
  osc    = sync "/osc*/volume"
  volume = osc[0]
  set :volume, volume

  set_volume! get(:volume)
end

# Set debug mode on/off
#
# Parameter :
# - 0 (disable) or 1 (enable)
#
live_loop :set_debug do
  use_real_time
  osc = sync "/osc*/debug"
  if osc[0] == 1 then
    puts "DEBUG MODE ENABLING..."
    set :debug, true
    puts "DEBUG MODE ENABLED"
  else
    puts "DEBUG MODE DISABLING..."
    set :debug, false
    puts "DEBUG MODE DISABLED"
  end
end

# Set sequencer mod
#
# Parameter :
# - 0 (sequencer), 1 (single)
#
# sequencer :
# signle
#
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

# Manage steps
run_file "#{FILE_PATH}/sonic-pi/steps.rb"
# Manage FXs
run_file "#{FILE_PATH}/sonic-pi/fxs.rb"
# Manage instruments
run_file "#{FILE_PATH}/sonic-pi/instrus.rb"
# Manage time
run_file "#{FILE_PATH}/sonic-pi/metronome.rb"
# Play all together
run_file "#{FILE_PATH}/sonic-pi/play.rb"
