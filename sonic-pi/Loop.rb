live_loop :play do
  use_real_time
  use_bpm get(:bpm)

  while PLAY_STATE[get(:play_state).to_i] != 'play' do
    sleep (1.0/get(:eighth))
  end

  n = get(:n)
  p = get(:p)

  puts "Pattern #{p}"
  puts "Step #{n}"

  # if p != nil then
    instrus = get(:instrus).drop(0)
    puts instrus
    instrus.each do |instru|
        patterns = instru['patterns'][p]

        # if patterns[n] != nil then
          opts = instru['opts'].to_h

          fxs = instru['fxs']

          instruName = instru['name']
          toEval = ''
            fxs.to_h.each do |fxName, fxOpts|
              puts "#{fxName}"

              toEval += "with_fx #{fxName}, #{fxOpts.to_h} do \n"
            end
          case instru['type']
            when 'synth'
              opts[:note] = eval(patterns[n].to_s)
              toEval += "synth #{instruName}, opts \n"
            when 'external_synth'
            when 'sample'
              toEval += "sample #{instruName}, #{opts.to_h} \n"
            when 'external_sample'
              toEval += "sample \"#{instruName}\", #{opts.to_h} \n"

          end
            fxs.to_h.each do |fx|
              toEval += "end \n"
            end
          eval toEval
        # end
    end
  # end

  if SEQUENCER_MOD[get(:sequencer_mod).to_i] != 'single' then
    p = p+1 if n >= get(:endBar)
    p = 0 if p >= get(:pmax)
    set :p, p
  end

  sleep (1.0/get(:eighth))
end

