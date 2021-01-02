live_loop :add_instru do
  use_real_time
  osc        = sync '/osc*/instru/add'
  instruType = osc[0]
  instruName = osc[1]

  instrus = get(:instrus)[0..]

  instrus.push({
    'type' => instruType,
    'name' => instruName,
    'opts' => {},
    'fxs' => [],
    'steps' => Array.new(get(:end)+1)
  })

  set(:instrus, instrus)

  # osc "/instru/add", instrus.length-1
end

live_loop :add_instru_complete do
  use_real_time
  osc        = sync '/osc*/instru/add/complete'
  instru     = JSON.parse osc[0]

  instrus = get(:instrus)[0..]

  instrus.push(instru)

  set(:instrus, instrus)
end

live_loop :change_instru_complete do
  use_real_time
  osc        = sync '/osc*/instru/change/complete'
  instru     = JSON.parse osc[0]
  position   = osc[1]

  instrus = get(:instrus)[0..]

  instrus[position] = instru

  set(:instrus, instrus)
end

live_loop :remove_instru do
  use_real_time
  osc       = sync '/osc*/instru/remove'
  instruPos = osc[0]

  instrus = get(:instrus)[0..]

  instrus.delete_at(instruPos)

  set(:instrus, instrus)
end


live_loop :change_instru do
  use_real_time
  osc        = sync '/osc*/instru/change'
  instruType = osc[0]
  instruPos  = osc[1]
  instruName = osc[2]

  instrus = get(:instrus)[0..]
  instru  = (instrus[instruPos]).to_h

  instru['type'] = instruType
  instru['name'] = instruName

  instrus[instruPos] = instru

  set(:instrus, instrus)
end

live_loop :change_instru_options do
  use_real_time
  osc       = sync '/osc*/instru/options/change'
  instruPos = osc[0]
  options   = osc[1..]

  instrus = get(:instrus)[0..]
  instru  = (instrus[instruPos]).to_h

  opts = instru['opts'].to_h

  options.each_with_index do |v, i|
    if i % 2 == 0 then
      opts[v.to_sym] = options[i+1]
    end
  end

  instru['opts'] = opts

  instrus[instruPos] = instru
  set(:instrus, instrus)
end

live_loop :remove_instru_options do
  use_real_time
  osc       = sync '/osc*/instru/options/remove'
  instruPos = osc[0]
  options   = osc[1..]

  instrus = get(:instrus)[0..]
  instru  = (instrus[instruPos]).to_h

  opts = instru['opts'].to_h

  options.each_with_index do |v, i|
    opts.except!(v.to_sym)
  end

  instru['opts'] = opts

  instrus[instruPos] = instru
  set(:instrus, instrus)
end

live_loop :remove_all_instru_options do
  use_real_time
  osc       = sync '/osc*/instru/options/remove/all'
  instruPos = osc[0]

  instrus = get(:instrus)[0..]
  instru  = (instrus[instruPos]).to_h

  instru['opts'] = {}

  instrus[instruPos] = instru
  set(:instrus, instrus)
end
