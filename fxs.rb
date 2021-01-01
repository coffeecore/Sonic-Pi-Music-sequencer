live_loop :add_fx do
  use_real_time
  osc = sync "/osc*/instru/fx/add"
  instruPos = osc[0] # Synth index
  fxPosition   = osc[1] # FX position
  fxName   = osc[2] # FX name
  fxOpts = osc[3..] # FX Options

  instrus = get(:instrus).to_h
  instru = (instrus[instruPos]).to_h

  fxs = instru[:fxs].to_h
  fxs[fxPosition] = {'name': fxName, 'opts': {}}
  fxOpts.each_with_index do |v, i|
    if i % 2 == 0 then
      fxs[fxPosition][:opts][v.to_sym] = fxOpts[i+1]
    end
  end

  instru[:fxs] = fxs

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

  fxs = instru[:fxs].to_h

  fxOpts.each_with_index do |v, i|
    fxs.except!(v)
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

  instru[:fxs] = {}

  instrus[instruPos] = instru
  set(:instrus, instrus)
end
