live_loop :add_step do
  use_real_time
  osc        = sync '/osc*/instru/step/add'
  instruPos  = osc[0]
  patternPos = osc[1]
  stepPos    = osc[2]
  note       = osc[3]

  instrus = get(:instrus)[0..]
  instru  = (instrus[instruPos]).to_h
  steps = instru['steps'][0..][patternPos]

  if steps == nil then
    steps = Array.new(get(:end)+1)
  end

  if instru['type'] == 'sample' || instru['type'] == 'external_sample' then
    note = 1
  end
  case stepPos
    when 0
      steps = [note]+steps[1..-1]
    when 1..(get(:end)-1)
      steps = steps[0..(stepPos-1)] +[note]+steps[(stepPos+1)..-1]
    when get(:end)
      steps = steps[0..-2]+[note]
  end

  ss = instru['steps'][0..]

  ss[patternPos] = steps

  instru['steps'] = ss

  instrus[instruPos] = instru

  set(:instrus, instrus)
end

live_loop :remove_step do
  use_real_time
  osc        = sync '/osc*/instru/step/remove'
  instruPos  = osc[0]
  patternPos = osc[1]
  stepPos    = osc[2]

  instrus = get(:instrus)[0..]
  instru  = (instrus[instruPos]).to_h
  steps   = instru['steps'][patternPos]

  case stepPos
    when 0
      steps = [nil]+steps[1..-1]
    when 1..(get(:end)-1)
      steps = bts[0..(stepPos-1)] +[nil]+steps[(stepPos+1)..-1]
    when get(:end)
      steps = steps[0..-2]+[nil]
  end
  instru['steps'][patternPos] = steps

  instrus[instruPos] = instru
  set(:instrus, instrus)
end
