live_loop :add_fx do
  use_real_time
  osc       = sync "/osc*/instru/fx/add"
  instruPos = osc[0]
  fxName    = osc[1]
  # fxOpts    = osc[2..]
  fxOpts    = osc.drop(2)

  # instrus = get(:instrus)[0..]
  # instrus = get(:instrus).take(get(:instrus).length)
  instrus = get(:instrus).drop(0)
  instru  = (instrus[instruPos]).to_h

  # fxs = instru['fxs'][0..]
  fxs = instru['fxs'].take(get(:instrus).length)
  fx  = {'name' => fxName, 'opts' => {}}
  fxOpts.each_with_index do |v, i|
    if i % 2 == 0 then
      fx['opts'][v] = fxOpts[i+1]
    end
  end

  # instru['fxs'] = fxs.push(fx)
  instru['fxs'] = fxs+[fx]

  instrus[instruPos] = instru
  # instrus = instrus.take(instruPos)+[instru]+instrus.drop(instruPos+1)
  set(:instrus, instrus)
end

live_loop :change_options_fx do
  use_real_time
  osc        = sync '/osc*/instru/fx/change'
  instruPos  = osc[0]
  fxPosition = osc[1]
  # fxOpts     = osc[2..]
  fxOpts     = osc.drop(2)

  # instrus = get(:instrus)[0..]
  # instrus = get(:instrus).take(get(:instrus).length)
  instrus = get(:instrus).drop(0)
  instru  = (instrus[instruPos]).to_h

  # fxs = instru['fxs'][0..]
  fxs = instru['fxs'].take(instru['fxs'].length)
  fx  = fxs[fxPosition].to_h
  fxsOptions = fx['opts'].to_h
  fxOpts.each_with_index do |v, i|
    if i % 2 == 0 then
      fxsOptions[v] = fxOpts[i+1]
    end
  end

  fx['opts']       = fxsOptions
  fxs[fxPosition] = fx
  instru['fxs']    = fxs

  instrus[instruPos] = instru
  # instrus = instrus.take(instruPos)+[instru]+instrus.drop(instruPos+1)
  set(:instrus, instrus)
end

live_loop :remove_fx do
  use_real_time
  osc       = sync '/osc*/instru/fx/remove'
  instruPos = osc[0]
  # fxOpts    = osc[1..]
  fxOpts    = osc.drop(1)

  # instrus = get(:instrus)[0..]
  # instrus = get(:instrus).take(get(:instrus).length)
  instrus = get(:instrus).drop(0)
  instru  = (instrus[instruPos]).to_h

  # fxs = instru['fxs'][0..]
  fxs = instru['fxs'].take(instru['fxs'].length)

  fxOpts.each_with_index do |v, i|
    # fxs.delete_at(i)
    fxs = fxs.take(i)+fxs.drop(i+1)
  end

  instru['fxs'] = fxs

  instrus[instruPos] = instru
  # instrus = instrus.take(instruPos)+[instru]+instrus.drop(instruPos+1)
  set(:instrus, instrus)
end

live_loop :remove_all_fx do
  use_real_time
  osc       = sync '/osc*/instru/fx/remove/all'
  instruPos = osc[0]

  # instrus = get(:instrus)[0..]
  # instrus = get(:instrus).take(get(:instrus).length)
  instrus = get(:instrus).drop(0)
  instru  = (instrus[instruPos]).to_h

  instru['fxs'] = []
  puts instru
  instrus[instruPos] = instru

  # instrus = instrus.take(instruPos)+[instru]+instrus.drop(instruPos+1)
  set(:instrus, instrus)
end
