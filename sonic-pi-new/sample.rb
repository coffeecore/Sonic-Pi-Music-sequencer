sampleNumber = 0

define :play_sample do |i|
  n = (sync :n)[0]

  sample i[:name].to_sym, i[:opts] if i[:patterns][n] != nil
end

define :create_loop_sample do |instru|
  name = instru[:name]
  live_loop name.to_sym do
    puts get((name+"_state").to_sym)
    use_bpm get :bpm
    s = ""
    instru[:fxs].each do |key, value|
      s += "with_fx :#{key}, #{value} do \n"
    end

    s += "play_sample instru \n"

    instru[:fxs].each do |key, value|
      s += "end \n"
    end

    eval s
  end
end
