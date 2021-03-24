FILE_PATH     = "/Users/antoine/Music/Sonic Pi"
CHANNELS_PATH = '/Users/antoine/Music/Sonic Pi/.data'
STATE = (map stop: 0, play: 1, pause: 2)

use_debug false
use_cue_logging false

set :bpm, 60
set :bar, 4
set :pmax, 1
set :state, STATE[:play]


channels = []

live_loop :set_settings do
  name, value = sync "/osc*/settings"
  case name
  when 'volume'
    set_volume! value
  when 'state'
    set :state, STATE[value.to_sym]
  else
    set name.to_sym, value
  end
end

live_loop :kill_loop do
  name, = sync "/osc*/kill"
  live_loop (name).to_sym do
    stop
  end
end

# live_loop :channel_from_json_file do
#   channel, = sync "/osc*/channel/json/file"
#   filepath = CHANNELS_PATH+"/channel_#{channel}.json"
#   if Pathname.new(filepath).exist? then
#     content = File.read(filepath)
#     content = JSON.parse(content, :symbolize_names => true)
#     create_loop channel, content
#   end
# end

live_loop :channel_from_json do
  channel, json = sync "/osc*/channel/json"
  instru        = JSON.parse(json, :symbolize_names => true)
  create_loop channel, instru
  set "channel_#{channel}".to_sym, instru
  # filepath = CHANNELS_PATH+"/channel_#{channel}.json"
  # File.write(filepath, json)
end

live_loop :channel_play do
  use_real_time
  channel, note = sync "/osc*/channel/play"
  instru = get "channel_#{channel}".to_sym
  synth instru[:name].to_sym, instru[:default_step_options].to_h.merge({:note => note}) if instru[:type] == 'synth'
  sample instru[:name], instru[:default_step_options].to_h if instru[:type] == 'sample' or instru[:type] == 'external_sample'
end

# live_loop :channel_options do
#   name, json = sync "/osc*/channel/options"
#   with_arg_checks false do
#     control (get (name+"_opts").to_sym), JSON.parse(json, :symbolize_names => true)
#   end
# end

# live_loop :channel_fxs do
#   name, fx, json = sync "/osc*/channel/fxs"
#   control (get (name+"_fxs_"+fx).to_sym), JSON.parse(json, :symbolize_names => true)
# end

define :create_loop do |p, i|
  name = "#{i[:type]}_#{p}"
  fxs_name = i[:fxs].keys
  live_loop name.to_sym do
    use_bpm get(:bpm)
    psync, = sync :p
    create_fx(i, name, 0, fxs_name, psync)
  end
end

define :create_fx do |i, name, fx_index, fxs_name, psync|
  if fxs_name.length == 0 or fx_index >= fxs_name.length then
    send("play_#{i[:type]}", i, name, psync)
    # end
    # if fx_index < fxs_name.length then
  else
    with_fx fxs_name[fx_index], i[:fxs][fxs_name[fx_index]] do
      fx_index = fx_index + 1
      create_fx(i, name, fx_index, fxs_name, psync)
    end
  end
end

define :play_synth do |i, name, p|
  if i[:patterns][p] != nil then
    i[:patterns][p].length.times do
      sleepN = i[:sleeps][p].tick
      step   = i[:patterns][p].look
      if step != nil then
        # set (name+"_opts").to_sym, (synth i[:name].to_sym, step)
        synth i[:name].to_sym, i[:default_step_options].merge(step)
      end
      sleep sleepN
    end
  end
end

define :play_external_sample do |i, name, p|
  if i[:patterns][p] != nil then
    i[:patterns][p].length.times do
      sleepN = i[:sleeps][p].tick
      step   = i[:patterns][p].look
      if step != nil then
        # set (name+"_opts").to_sym, (sample i[:name].to_sym, step)
        sample i[:name], i[:default_step_options].merge(step)
      end
      sleep sleepN
    end
  end
end

define :play_sample do |i, name, p|
  if i[:patterns][p] != nil then
    i[:patterns][p].length.times do
      sleepN = i[:sleeps][p].tick
      step   = i[:patterns][p].look
      if step != nil then
        # set (name+"_opts").to_sym, (sample i[:name].to_sym, step)
        sample i[:name].to_sym, i[:default_step_options].merge(step)
      end
      sleep sleepN
    end
  end
end

live_loop :metronome do
  use_real_time
  while get(:state) != STATE[:play]
    use_bpm get(:bpm)
    if get(:state) == STATE[:stop] then
      tick_reset
      tick
      set :state, STATE[:pause]
    end
    sleep 1
  end
  use_bpm get(:bpm)
  l = look
  tick
  cue :p, l
  if look > (get(:pmax)-1) then
    tick_reset
    tick
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
