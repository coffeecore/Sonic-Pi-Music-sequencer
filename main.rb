FILE_PATH = "/Users/antoine/Music/Sonic Pi"
STATE = (map stop: 0, play: 1, pause: 2)

use_debug false
use_cue_logging false

set :bpm, 60
set :eighth, 4
set :bar, 1
set :pmax, 4
set :state, STATE[:pause]

set :sleep, 1.0/get(:eighth)
set_volume! 5

live_loop :set_volume do
  osc = sync "/osc*/volume"
  set_volume! osc[0]
end

live_loop :set_settings do
  osc = sync "/osc*/settings"
  set osc[0].to_sym, osc[1]
  set :sleep, 1.0/get(:eighth)
end

live_loop :set_state do
  osc = sync "/osc*/state"
  state = get(:state)
  set :state, STATE[osc[0].to_sym]
end

live_loop :kill_loop do
  osc = sync "/osc*/kill"
  live_loop (osc[0]).to_sym do
    stop
  end
end

live_loop :patterns do
  osc = sync "/osc*/patterns"
  instrus     = JSON.parse(osc[0], :symbolize_names => true)
  instrus.each_with_index do |i, p|
    create_loop p, i
  end
end

live_loop :pattern do
  osc = sync "/osc*/pattern"
  position = osc[0]
  instru     = JSON.parse(osc[1], :symbolize_names => true)
  create_loop position, instru
end

define :create_loop do |p, i|
  name = "#{i[:type]}_#{p}"
  live_loop name.to_sym do
    use_bpm get(:bpm)
    s = ""
    i[:fxs].each do |key, value|
      # value[:reps] = get(:pmax)
      s += "with_fx :#{key}, #{value} do \n"
    end
        s += "play_#{i[:type]} i \n"
    i[:fxs].each do |key, value|
      s += "end \n"
    end
    eval s
  end
end

define :play_synth do |i|
  p = (sync :p)[0]
  puts "PPP #{p}"
  in_thread do
    i[:patterns][p].length.times do
    i[:opts][:note] = i[:patterns][p][tick]
    if i[:opts][:note] != nil then
      i[:opts][:note] = eval(i[:opts][:note].to_s)
      puts "Synth #{p} #{i[:synth]} #{i[:opts][:note]}"
      synth i[:synth].to_sym, i[:opts]
    end
    sleep get(:sleep)
  end
end
end

define :play_external_sample do |i|
  p = (sync :p)[0]
  in_thread do
    i[:patterns][p].length.times do
  if i[:patterns][p][tick] == true then
    puts "Ext sample #{p} #{i[:sample]}"
    sample i[:sample], i[:opts]
  end
  sleep get(:sleep)
end
end
end

define :play_sample do |i|
  p = (sync :p)[0]
  in_thread do
    i[:patterns][p].length.times do
  if i[:patterns][p][tick] == true then
    puts "Sample #{p} #{i[:sample]}"
    sample i[:sample].to_sym, i[:opts]
  end
  sleep get(:sleep)
end
end
end




live_loop :metronome do
  use_real_time
  use_bpm get(:bpm)
  while get(:state) != STATE[:play]
    # if get(:state) == STATE[:stop] then
    #   tick_reset
    #   set :state, STATE[:pause]
    # end
    sleep get(:bar)
  end
  l = tick
  cue :p, l
  if look == (get(:pmax)-1) then
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
