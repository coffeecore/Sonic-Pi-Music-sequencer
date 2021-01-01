live_loop :play do
  use_real_time
  sync :t
  use_bpm get(:bpm)

  n = get(:n)
  puts "N #{n}" if get(:debug)

  instrus = get(:instrus).to_h
  puts "INSTRUS #{instrus}" if get(:debug)
  instrus.each do |i, s|
    puts "INSTRU #{s[:name]}" if get(:debug)
    steps = get(':steps'+i.to_s)
    puts "BEATS #{steps}" if get(:debug)
      if steps != nil then
      opts = s[:opts].to_h
      puts "OPTS #{opts}" if get(:debug)
      fxs = s[:fxs]
      if steps[n] != nil then
        opts[:note] = steps[n]
        instru = s[:name]
        string = ''
        fxs.reverse.each_with_index do |f, ii|
          string += "with_fx :#{fxs[ii][:name]}, #{fxs[ii][:opts]}.to_h do "
        end
        case s[:type]
          when 'synth'
            string += "synth instru.to_sym, opts "
          when 'sample'
            string += "sample instru.to_sym, opts "
        end

        fxs.reverse.each_with_index do |f, ii|
          string += "end "
        end
        puts "STRING #{string}" if get(:debug)
        eval string
      end
    end
  end
  ##| sleep (1.0/get(:eighth))
end

