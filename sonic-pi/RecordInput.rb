# Author Soxsa
# https://in-thread.sonic-pi.net/t/recording-phrases-from-the-keyboard/4911

#Midi keyboard phrase recorder
use_bpm 100
notes=[]
times=[]
t0=0.0
live_loop :rec do
  #stop
  use_real_time
  n,v=sync mhs_cue="/midi:mpk_mini_midi_1:*:*/"+"note_on"
  if tick==0
    t0=rt(vt)
  end
  notes.push n
  times.push (rt(vt)-t0)
  puts "x="+notes.to_s
  puts "y="+times.to_s
  play n, amp: 0.1
end

live_loop :beat do
  sample :perc_snap, amp: 0.1
  sleep 1
end
