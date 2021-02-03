# externalSampleNumber = 0

define :play_external_sample do |i|
  n = (sync :n)[0]

  sample i[:sample], i[:opts] if i[:patterns][n] != nil
end
define :create_loop_external_sample do |instru|
  name = instru[:name]
  live_loop name.to_sym do
    use_bpm get :bpm
    s = ""
    instru[:fxs].each do |key, value|
      value[:reps] = get(:max)

      s += "with_fx :#{key}, #{value} do \n"
    end

    s += "play_external_sample instru \n"

    instru[:fxs].each do |key, value|
      s += "end \n"
    end

    eval s
  end
end
