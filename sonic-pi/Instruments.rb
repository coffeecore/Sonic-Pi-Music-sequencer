live_loop :add_instru do
  use_real_time
  use_cue_logging get(:cue_logging)
  use_debug get(:debug)
  osc        = sync '/osc*/instru/add/complete'
  instru     = JSON.parse osc[0]

  # instrus = get(:instrus)[0..]
  # instrus = get(:instrus).take(get(:instrus).length)
  instrus = ring_clone(get(:instrus))

  instrus.push(instru)
  # instrus = instrus+[instru]
  # instrus = ring_push(instrus, instru)

  set(:instrus, instrus)
end

live_loop :change_instru do
  use_real_time
  use_cue_logging get(:cue_logging)
  use_debug get(:debug)
  osc        = sync '/osc*/instru/change/complete'
  instru     = JSON.parse osc[0]
  position   = osc[1]

  instrus = ring_clone(get(:instrus))

  # instrus = get(:instrus)[0..]
  # instrus = get(:instrus).take(get(:instrus).length)
  instrus = ring_set_at(instrus, position, instru)

  # instrus[position] = instru
  # instrus = instrus.take(position)+[instru]+instrus.drop(position+1)

  set(:instrus, instrus)
end

live_loop :remove_instru do
  use_real_time
  use_cue_logging get(:cue_logging)
  use_debug get(:debug)
  osc       = sync '/osc*/instru/remove'
  instruPos = osc[0]

  instrus = ring_clone(get(:instrus))
  # instrus = get(:instrus)[0..]
  # instrus = get(:instrus).take(get(:instrus).length)

  # instrus.delete_at(instruPos)
  # instrus = instrus.take(instruPos)+instrus.drop(instruPos+1)

  instrus = ring_delete_at(instrus, instruPos)

  set(:instrus, instrus)
end

live_loop :change_instru do
  use_real_time
  use_cue_logging get(:cue_logging)
  use_debug get(:debug)
  osc        = sync '/osc*/instru/change'
  instruType = osc[0]
  instruPos  = osc[1]
  instruName = osc[2]

  # instrus = get(:instrus)[0..]
  # instrus = get(:instrus).take(get(:instrus).length)
  instrus = ring_clone(get(:instrus))
  instru  = (instrus[instruPos]).to_h

  instru['type'] = instruType
  instru['name'] = instruName

  instrus[instruPos] = instru

  set(:instrus, instrus)
end

live_loop :change_instru_options do
  use_real_time
  use_cue_logging get(:cue_logging)
  use_debug get(:debug)
  osc       = sync '/osc*/instru/options/change'
  instruPos = osc[0]
  # options   = osc[1..]
  options   = osc.drop(1)

  # instrus = get(:instrus)[0..]
  # instrus = get(:instrus).take(get(:instrus).length)
  instrus = ring_clone(get(:instrus))
  instru  = (instrus[instruPos]).to_h

  opts = instru['opts'].to_h

  options.each_with_index do |v, i|
    if i % 2 == 0 then
      opts[v.to_sym] = options[i+1]
    end
  end

  instru['opts'] = opts

  instrus[instruPos] = instru
  # instrus = instrus.take(instruPos)+[instru]+instrus.drop(instruPos+1)

  set(:instrus, instrus)
end

live_loop :remove_instru_options do
  use_real_time
  use_cue_logging get(:cue_logging)
  use_debug get(:debug)
  osc       = sync '/osc*/instru/options/remove'
  instruPos = osc[0]
  # options   = osc[1..]
  options   = osc.drop(1)
  instrus = ring_clone(get(:instrus))
  # instrus = get(:instrus)[0..]
  # instrus = get(:instrus).take(get(:instrus).length)
  instru  = (instrus[instruPos]).to_h

  opts = instru['opts'].to_h

  options.each_with_index do |v, i|
    opts.except!(v.to_sym)
  end

  instru['opts'] = opts

  instrus[instruPos] = instru
  # instrus = instrus.take(instruPos)+[instru]+instrus.drop(instruPos+1)
  set(:instrus, instrus)
end

live_loop :remove_all_instru_options do
  use_real_time
  use_cue_logging get(:cue_logging)
  use_debug get(:debug)
  osc       = sync '/osc*/instru/options/remove/all'
  instruPos = osc[0]

  # instrus = get(:instrus)[0..]
  # instrus = get(:instrus).take(get(:instrus).length)
  instrus = ring_clone(get(:instrus))
  instru  = (instrus[instruPos]).to_h

  instru['opts'] = {}

  # instrus[instruPos] = instru
  # instrus = instrus.take(instruPos)+[instru]+instrus.drop(instruPos+1)
  set(:instrus, instrus)
end
