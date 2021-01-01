set :bpm, 60
set :metronome_state, true


live_loop :metronome do
  use_real_time

  # sync :t
  use_bpm get(:bpm)

  if get(:metronome_state) && PLAY_STATE[get(:play_state).to_i] == 'play' then
    play 60, release: 0.01
  end

  sleep 1
end

live_loop :set_eighth do
  use_real_time
  osc = sync "/osc*/eighth"
  set :eighth, osc[0]

  set(:end, ((osc[0]*4)-1)) if SEQUENCER_MOD[get(:sequencer_mod).to_i] == 'step'
end

live_loop :set_end do
  use_real_time
  osc = sync "/osc*/end"

  set(:end, osc[0]) if SEQUENCER_MOD[get(:sequencer_mod).to_i] == 'tracker'
end

live_loop :set_metronome do
  use_real_time
  osc = sync "/osc*/metronome"

  if osc[0] == 1 then
    set :metronome_state, true
    puts "METRONOME ENABLED"
  else
    set :metronome_state, false
    puts "METRONOME DISABLED"
  end
end

live_loop :tempo do
  use_real_time
  cue :t
  use_bpm get(:bpm)

  while get(:play_state) != 1 do
    if get(:play_state) == 0 then
      tick_reset
    end
    sleep (1.0/get(:eighth))
  end

  tick
  n = look

  set :n, n
  tick_set get(:start) if look >= get(:end)

  sleep (1.0/get(:eighth))
end

live_loop :set_bpm do
  osc = sync '/osc*/bpm'
  set :bpm, osc[0]
end
