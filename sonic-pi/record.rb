#https://in-thread.sonic-pi.net/t/recording-is-not-happening-with-osc-commands/4710/6
# Author robin.newman
#This program lets you find the current server Listen port,
#where the Sonic Pi server listens to command from the GUI front end
#It also demonstrates how to setup a Stop All command
#and how to send code to run on Sonic Pi
#developed by Robin Newman, August 2019

#WARNING this uses undocumented features in Sonic Pi which MAY CHANGE
#and it is not guaranteed to work with future versions of Sonic Pi

define :pvalue do #get current listen port for Sonic Pi from log file
  value= 4557 #pre new logfile format port was always 4557
  File.open(ENV['HOME']+'/.sonic-pi/log/server-output.log','r') do |f1|
    while l = f1.gets
      if l.include?"Listen port:"
        value = l.split(" ").last.to_i
        break
      end
    end
    f1.close
  end
  return value
end
puts "Server Listen port is: #{pvalue}"
set :pvalue,pvalue
#three functions with will start recording, stop recording and save recorded audio file
define :recordStart do #this command is equivalent to pushing the start recording button
  use_real_time
  pvalue=get(:pvalue)
  osc_send "localhost",pvalue, "/start-recording","guid-rbn"
  sleep 1# make sure recording running before creating any audio to save
  puts "recording started"
end
define :recordStop do #this command stops a currently recording process
  use_real_time
  pvalue=get(:pvalue)
  osc_send "localhost",pvalue, "/stop-recording","guid-rbn"
end
define :saveAudio do |file|  #this command saves the recorded audio file
  pvalue=get(:pvalue)
  osc_send "localhost",pvalue, "/save-recording","guid-rbn",file
  puts "recording stopped"
end
#combine stop and save functions
define :stopAndSaveRecording do |file|
  recordStop
  saveAudio(file)
  puts "Recording saved to #{file}"
end


#test recording
recordStart
#play some audio
use_synth :tb303
24.times do
  play scale(:c4,:minor_pentatonic,num_octaves: 2).choose,release: 0.2,cutoff: 70
  sleep 0.2
end
sample :loop_amen
sleep sample_duration :loop_amen #wait till finished
#adjust path/name to suit your own location
stopAndSaveRecording("/Users/rbn/testfile.avi")
