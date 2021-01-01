live_loop :add_step do
  use_real_time
  osc = sync '/osc*/instru/step/add'
  instruPos = osc[0]
  stepPos = osc[1]
  note = osc[2]

  instrus = get(:instrus)[0..]
  instru = (instrus[instruPos]).to_h
  bts = instru[:steps][0..]
  if instru[:type] == 'sample' then
    note = 1
  end
  case stepPos
    when 0
      lu = [note]+bts[1..-1]
    when 1..14
      lu = bts[0..(stepPos-1)] +[note]+bts[(stepPos+1)..-1]
    when 15
      lu = bts[0..-2]+[note]
  end
  instru[:steps] = lu

  instrus[instruPos] = instru
  set(:instrus, instrus)
end

live_loop :remove_step do
  use_real_time
  osc = sync '/osc*/instru/step/remove'
  instruPos = osc[0]
  stepPos = osc[1]

  instrus = get(:instrus)[0..]
  instru = (instrus[instruPos]).to_h
  bts = instru[:steps]

  case stepPos
    when 0
      lu = [nil]+bts[1..-1]
    when 1..14
      lu = bts[0..(stepPos-1)] +[nil]+bts[(stepPos+1)..-1]
    when 15
      lu = bts[0..-2]+[nil]
  end
  instru[:steps] = bts

  instrus[instruPos] = instru
  set(:instrus, instrus)
end
