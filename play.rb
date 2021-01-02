live_loop :play do
  use_real_time
  sync :t
  use_bpm get(:bpm)

  n = get(:n)
  puts "N #{n}" if get(:debug)

  instrus = get(:instrus)[0..]

  puts "INSTRUS #{instrus}" if get(:debug)
  instrus.each do |instru|
    # puts "SSSSS #{s['steps']}"
    # puts "IIIII #{i}"

    puts "INSTRU #{instru['name']}" if get(:debug)

    steps = instru['steps']
    puts "STEPS #{steps}" if get(:debug)

    if steps != nil then
      opts = instru['opts'].to_h
      puts "OPTS #{opts}" if get(:debug)
      fxs = instru['fxs']
      if steps[n] != nil then
        opts['note'] = steps[n]
        instruName = instru['name']
        to_eval = ''
        fxs.reverse.each do |fx|
          to_eval += "with_fx :#{fx['name']}, #{fx['opts'].to_h} do "
        end
        case instru['type']
          when 'synth'
            to_eval += "synth instruName.to_sym, opts "
          when 'sample'
            to_eval += "sample instruName.to_sym, opts "
          when 'external_sample'
            to_eval += "sample \"#{instruName}\", opts "
        end

        fxs.reverse.each do |fx|
          to_eval += "end "
        end
        puts "STRING #{to_eval}" if get(:debug)
        eval to_eval
      end
    end
  end
  ##| sleep (1.0/get(:eighth))
end

