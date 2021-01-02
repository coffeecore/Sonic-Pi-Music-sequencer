live_loop :play do
  # use_real_time
  sync :t
  use_bpm get(:bpm)

  n = get(:n)
  puts "N #{n}" if get(:debug)

  instrus = get(:instrus)[0..]

  puts "INSTRUS #{instrus}" if get(:debug)
  instrus.each do |instru|
    puts "INSTRU #{instru['name']}" if get(:debug)

    steps = instru['steps']
    puts "STEPS #{steps}" if get(:debug)

    if steps[n] != nil then
      opts = instru['opts'].to_h
      puts "OPTS #{opts}" if get(:debug)
      fxs = instru['fxs']

      opts['note'] = steps[n]
      instruName = instru['name']
      toEval = ''
      fxs.reverse.each do |fx|
        toEval += "with_fx :#{fx['name']}, #{fx['opts'].to_h} do "
      end
      case instru['type']
        when 'synth'
          toEval += "synth instruName.to_sym, opts "
        when 'sample'
          toEval += "sample instruName.to_sym, opts "
        when 'external_sample'
          toEval += "sample \"#{instruName}\", opts "
      end

      fxs.reverse.each do |fx|
        toEval += "end "
      end
      puts "STRING #{toEval}" if get(:debug)
      eval toEval
    end
  end
  ##| sleep (1.0/get(:eighth))
end

