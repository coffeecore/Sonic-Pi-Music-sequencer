live_loop :add_beat do
  use_real_time
  osc = sync '/osc*/instru/beat/add'
  instruPos = osc[0]
  beatPos = osc[1]
  note = osc[2]

  bts = get(':beats'+instruPos.to_s)
  instrus = get(:instrus).to_h
  instru = (instrus[instruPos]).to_h
  if instru[:type] == 'sample' then 
    note = 1
  end
  case beatPos #check the new data position in the array
    when 0 # deals with new value at the beginning
      lu = [note]+bts[1..-1]
    when 1..14 #deals with new value at position 1 to 14 (index from 0)
      lu = bts[0..(beatPos-1)] +[note]+bts[(beatPos+1)..-1]
    when 15 #deals with new value at the end of the array
      lu = bts[0..-2]+[note]
  end
  set (":beats"+instruPos.to_s), lu
end

live_loop :remove_beat do
  use_real_time
  osc = sync '/osc*/instru/beat/remove'
  instruPos = osc[0]
  beatPos = osc[1]

  bts = get(':beats'+instruPos.to_s)
  case beatPos #check the new data position in the array
    when 0 # deals with new value at the beginning
      lu = [nil]+bts[1..-1]
    when 1..14 #deals with new value at position 1 to 14 (index from 0)
      lu = bts[0..(beatPos-1)] +[nil]+bts[(beatPos+1)..-1]
    when 15 #deals with new value at the end of the array
      lu = bts[0..-2]+[nil]
  end
  set (":beats"+instruPos.to_s), lu
end
