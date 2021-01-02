PLAY_STATE    = ['stop', 'play', 'pause']
SEQUENCER_MOD = ['step', 'tracker']
PATH_FILE     = "/Users/antoine/Music/Sonic Pi/"

set :instrus, []
set :start, 0
set :eighth, 4
set :end, ((get(:eighth)*4)-1)
set :n, 0
set :bpm, 60
set :volume, 5
set :debug, false
set :metronome_state, true
set :play_state, PLAY_STATE[0]
set :sequencer_mod, SEQUENCER_MOD[0]

use_osc "127.0.0.1", 7000

set_volume! get(:volume)

live_loop :start_play do
  use_real_time
  osc = sync "/osc*/start"

  set :play_state, 1
end

live_loop :stop_play do
  use_real_time
  osc = sync "/osc*/stop"

  set :n, 0
  set :play_state, 0
end

live_loop :pause_play do
  use_real_time
  osc = sync "/osc*/pause"

  set :play_state, 2
end


live_loop :global_volume do
  use_real_time
  osc    = sync "/osc*/volume"
  volume = osc[0]
  set :volume, volume

  set_volume! get(:volume)
end

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

live_loop :set_sequencer_mod do
  use_real_time
  osc = sync "/osc*/sequencer_mod"
  set :sequencer_mod, osc[0]
  puts "SEQUENCER MODE : #{SEQUENCER_MOD[osc[0]]}"
end

# Manage steps
run_file "#{PATH_FILE}steps.rb"
# Manage FXs
run_file "#{PATH_FILE}fxs.rb"
# Manage instruments
run_file "#{PATH_FILE}instrus.rb"
# Manage time
run_file "#{PATH_FILE}metronome.rb"
# Play all together
run_file "#{PATH_FILE}play.rb"
