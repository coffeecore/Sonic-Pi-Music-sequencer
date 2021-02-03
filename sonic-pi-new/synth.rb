define :play_synth do |i|
  n = (sync :n)[0]
  i[:opts][:note] = i[:patterns][n]
  if i[:opts][:note] != nil then
    i[:opts][:note] = eval(i[:opts][:note].to_s)
    synth i[:synth].to_sym, i[:opts]
  end
end

define :create_loop_synth do |position, instru|
  name = "#{instru[:type]}_#{position}"
  live_loop name.to_sym do
    use_bpm get(:bpm)
    s = ""
    instru[:fxs].each do |key, value|
      value[:reps] = get(:max)
      s += "with_fx :#{key}, #{value} do \n"
    end

    s += "play_synth instru \n"

    instru[:fxs].each do |key, value|
      s += "end \n"
    end

    eval s
  end
end
