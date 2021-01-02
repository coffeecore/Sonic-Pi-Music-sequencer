live_loop :add_step do
  use_real_time
  osc       = sync '/osc*/instru/step/add'
  instruPos = osc[0]
  stepPos   = osc[1]
  note      = osc[2]

  instrus = get(:instrus)[0..]
  instru  = (instrus[instruPos]).to_h

  steps = instru['steps'][0..]
  if instru['type'] == 'sample' || instru['type'] == 'external_sample' then
    note = 1
  end
  case stepPos
    when 0
      steps = [note]+steps[1..-1]
    when 1..14
      steps = steps[0..(stepPos-1)] +[note]+steps[(stepPos+1)..-1]
    when 15
      steps = steps[0..-2]+[note]
  end
  instru['steps'] = steps

  instrus[instruPos] = instru
  set(:instrus, instrus)
end

live_loop :remove_step do
  use_real_time
  osc       = sync '/osc*/instru/step/remove'
  instruPos = osc[0]
  stepPos   = osc[1]

  instrus = get(:instrus)[0..]
  instru  = (instrus[instruPos]).to_h
  steps   = instru['steps']

  case stepPos
    when 0
      steps = [nil]+steps[1..-1]
    when 1..14
      steps = bts[0..(stepPos-1)] +[nil]+steps[(stepPos+1)..-1]
    when 15
      steps = steps[0..-2]+[nil]
  end
  instru['steps'] = steps

  instrus[instruPos] = instru
  set(:instrus, instrus)
end
