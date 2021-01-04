live_loop :metronome do
  use_real_time

  # sync :t
  use_bpm get(:bpm)

  if get(:metronome_state) && PLAY_STATE[get(:play_state).to_i] == 'single' then
    play 60, get(:metronome_options).to_h
  end

  sleep 1
end

live_loop :set_eighth do
  use_real_time
  osc = sync "/osc*/eighth"
  set :eighth, osc[0]

  set(:endBar, ((osc[0]*get(:bar))-1)) #if SEQUENCER_MOD[get(:sequencer_mod).to_i] == 'sequencer'
end

live_loop :set_bar do
  use_real_time
  osc = sync "/osc*/bar"
  set :bar, osc[0]

  set(:endBar, ((get(:eighth)*osc[0])-1)) #if SEQUENCER_MOD[get(:sequencer_mod).to_i] == 'sequencer'
end

live_loop :set_end do
  use_real_time
  osc = sync "/osc*/end"

  set(:endBar, osc[0]) if SEQUENCER_MOD[get(:sequencer_mod).to_i] == 'tracker'
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

live_loop :set_metronome_options do
  use_real_time
  osc = sync "/osc*/metronome/options"

  options   = osc[0..]

  opts = get(:metronome_options).to_h

  options.each_with_index do |v, i|
    if i % 2 == 0 then
      opts[v.to_sym] = options[i+1]
    end
  end

  set(:metronome_options, opts)
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

  p = get(:p)

  if SEQUENCER_MOD[get(:sequencer_mod).to_i] != 'single' then
    set :p, p+1 if n != 0 and n % (get(:endBar)-1) == 0
    set :p, get(:startBar) if p >= get(:pmax)
  end

  tick_set get(:startBar) if look >= get(:endBar)

  sleep (1.0/get(:eighth))
end

live_loop :set_bpm do
  osc = sync '/osc*/bpm'
  set :bpm, osc[0]
end
