# Author : robin.newman
# URI : https://in-thread.sonic-pi.net/t/recording-is-not-happening-with-osc-commands/4710/6

define :pvalue do #get current listen port for Sonic Pi from log file
  value = 51243 #pre new logfile format port was always 4557
  File.open(ENV['HOME']+'/.sonic-pi/log/server-output.log','r') do |f1|
    while l = f1.gets
      if l.include?"Listen port:"
        value = l.split(" ").last.to_i
        break
      end
    end
    f1.close
  end
  puts "PORt #{value}"
  return value
end
set :pvalue, pvalue

define :recordStart do #this command is equivalent to pushing the start recording button
  use_real_time
  pvalue = get(:pvalue)
  osc_send "localhost", pvalue, "/start-recording","guid-rbn"

  sleep 1# make sure recording running before creating any audio to save
end

define :recordStop do #this command stops a currently recording process
  use_real_time
  pvalue = get(:pvalue)
  osc_send "localhost", pvalue, "/stop-recording","guid-rbn"
end

define :saveAudio do |file|  #this command saves the recorded audio file
  pvalue = get(:pvalue)
  osc_send "localhost", pvalue, "/save-recording","guid-rbn",file
end


live_loop :start_record do
    use_real_time
    use_cue_logging get(:cue_logging)
    use_debug get(:debug)
    osc = sync '/osc*/record/start'

    recordStart()
end

live_loop :stop_record do
    use_real_time
    use_cue_logging get(:cue_logging)
    use_debug get(:debug)
    osc = sync '/osc*/record/stop'
    recordStop()
end

live_loop :save_record_audio_file do
    use_real_time
    use_cue_logging get(:cue_logging)
    use_debug get(:debug)
    osc = sync '/osc*/record/save'

    sleep 1
    saveAudio(FILE_PATH+'/records/'+(Time.new).strftime("%Y%m%d_%H%M%S")+'.wav')

    stop
end
