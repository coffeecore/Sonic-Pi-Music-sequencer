live_loop :add_pattern do
  use_real_time
  # use_cue_logging get(:cue_logging)
  # use_debug get(:debug)
  osc        = sync '/osc*/instru/pattern/add'
  instruPos  = osc[0]

  instrus = get(:instrus)[0..-1]

  instru  = (instrus[instruPos]).to_h

  patterns = instru['patterns'][0..-1]

  patterns.push(Array.new(get(:endBar)+1))

  instru['patterns'] = patterns

  instrus[instruPos] = instru

  set(:instrus, instrus)
end

live_loop :remove_pattern do
  use_real_time
  # use_cue_logging get(:cue_logging)
  # use_debug get(:debug)
  osc        = sync '/osc*/instru/pattern/remove'
  instruPos  = osc[0]
  patternPos = osc[1]

  instrus = get(:instrus)[0..-1]
  instru  = (instrus[instruPos]).to_h
  patterns   = instru['patterns'][0..-1]

  patterns.delete_at(patternPos)

  instru['patterns'] = patterns

  instrus[instruPos] = instru
  set(:instrus, instrus)
end
