live_loop :play do
  use_real_time
  # use_debug get(:debug)
  # use_cue_logging get(:cue_logging)
  use_bpm get(:bpm)

  while PLAY_STATE[get(:play_state).to_i] != 'play' do
    sleep (1.0/get(:eighth))
  end

  n = get(:n)
  p = get(:p)

  puts "Pattern #{p}"
  puts "Step #{n}"

  if p != nil then
    # instrus = get(:instrus)[0..]
    # instrus = get(:instrus).take(get(:instrus).length)
    instrus = get(:instrus).drop(0)

    instrus.each do |instru|
      if instru['patterns'] != nil then
        patterns = instru['patterns'][p]

        if patterns != nil && patterns[n] != nil then
          opts = instru['opts'].to_h

          fxs = instru['fxs']

          instruName = instru['name']
          toEval = ''
          if fxs != nil then
            fxs.reverse.each do |fx|
              puts "#{fx['name']}"
              toEval += "with_fx :#{fx['name']}, #{fx['opts'].to_h} do \n"
            end
          end
          # puts patterns[n]
          case instru['type']
            when 'synth'
              opts[:note] = eval(patterns[n].to_s)
              toEval += "synth instruName.to_sym, opts \n"
            when 'external_synth'
              # opts[:note] = patterns[n].to_sym
              # toEval += "load_synthdefs \"/Users/antoine/Music/Sonic Pi/synths/SonicPiSuperColliderSynthDefs\" \n"
              # toEval += "use_synth \"#{instruName}\" \n play 60"
            when 'sample'
              toEval += "sample instruName.to_sym, opts \n"
            when 'external_sample'
              toEval += "sample \"#{instruName}\", opts \n"
          end

          fxs.reverse.each do |fx|
            toEval += "end "
          end
          # puts "EVAAAAAAAL #{toEval}"
          eval toEval
        end
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

