FILE_PATH = "/Users/antoine/Music/Sonic Pi"
STATE = (map stop: 0, play: 1, pause: 2)

use_debug false
use_cue_logging false

set :bpm, 60
set :eighth, 4
set :bar, 4
set :pmax, 1
set :state, STATE[:stop]

# set :sleep, (1.0/get(:eighth))
set_volume! 5

live_loop :set_settings do
  name, value = sync "/osc*/settings"
  if name == 'volume' then
    set_volume! value
  else
    set name.to_sym, value
    # set :sleep, (1.0/get(:eighth))
  end
end

live_loop :set_state do
  stateName, = sync "/osc*/state"
  state = get(:state)
  set :state, STATE[stateName.to_sym]
end

live_loop :kill_loop do
  name, = sync "/osc*/kill"
  live_loop (name).to_sym do
    stop
  end
end

live_loop :channels do
  json, = sync "/osc*/channels"
  instrus     = JSON.parse(json, :symbolize_names => true)
  instrus.each_with_index do |i, p|
    create_loop p, i
  end
end

live_loop :channel do
  position, json = sync "/osc*/channel"
  instru     = JSON.parse(json, :symbolize_names => true)
  create_loop position, instru
end

live_loop :channel_options do 
  name, json = sync "/osc*/channel/options"
  with_arg_checks false do
    control (get (name+"_opts").to_sym), JSON.parse(json, :symbolize_names => true)
  end
end

live_loop :channel_fxs do
  name, fx, json = sync "/osc*/channel/fxs"
  control (get (name+"_fxs_"+fx).to_sym), JSON.parse(json, :symbolize_names => true)
end

define :create_loop do |p, i|
  name = "#{i[:type]}_#{p}"
  live_loop name.to_sym do
    use_bpm get(:bpm)
    s = ""
    i[:fxs].each do |key, value|
      s += "with_fx :#{key}, #{value} do |f_#{key}| \n"
      s += "set :#{name}_fxs_#{key}, f_#{key} \n"
    end
    s += "play_#{i[:type]} i, name \n"
    i[:fxs].each do |key, value|
      s += "end \n"
    end
    eval s
  end
end

define :play_synth do |i, name|
  p = (sync :p)[0]
  in_thread do
    i[:patterns][p].length.times do
      sleepN = i[:steps][p].look
      step = i[:patterns][p].tick
      if step != nil then
        note = eval(step[:n].to_s)
        step[:note] = note
        set (name+"_opts").to_sym, (synth i[:name].to_sym, step)
      end
      sleep sleepN
    end
  end
end

define :play_external_sample do |i, name|
  p = (sync :p)[0]
  in_thread do
    i[:patterns][p].length.times do
      sleepN = i[:patterns][p].look
      step = i[:patterns][p].tick
      if step != nil then
        set (name+"_opts").to_sym, (synth i[:name].to_sym, step)
      end
      sleep sleepN
    end
  end
end

define :play_sample do |i, name|
  p = (sync :p)[0]
  in_thread do
    i[:patterns][p].length.times do
      sleepN = i[:steps][p].look
      step = i[:patterns][p].tick
      if step != nil then
        set (name+"_opts").to_sym, (synth i[:name].to_sym, step)
      end
      sleep sleepN
    end
  end
end

live_loop :metronome do
  # use_real_time
  use_bpm get(:bpm)
  while get(:state) != STATE[:play]
    if get(:state) == STATE[:stop] then
      tick_reset
      tick # you must tick to avoid repeat first pattern
      set :state, STATE[:pause]
    end
    sleep 1
  end
  l = look
  tick
  cue :p, l
  if look > (get(:pmax)-1) then
    tick_reset
  end
  sleep get(:bar)
end





##
# RECORD #
##
# Author : robin.newman
# URI : https://in-thread.sonic-pi.net/t/recording-is-not-happening-with-osc-commands/4710/6

# define :port_value do #get current listen port for Sonic Pi from log file
#   value = 51243 #pre new logfile format port was always 4557
#   File.open(ENV['HOME']+'/.sonic-pi/log/server-output.log','r') do |f1|
#     while l = f1.gets
#       if l.include?"Listen port:"
#         value = l.split(" ").last.to_i
#         break
#       end
#     end
#     f1.close
#   end
#   puts "Port record #{value}"
#   return value
# end
# set :pvalue, port_value
# set :record, false

# define :record_start do # This command is equivalent to pushing the start recording button
#   use_real_time
#   pvalue = get(:pvalue)
#   osc_send "localhost", pvalue, "/start-recording","guid-rbn"
#   sleep 1 # Make sure recording running before creating any audio to save
# end

# define :record_stop do # This command stops a currently recording process
#   use_real_time
#   pvalue = get(:pvalue)
#   osc_send "localhost", pvalue, "/stop-recording","guid-rbn"
# end

# define :save_audio do |file|  # This command saves the recorded audio file
#   pvalue = get(:pvalue)
#   osc_send "localhost", pvalue, "/save-recording","guid-rbn",file
# end


# live_loop :start_record do
#     # use_real_time
#     osc = sync '/osc*/record/start'
#     puts "Record starting..."
#     record_start()
#     puts "Record started"
# end

# live_loop :stop_record do
#     # use_real_time
#     osc = sync '/osc*/record/stop'
#     puts "Record stoping..."
#     record_stop()
#     puts "Record stopped"
# end

# live_loop :save_record_audio_file do
#     # use_real_time
#     osc = sync '/osc*/record/save'
#     puts "Record saving..."
#     sleep 1
#     save_audio(FILE_PATH+'/records/'+(Time.new).strftime("%Y%m%d_%H%M%S")+'.wav')
#     puts "Record saved"
#     stop
# end
