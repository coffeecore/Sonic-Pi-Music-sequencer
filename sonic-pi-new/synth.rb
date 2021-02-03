# synthNumber = 0

define :play_synth do |i|
  n = (sync :n)[0]
  i[:opts][:note] = i[:patterns][n]
  i[:opts][:note] = eval(i[:opts][:note].to_s) if i[:opts][:note] != nil

  synth i[:synth].to_sym, i[:opts] if i[:opts][:note] != nil
end

define :create_loop_synth do |instru|
  name = instru[:name]
  live_loop name.to_sym do
    use_bpm get :bpm
    s = ""
    instru[:fxs].each do |key, value|
      value[:reps] = (get(:bar)*get(:eighth))
      s += "with_fx :#{key}, #{value} do \n"
    end

    s += "play_synth instru \n"

    instru[:fxs].each do |key, value|
      s += "end \n"
    end

    eval s
  end
end
