live_loop :add_pattern do
  use_real_time
  use_cue_logging get(:cue_logging)
  use_debug get(:debug)
  osc        = sync '/osc*/instru/pattern/add'
  instruPos  = osc[0]

  # instrus = get(:instrus)[0..]
  instrus = get(:instrus).take(get(:instrus).length)

  instru  = (instrus[instruPos]).to_h

  # patterns = instru['patterns'][0..]
  patterns = instru['patterns'].take(instru['patterns'].length)

  patterns.push(Array.new(get(:endBar)+1))

  instru['patterns'] = patterns

  # instrus[instruPos] = instru

  instrus = instrus.take(instruPos)+[instru]+instrus.drop(instruPos+1)

  set(:instrus, instrus)
end

live_loop :remove_pattern do
  use_real_time
  use_cue_logging get(:cue_logging)
  use_debug get(:debug)
  osc        = sync '/osc*/instru/pattern/remove'
  instruPos  = osc[0]
  patternPos = osc[1]

  # instrus = get(:instrus)[0..]
  instrus = get(:instrus).take(get(:instrus).length)
  instru  = (instrus[instruPos]).to_h
  # patterns   = instru['patterns'][0..]
  patterns   = instru['patterns'].take(get(:instrus).length)

  patterns.delete_at(patternPos)

  instru['patterns'] = patterns

  # instrus[instruPos] = instru

  instrus = instrus.take(instruPos)+[instru]+instrus.drop(instruPos+1)
  set(:instrus, instrus)
end
