live_loop :tempo do
    use_real_time
    use_bpm get(:bpm)
    # use_debug get(:debug)
    # use_cue_logging get(:cue_logging)
    # cue :temp
    sleep (1.0/get(:eighth))
end

live_loop :metronome do
  # sync :temp
  use_real_time
  use_bpm get(:bpm)
  # use_debug get(:debug)
  # use_cue_logging get(:cue_logging)
  if get(:metronome_state) && PLAY_STATE[get(:play_state).to_i] == 'play' && get(:n) % get(:eighth) == 0 then
    play 60, release: 0.001
  end
  sleep 1
end

live_loop :set_eighth do
  use_real_time
  # use_debug get(:debug)
  # use_cue_logging get(:cue_logging)
  osc = sync "/osc*/eighth"
  set :eighth, osc[0]

  set(:endBar, ((osc[0]*get(:bar))-1))
end

live_loop :set_bar do
  use_real_time
  # use_debug get(:debug)
  # use_cue_logging get(:cue_logging)
  osc = sync "/osc*/bar"
  set :bar, osc[0]

  set(:endBar, ((get(:eighth)*osc[0])-1))
end

live_loop :set_bpm do
    # use_debug get(:debug)
    use_cue_logging get(:cue_logging)
  osc = sync '/osc*/bpm'
  set :bpm, osc[0]
end

live_loop :set_metronome do
  use_real_time
  # use_debug get(:debug)
  # use_cue_logging get(:cue_logging)
  osc = sync "/osc*/metronome"

  if osc[0] == 1 then
    set :metronome_state, true
  else
    set :metronome_state, false
  end
end

live_loop :step do
    use_real_time
    use_bpm get(:bpm)
    # use_debug get(:debug)
    # use_cue_logging get(:cue_logging)

    while PLAY_STATE[get(:play_state).to_i] != 'play' do
        if PLAY_STATE[get(:play_state).to_i] == 'stop' then
            tick_reset
        end
        sleep (1.0/get(:eighth))
    end

    tick
    n = look
    set :n, n

    tick_set get(:startBar) if look >= get(:endBar)

    sleep (1.0/get(:eighth))
end
