live_loop :json do
  use_real_time

  osc        = sync '/osc*/json'
  instrus     = JSON.parse osc[0]

  set(:instrus, instrus)
end
