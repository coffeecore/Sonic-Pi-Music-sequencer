FILE_PATH     = "/Users/antoine/Music/Sonic Pi"
STATE = (map stop: 0, play: 1, pause: 2)

use_debug true
use_cue_logging true

set :bpm, 60
set :bar, 4
set :pmax, 1
set :state, STATE[:play]

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

live_loop :channel_from_json do
  channel, json = sync "/osc*/channel/json"
  instru        = MultiJson.load(json, :symbolize_keys => true)
  create_loop channel, instru
  set "channel_#{channel}".to_sym, instru
end




# PLAY
live_loop :channel_play_on do
  use_real_time
  use_bpm get(:bpm)
  channel, note, with_opts, with_fxs = sync "/osc*/channel/play/on"
  instru = get "channel_#{channel}".to_sym
  create_fx_channel_play(channel, instru, note, 0, instru[:fxs].keys, with_fxs, with_opts)
end

live_loop :channel_play_off do
  use_real_time
  use_bpm get(:bpm)
  channel, note = sync "/osc*/channel/play/off"
  a = get "play_on_#{channel}_#{note}".to_sym
  if a != nil then
    a.kill
  end
end

live_loop :channel_play_control do
  use_real_time
  channel, note, json = sync "/osc*/channel/play/control"
  options        = MultiJson.load(json, :symbolize_keys => true)
  control (get "play_on_#{channel}_#{note}".to_sym), options
end

live_loop :channel_play do
  use_real_time
  use_bpm get(:bpm)
  channel, note, with_fxs, with_opts = sync "/osc*/channel/play"
  instru = get "channel_#{channel}".to_sym
  create_fx_channel_play(channel, instru, note, 0, instru[:fxs].keys, with_fxs, with_opts)
end

define :create_fx_channel_play do |channel, instru, note, fx_index, fxs_name, with_fxs, with_opts|
  if with_fxs == false and with_fxs != nil then
    is_with_opts(instru[:type], instru[:name], "#{channel}_#{note}", note, instru[:options], with_opts) if instru[:type] == 'synth'
    is_with_opts(instru[:type], instru[:name], "#{channel}_#{note}", note, instru[:options], with_opts) if instru[:type] == 'sample' or instru[:type] == 'external_sample'
  elsif fxs_name.length == 0 or fx_index >= fxs_name.length then
    is_with_opts(instru[:type], instru[:name], "#{channel}_#{note}", note, instru[:options], with_opts) if instru[:type] == 'synth'
    is_with_opts(instru[:type], instru[:name], "#{channel}_#{note}", note, instru[:options], with_opts) if instru[:type] == 'sample' or instru[:type] == 'external_sample'
  else
    with_fx (fxs_name[fx_index]).to_sym, instru[:fxs][fxs_name[fx_index]].to_h do
      fx_index = fx_index + 1
      create_fx_channel_play(channel, instru, note, fx_index, fxs_name, with_fxs, with_opts)
    end
  end
end

define :is_with_opts do |type, name, slug, note, options, with_opts|
  if with_opts == false and with_opts != nil then
    channel_play_once(type, name, slug, {:note => note}) if type == 'synth'
    channel_play_once(type, name, slug) if type == 'sample' or type == 'external_sample'
  else
    channel_play_once(type, name, slug, options.to_h.merge({:note => note})) if type == 'synth'
    channel_play_once(type, name, slug, options.to_h) if type == 'sample' or type == 'external_sample'
  end
end

define :channel_play_once do |type, name, slug, options|
  if options.length != 0 then
    s = synth name.to_sym, options if type == 'synth'
    s = sample name, options.to_h if type == 'sample' or type == 'external_sample'
    set "play_on_#{slug}".to_sym, s
  else
    s = synth name.to_sym if type == 'synth'
    s = sample name if type == 'sample' or type == 'external_sample'
    set "play_on_#{slug}".to_sym, s
  end
end




# SEQUENCER
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
  else
    with_fx fxs_name[fx_index].to_sym, i[:fxs][fxs_name[fx_index]].to_h do
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
        synth i[:name].to_sym, i[:options].merge(step)
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
        sample i[:name], i[:options].merge(step)
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
        sample i[:name].to_sym, i[:options].merge(step)
      end
      sleep sleepN
    end
  end
end




# METRONOME
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
