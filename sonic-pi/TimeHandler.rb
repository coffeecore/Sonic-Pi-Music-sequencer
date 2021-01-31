live_loop :tempo do
    use_real_time
    use_bpm get(:bpm)
    sleep (1.0/get(:eighth))
end

live_loop :metronome do
  use_real_time
  use_bpm get(:bpm)
  if get(:metronome_state) && PLAY_STATE[get(:play_state).to_i] == 'play' && get(:n) % get(:eighth) == 0 then
    play 60, release: 0.001
  end
  sleep (1.0/get(:eighth))
end

live_loop :step do
    use_real_time
    use_bpm get(:bpm)


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
