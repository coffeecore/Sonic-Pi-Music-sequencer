STATE = (map stop: 0, play: 1, pause: 2)

use_debug false
use_cue_logging false
set :state, STATE[:stop]
set :eighth, 4
set :bar, 4
set :bpm, 60
set :sleep, 1.0/get(:eighth)

live_loop :metronome do
  use_real_time
  use_bpm get :bpm
  while get(:state) === STATE[:pause] or get(:state) === STATE[:stop]
      sleep (1.0/get(:eighth))
  end
  t = tick
  cue :n, (t % (get(:bar)*get(:eighth)))
  sleep get :sleep
end

live_loop :set_measure_settings do
  osc = sync "/osc*/measure"

  set osc[0].to_sym, osc[1]
  set :sleep, 1.0/get(:eighth)
end

live_loop :set_bpm do
  osc = sync "/osc*/bpm"

  set :bpm, osc[0]
end

live_loop :kill_loop do
  osc = sync "/osc*/kill"
  live_loop (osc[0]).to_sym do
    stop
  end
end

live_loop :patterns do
  osc = sync "/osc*/patterns"
  instrus     = JSON.parse(osc[0], :symbolize_names => true)
  instrus.each do |i|
    create_loop i
  end
end

live_loop :pattern do
  osc = sync "/osc*/pattern"
  instru     = JSON.parse(osc[0], :symbolize_names => true)

  create_loop instru
end

define :create_loop do |i|
  create_loop_synth(i) if i[:type] === 'synth'
  create_loop_external_sample i if i[:type] === 'external_sample'
  create_loop_sample i if i[:type] === 'sample'
end

live_loop :set_state do
  osc = sync "/osc*/state"
  state = get :state
  set :state, STATE[osc[0].to_sym]
  if state ===  STATE[:stop] and osc[0] === 'play' then
    cue :n, 0
  end
end

run_file "/Users/antoine/Music/Sonic Pi/sonic-pi-new/synth.rb"
run_file "/Users/antoine/Music/Sonic Pi/sonic-pi-new/external-sample.rb"
run_file "/Users/antoine/Music/Sonic Pi/sonic-pi-new/sample.rb"
