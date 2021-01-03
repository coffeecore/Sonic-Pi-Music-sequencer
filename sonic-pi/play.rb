live_loop :play do
  # use_real_time
  sync :t
  use_bpm get(:bpm)

  n = get(:n)
  p = get(:p)
  puts "N #{n}" if get(:debug)
  puts "P #{p}" if get(:debug)
  if p != nil then
    instrus = get(:instrus)[0..]
    puts "INSTRUS #{instrus}" if get(:debug)

    instrus.each do |instru|
      puts "INSTRU #{instru['name']}" if get(:debug)
      # puts "PPPPPPPP #{get(:p)}"
      steps = instru['steps'][p]
      puts "STEPS #{steps}" if get(:debug)

      if steps != nil && steps[n] != nil then
        opts = instru['opts'].to_h
        puts "OPTS #{opts}" if get(:debug)

        fxs = instru['fxs']
        puts "FXs #{fxs}" if get(:debug)

        instruName = instru['name']
        toEval = ''
        fxs.reverse.each do |fx|
          puts "FX #{fx}" if get(:debug)
          toEval += "with_fx :#{fx['name']}, #{fx['opts'].to_h} do "
        end
        case instru['type']
          when 'synth'
            opts[:note] = steps[n].to_sym
            # toEval += "synth instruName.to_sym "
            toEval += "synth instruName.to_sym, opts "
          when 'sample'
            toEval += "sample instruName.to_sym, opts "
            # toEval += "sample instruName.to_sym "
          when 'external_sample'
            toEval += "sample \"#{instruName}\", opts "
            # toEval += "sample \"#{instruName}\" "
        end

        fxs.reverse.each do |fx|
          toEval += "end "
        end
        puts "STRING #{toEval}" if get(:debug)
        puts "OPTS #{opts}" if get(:debug)
        eval toEval
      end
    end
  end
end

