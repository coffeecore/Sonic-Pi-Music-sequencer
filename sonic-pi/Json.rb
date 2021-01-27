live_loop :add_instru do
  use_real_time

  osc        = sync '/osc*/instru/add/complete'
  instrus     = JSON.parse osc[0]

  set(:instrus, instrus)
end
