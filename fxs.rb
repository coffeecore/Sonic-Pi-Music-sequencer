live_loop :add_fx do
  use_real_time
  osc = sync "/osc*/instru/fx/add"
  instruPos = osc[0] # Synth index
  # fxPosition   = osc[1] # FX position
  fxName   = osc[1] # FX name
  fxOpts = osc[2..] # FX Options

  instrus = get(:instrus).to_h
  instru = (instrus[instruPos]).to_h

  fxs = instru[:fxs][0..]
  fx = {'name': fxName, 'opts': {}}
  fxOpts.each_with_index do |v, i|
    if i % 2 == 0 then
      fx[:opts][v.to_sym] = fxOpts[i+1]
    end
  end

  instru[:fxs] = fxs.push(fx)

  instrus[instruPos] = instru
  set(:instrus, instrus)
end

live_loop :remove_fx do
  use_real_time
  osc = sync '/osc*/instru/fx/remove'
  instruPos = osc[0]
  instrus = get(:instrus).to_h
  instru = (instrus[instruPos]).to_h
  fxOpts = osc[1..]

  fxs = instru[:fxs][0..]

  fxOpts.each_with_index do |v, i|
    fxs.delete_at(v)
  end

  instru[:fxs] = fxs

  instrus[instruPos] = instru
  set(:instrus, instrus)
end

live_loop :remove_all_fx do
  use_real_time
  osc = sync '/osc*/instru/fx/remove/all'
  instruPos = osc[0]
  instrus = get(:instrus).to_h
  instru = (instrus[instruPos]).to_h

  instru[:fxs] = []

  instrus[instruPos] = instru
  set(:instrus, instrus)
end
