# synths_paths = FILE_PATH+"/synths/SonicPiSuperColliderSynthDefs"
# puts synths_paths
# load_synthdefs synths_paths
# load_synthdefs "/Users/antoine/Music/Sonic Pi/synths/SonicPiSuperColliderSynthDefs"

live_loop :play do
  use_real_time
  use_debug get(:debug)
  use_cue_logging get(:cue_logging)
  # sync :temp
  use_bpm get(:bpm)
  while PLAY_STATE[get(:play_state).to_i] != 'play' do
    sleep (1.0/get(:eighth))
  end

  n = get(:n)
  p = get(:p)
  puts "N #{n}" if get(:debug)
  puts "P #{p}" if get(:debug)
  if p != nil then
    instrus = get(:instrus)[0..]
    puts "INSTRUS #{instrus}" if get(:debug)

    instrus.each do |instru|
      puts "INSTRU #{instru['name']}" if get(:debug)

      patterns = instru['patterns'][p]
      puts "PATTERNS #{patterns}" if get(:debug)

      if patterns != nil && patterns[n] != nil then
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
            opts[:note] = eval(patterns[n].to_s)
            # toEval += "synth instruName.to_sym "
            toEval += "synth instruName.to_sym, opts "
          when 'external_synth'
            opts[:note] = patterns[n].to_sym
            # toEval += "synth instruName.to_sym "
            # toEval += "synth \"#{instruName}\", opts "
            toEval += "load_synthdefs \"/Users/antoine/Music/Sonic Pi/synths/SonicPiSuperColliderSynthDefs\" \n"
            toEval += "use_synth \"#{instruName}\" \n play 60"
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

  if SEQUENCER_MOD[get(:sequencer_mod).to_i] != 'single' then
    p = p+1 if n >= get(:endBar)
    p = 0 if p >= get(:pmax)
    set :p, p
  end
  
  sleep (1.0/get(:eighth))
end

