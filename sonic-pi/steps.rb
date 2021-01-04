live_loop :add_step do
  use_real_time
  osc        = sync '/osc*/instru/step/add'
  instruPos  = osc[0]
  patternPos = osc[1]
  stepPos    = osc[2]
  note       = osc[3]

  instrus = get(:instrus)[0..]
  instru  = (instrus[instruPos]).to_h
  patterns = instru['patterns'][0..][patternPos]

  if patterns == nil then
    patterns = Array.new(get(:end)+1)
  end

  if instru['type'] == 'sample' || instru['type'] == 'external_sample' then
    note = 1
  end
  case stepPos
    when 0
      patterns = [note]+patterns[1..-1]
    when 1..(get(:end)-1)
      patterns = patterns[0..(stepPos-1)] +[note]+patterns[(stepPos+1)..-1]
    when get(:end)
      patterns = patterns[0..-2]+[note]
  end

  ss = instru['patterns'][0..]

  ss[patternPos] = patterns

  instru['patterns'] = ss

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
  patterns   = instru['patterns'][patternPos]

  case stepPos
    when 0
      patterns = [nil]+patterns[1..-1]
    when 1..(get(:end)-1)
      patterns = bts[0..(stepPos-1)] +[nil]+patterns[(stepPos+1)..-1]
    when get(:end)
      patterns = patterns[0..-2]+[nil]
  end
  instru['patterns'][patternPos] = patterns

  instrus[instruPos] = instru
  set(:instrus, instrus)
end
