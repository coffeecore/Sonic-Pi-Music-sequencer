live_loop :json do
  use_real_time

  osc        = sync '/osc*/json'
  instrus     = JSON.parse osc[0]

  set(:instrus, instrus)
end

live_loop :json_by_channel do
    use_real_time

    osc = sync '/osc*/json/channel'
    channel = osc[0]
    json = JSON.parse osc[1]

    instrus = get(:instrus).drop(0)

    instrus[channel] = json

    set(:instrus, instrus)
end
