live_loop :start_play do
  use_real_time
  # use_debug get(:debug)
  # use_cue_logging get(:cue_logging)
  osc = sync "/osc*/start"

  playState = get(:play_state)

  if playState == 0 then
    set :n, get(:startBar)
  end

  set :play_state, 1
end

live_loop :stop_play do
  use_real_time
  # use_debug get(:debug)
  # use_cue_logging get(:cue_logging)
  osc = sync "/osc*/stop"

  set :n, 0
  set :play_state, 0
end

live_loop :pause_play do
  use_real_time
  # use_debug get(:debug)
  # use_cue_logging get(:cue_logging)
  osc = sync "/osc*/pause"

  set :play_state, 2
end
