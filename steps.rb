live_loop :add_step do
  use_real_time
  osc = sync '/osc*/instru/step/add'
  instruPos = osc[0]
  stepPos = osc[1]
  note = osc[2]

  bts = get(':steps'+instruPos.to_s)
  instrus = get(:instrus).to_h
  instru = (instrus[instruPos]).to_h
  if instru[:type] == 'sample' then 
    note = 1
  end
  case stepPos #check the new data position in the array
    when 0 # deals with new value at the beginning
      lu = [note]+bts[1..-1]
    when 1..14 #deals with new value at position 1 to 14 (index from 0)
      lu = bts[0..(stepPos-1)] +[note]+bts[(stepPos+1)..-1]
    when 15 #deals with new value at the end of the array
      lu = bts[0..-2]+[note]
  end
  set (":steps"+instruPos.to_s), lu
end

live_loop :remove_step do
  use_real_time
  osc = sync '/osc*/instru/step/remove'
  instruPos = osc[0]
  stepPos = osc[1]

  bts = get(':steps'+instruPos.to_s)
  case stepPos #check the new data position in the array
    when 0 # deals with new value at the beginning
      lu = [nil]+bts[1..-1]
    when 1..14 #deals with new value at position 1 to 14 (index from 0)
      lu = bts[0..(stepPos-1)] +[nil]+bts[(stepPos+1)..-1]
    when 15 #deals with new value at the end of the array
      lu = bts[0..-2]+[nil]
  end
  set (":steps"+instruPos.to_s), lu
end
