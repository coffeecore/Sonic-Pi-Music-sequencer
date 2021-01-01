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
    beats = get(':beats'+i.to_s)
    puts "BEATS #{beats}" if get(:debug)
      if beats != nil then
      opts = s[:opts].to_h
      puts "OPTS #{opts}" if get(:debug)
      fxs = s[:fxs].to_h
      if beats[n] != nil then
        opts[:note] = beats[n]
        instru = s[:name]
        string = ''
        fxs.each_with_index do |f, ii|
          string += "with_fx :#{fxs[ii][:name]}, #{fxs[ii][:opts]}.to_h do "
        end
        case s[:type]
          when 'synth'
            string += "synth instru.to_sym, opts "
          when 'sample'
            string += "sample instru.to_sym, opts "
        end

        fxs.each_with_index do |f, ii|
          string += "end "
        end
        puts "STRING #{string}" if get(:debug)
        eval string
      end
    end
  end
  ##| sleep (1.0/get(:eighth))
end

