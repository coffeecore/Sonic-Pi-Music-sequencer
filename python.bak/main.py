from Machine import Machine
from Channel import Channel
from PianoHat import PianoHat

from pythonosc import osc_message_builder
from pythonosc import udp_client
import time
import json
import sys
import random

from os import walk

# dark_mist = Machine()
# dark_mist.bar = 4
# dark_mist.pmax = 2
# print(dark_mist.SAMPLES_FOLDER)
# f = {}
# def samples_recursive_dir(dirnames):
#     if len(dirnames) != 0:
#         for dirname in dirnames:
#             for (dirpath_child, dirnames_child, filenames_child) in walk(dark_mist.SAMPLES_FOLDER+'/'+dirname):
#                 if f.get(dirpath_child.split('/')[-2:][0]) == None:
#                     f[(dirpath_child.split('/')[-2:][0])] = {}
#                 if len(filenames_child) != 0:
#                     f[(dirpath_child.split('/')[-2:][0])][(dirpath_child.split('/')[-1:][0])] = filenames_child
#                 samples_recursive_dir(dirnames_child)

# for (dirpath, dirnames, filenames) in walk(dark_mist.SAMPLES_FOLDER):
#     samples_recursive_dir(dirnames)

# print(f)
# exit()

sender = udp_client.SimpleUDPClient('127.0.0.1', 4560)
# sender.send_message('/settings', ['bpm', dark_mist.bpm])
# sender.send_message('/settings', ['bar', dark_mist.bar])
# sender.send_message('/settings', ['pmax', dark_mist.pmax])

# prophet_channel = Channel('synth', 'prophet')
# prophet_channel.bar = dark_mist.bar
# prophet_channel.add_fx('slicer')
# prophet_channel.add_fx_option('slicer', 'probability', 0.7)
# prophet_channel.add_fx_option('slicer', 'prob_pos', 1)
# prophet_channel.add_step(0, 0, 4, {"note": ":e1", "release": 8, "cutoff": 70})
# prophet_channel.add_step(0, 1, 4, {"note": ":f1", "release": 8, "cutoff": 70})
# dark_mist.add_channel(prophet_channel)

# guit_channel = Channel('sample', 'guit_em9')
# guit_channel.bar = dark_mist.bar
# guit_channel.add_fx('slicer')
# guit_channel.add_fx_option('slicer', 'phase', 0.125)
# guit_channel.add_step(0, 0, 4, {"rate": 0.5})
# dark_mist.add_channel(guit_channel)

# mika_channel = Channel('sample', 'loop_mika')
# mika_channel.bar = dark_mist.bar
# mika_channel.add_fx('slicer')
# mika_channel.add_fx_option('slicer', 'phase', 0.25)
# mika_channel.add_fx_option('slicer', 'wave', 0)
# mika_channel.add_step(0, 0, 4, {"rate": 0.5})
# dark_mist.add_channel(mika_channel)


# dark_mist.state = 'play'
# sender.send_message('/settings', ['state', dark_mist.state])
# sender.send_message('/channels', [dark_mist.json()])

# print(dark_mist.display())


# exit()

# synth :beep, {note: [62.0, nil, nil, 69.0, 77.0, nil, 69.0, nil, 62.0, nil, nil, 70.0, 79.0, nil, 70.0, nil]}

bizzet = Machine()
bizzet.bar  = 4
bizzet.pmax = 8
bizzet.eighth = 0.25
sender.send_message('/settings', ['bar', bizzet.bar])
sender.send_message('/settings', ['pmax', bizzet.pmax])
# for i in range(4):
#     sender.send_message('/ping/json', [i])

# exit()

# bizet_bass = (ring :d, :r, :r, :a, :f5, :r, :a, :r)
# bizet_bass2 = (ring :d, :r, :r, :Bb, :g5, :r, :Bb, :r)
# bb = bizet_bass + bizet_bass2

# live_loop :bb do
#   16.times do
#     tick
#     play bb.look, release: 0.1
#     play bb.look - 12, release: 0.3
#     sleep 0.25
#   end
# end

beep_channel = Channel('synth', 'beep')
beep_channel.bar  = bizzet.bar
bizzet.add_channel(beep_channel)
beep_channel_12 = Channel('synth', 'beep')
beep_channel_12.bar  = bizzet.bar
bizzet.add_channel(beep_channel_12)

for ii in range(4):
    for i, n in enumerate([62.0, None, None, 69.0, 77.0, None, 69.0, None, 62.0, None, None, 70.0, 79.0, None, 70.0, None]):
        beep_channel.add_step(ii, i, 0.25, {"note": n, "release": 0.1})
    for i, n in enumerate([62.0, None, None, 69.0, 77.0, None, 69.0, None, 62.0, None, None, 70.0, 79.0, None, 70.0, None]):
        if n is None:
            beep_channel_12.add_step(ii, i, 0.25, {"note": None, "release": 0.3})
            continue
        beep_channel_12.add_step(ii, i, 0.25, {"note": n-12, "release": 0.3})

for ii in range(4,8):
    for i, n in enumerate([62.0, None, None, 69.0, 77.0, None, 69.0, None, 62.0, None, None, 70.0, 79.0, None, 70.0, None, 62.0, None, None, 69.0, 77.0, None, 69.0, None, 62.0, None, None, 70.0, 79.0, None, 70.0, None]):
        beep_channel.add_step(ii, i, 0.125, {"note": n, "release": 0.1})

    for i, n in enumerate([62.0, None, None, 69.0, 77.0, None, 69.0, None, 62.0, None, None, 70.0, 79.0, None, 70.0, None, 62.0, None, None, 69.0, 77.0, None, 69.0, None, 62.0, None, None, 70.0, 79.0, None, 70.0, None]):
        if n is None:
            beep_channel_12.add_step(ii, i, 0.125, {"note": None, "release": 0.3})
            continue
        beep_channel_12.add_step(ii, i, 0.125, {"note": n-12, "release": 0.3})



fm_channel = Channel('synth', 'fm')
fm_channel.bar  = bizzet.bar
bizzet.add_channel(fm_channel)
fm_channel.add_fx('distortion')
fm_channel.add_fx_option('distortion', 'distort', 0.9)
fm_channel_12 = Channel('synth', 'fm')
fm_channel_12.bar  = bizzet.bar
bizzet.add_channel(fm_channel_12)
fm_channel_12.add_fx('distortion')
fm_channel_12.add_fx_option('distortion', 'distort', 0.9)

for ii in range(4):
    for i, n in enumerate([62.0, None, None, 69.0, 77.0, None, 69.0, None, 62.0, None, None, 70.0, 79.0, None, 70.0, None]):
        fm_channel.add_step(ii, i, 0.25, {"note": n, "release": 0.1})
    for i, n in enumerate([62.0, None, None, 69.0, 77.0, None, 69.0, None, 62.0, None, None, 70.0, 79.0, None, 70.0, None]):
        if n is None:
            fm_channel_12.add_step(ii, i, 0.25, {"note": None, "release": 0.3})
            continue
        fm_channel_12.add_step(ii, i, 0.25, {"note": n-12, "release": 0.3})

for ii in range(4,8):
    for i, n in enumerate([62.0, None, None, 69.0, 77.0, None, 69.0, None, 62.0, None, None, 70.0, 79.0, None, 70.0, None, 62.0, None, None, 69.0, 77.0, None, 69.0, None, 62.0, None, None, 70.0, 79.0, None, 70.0, None]):
        fm_channel.add_step(ii, i, 0.125, {"note": n, "release": 0.1})
    for i, n in enumerate([62.0, None, None, 69.0, 77.0, None, 69.0, None, 62.0, None, None, 70.0, 79.0, None, 70.0, None, 62.0, None, None, 69.0, 77.0, None, 69.0, None, 62.0, None, None, 70.0, 79.0, None, 70.0, None]):
        if n is None:
            fm_channel_12.add_step(ii, i, 0.125, {"note": None, "release": 0.3})
            continue
        fm_channel_12.add_step(ii, i, 0.125, {"note": n-12, "release": 0.3})



# with_fx :slicer, phase: 0.125 do
##|       synth :blade, note: :d4, release: 8, cutoff: 100, amp: 1.5
##|     end
##|     sleep 8
##|   end

blade_channel = Channel('synth', 'blade')
blade_channel.bar  = bizzet.bar
bizzet.add_channel(blade_channel)
blade_channel.add_fx('slicer')
blade_channel.add_fx_option('slicer', 'phase', 0.125)
blade_channel.add_fx('reverb')
blade_channel.add_fx_option('reverb', 'room', 1)
blade_channel.add_fx_option('reverb', 'mix', 0.3)

blade_channel.add_step(0, 0, 4, {"note": ":d4", "release": 8, "cutoff": 100, "amp": 1.5})
blade_channel.add_step(2, 0, 4, {"note": ":d4", "release": 8, "cutoff": 100, "amp": 1.5})
blade_channel.add_step(4, 0, 4, {"note": ":d4", "release": 4, "cutoff": 100, "amp": 1.5})
blade_channel.add_step(5, 0, 4, {"note": ":d4", "release": 4, "cutoff": 100, "amp": 1.5})
blade_channel.add_step(6, 0, 4, {"note": ":d4", "release": 4, "cutoff": 100, "amp": 1.5})
blade_channel.add_step(7, 0, 4, {"note": ":d4", "release": 4, "cutoff": 100, "amp": 1.5})

  # sample :loop_industrial, beat_stretch: 1, cutoff: 100, rate: 1
indus_channel = Channel('sample', 'loop_industrial')
indus_channel.bar  = bizzet.bar
bizzet.add_channel(indus_channel)
for i in range(8):
    if i < 4:
        for ii in range(2):
            indus_channel.add_step(i, ii, 2, {"beat_stretch": 1, "cutoff": 100, "rate": 1})
    else:
        for ii in range(4):
            indus_channel.add_step(i, ii, 1, {"beat_stretch": 1, "cutoff": 100, "rate": 1})

haus_channel = Channel('sample', 'bd_haus')
haus_channel.bar  = bizzet.bar
bizzet.add_channel(haus_channel)
for i in range(8):
    if i < 4:
        for ii in range(2):
            haus_channel.add_step(i, ii, 2, {"cutoff": 110})
    else:
        for ii in range(4):
            haus_channel.add_step(i, ii, 1, {"cutoff": 110})

beepp_channel = Channel('synth', 'beep')
beepp_channel.bar  = bizzet.bar
bizzet.add_channel(beepp_channel)
for i in range(8):
    if i < 4:
        for ii in range(2):
            beepp_channel.add_step(i, ii, 2, {"note": 49, "attack": 0.5, "release": 0.1})
    else:
        for ii in range(4):
            beepp_channel.add_step(i, ii, 1, {"note": 49, "attack": 0.5, "release": 0.1})





# bizzet.json_channels()
for i, c in enumerate(bizzet.channels):
    bizzet.json_channel(i)
    sender.send_message('/channel/json/file', [i])
# bizzet.state = 'play'
# sender.send_message('/settings', ['state', bizzet.state])
# sender.send_message('/channels', [bizzet.json()])
# for i, c in enumerate(bizzet.channels):
#     sender.send_message('/channel', [i, json.dumps(c.json())])
# for ic, c in enumerate(bizzet.channels):
#   print(c.type, c.name)
#   # sender.send_message('/channel/add', [ic, c['type'], c['name'], json.dumps(c['fxs'])])
#   sender.send_message('/add', ['channel', ic, c.type, c.name, json.dumps(c.fxs)])
#   # time.sleep(1)
#   for ip, p in enumerate(c.patterns):
#     # sender.send_message('/channel/pattern/add', [ic, ip])
#     sender.send_message('/add', ['pattern', ic, ip])
#     # time.sleep(1)
#     for i_s, s in enumerate(p):
#       print([ic, ip, i_s, c.sleeps[ip][i_s], json.dumps(s)])
#       # sender.send_message('/channel/pattern/step/add', [ic, ip, i_s, c['sleeps'][ip][i_s], json.dumps(s)])
#       sender.send_message('/add', ['step', ic, ip, i_s, c.sleeps[ip][i_s], json.dumps(s)])
#       time.sleep(0.2)



bizzet.state = 'play'
sender.send_message('/settings', ['state', bizzet.state])

# print(bizzet.display())
# bizzet.del_channel(0)
# bizzet.del_channel(0)
# bizzet.del_channel(0)
# bizzet.del_channel(0)
print(bizzet.display())
exit()
time.sleep(32)
beep_channel = Channel('synth', 'beep')
beep_channel.bar  = bizzet.bar
# bizzet.del_channel(0)
bizzet.add_channel(beep_channel)
for i, n in enumerate([62.0, None, None, 69.0, 77.0, None, 69.0, None, 62.0, None, None, 70.0, 79.0, None, 70.0, None, 62.0, None, None, 69.0, 77.0, None, 69.0, None, 62.0, None, None, 70.0, 79.0, None, 70.0, None]):
    beep_channel.add_step(0, i, 0.125, {"note": n, "release": 0.1})
beep_channel_12 = Channel('synth', 'beep')
beep_channel_12.bar  = bizzet.bar
# bizzet.del_channel(1)
bizzet.add_channel(beep_channel_12)
for i, n in enumerate([62.0, None, None, 69.0, 77.0, None, 69.0, None, 62.0, None, None, 70.0, 79.0, None, 70.0, None, 62.0, None, None, 69.0, 77.0, None, 69.0, None, 62.0, None, None, 70.0, 79.0, None, 70.0, None]):
    if n is None:
        beep_channel_12.add_step(0, i, 0.125, {"note": None, "release": 0.3})
        continue
    beep_channel_12.add_step(0, i, 0.125, {"note": n-12, "release": 0.3})


fm_channel = Channel('synth', 'fm')
fm_channel.bar  = bizzet.bar
# bizzet.del_channel(2)
bizzet.add_channel(fm_channel)
for i, n in enumerate([62.0, None, None, 69.0, 77.0, None, 69.0, None, 62.0, None, None, 70.0, 79.0, None, 70.0, None, 62.0, None, None, 69.0, 77.0, None, 69.0, None, 62.0, None, None, 70.0, 79.0, None, 70.0, None]):
    fm_channel.add_step(0, i, 0.125, {"note": n, "release": 0.1})
fm_channel_12 = Channel('synth', 'fm')
fm_channel_12.bar  = bizzet.bar
# bizzet.del_channel(3)
bizzet.add_channel(fm_channel_12)
for i, n in enumerate([62.0, None, None, 69.0, 77.0, None, 69.0, None, 62.0, None, None, 70.0, 79.0, None, 70.0, None, 62.0, None, None, 69.0, 77.0, None, 69.0, None, 62.0, None, None, 70.0, 79.0, None, 70.0, None]):
    if n is None:
        fm_channel_12.add_step(0, i, 0.125, {"note": None, "release": 0.3})
        continue
    fm_channel_12.add_step(0, i, 0.125, {"note": n-12, "release": 0.3})


sender.send_message('/channels', [bizzet.json()])
print(bizzet.display())




exit()

    # machine = Machine()
    # machine.bpm = 60
    # # machine.bar = 1
    # # print(machine.display())

    # channelOne = Channel('synth', 'zawa')
    # channelOne.bar = machine.bar

    # for i in range(16):
    #     # channelOne.add_step(0, i, 0.25, {"note": random.choice(range(128)), "res": 2, "cutoff": 80, "amp": 0.5})
    #     # channelOne.add_step(1, i, 0.25, {"note": random.choice(range(128)), "res": 2, "cutoff": 80, "amp": 0.5})
    #     channelOne.add_step(0, i, 0.25, {"note": ":c2" if i%2 == 0 else ":c3", "res":0, "cutoff": 80})
    #     channelOne.add_step(1, i, 0.25, {"note": ":c2" if i%2 == 0 else None, "res":0, "cutoff": 80})
    #     # channelOne.add_step(1, i, 0.25, {"note": 60+i, "res": 2, "cutoff": 70, "amp": 0.5})

    # # channelOne.add_step(0, 0, 0.25, {"note": ":g4", "res": 2, "cutoff": 80, "amp": 0.5})
    # # channelOne.add_step(0, 1, 0.25, None)
    # # channelOne.add_step(0, 2, 0.25, {"note": ":a4", "res": 2, "cutoff": 80, "amp": 0.5, "attack": 2})
    # # channelOne.add_step(0, 3, 0.25, {"note": ":g4", "res": 2, "cutoff": 80, "amp": 0.5})
    # # channelOne.add_step(0, 4, 0.25, {"note": ":a4", "res": 2, "cutoff": 80, "amp": 0.5, "release": 2})
    # # print(machine.display())
    # # time.sleep(2)
    # # channelOne.add_step(0, 2, 0.25, None)

    # # channelOne.add_fx('reverb')
    # # channelOne.add_fx_option('reverb', 'room', 1)

    # channelTwo = Channel('sample', 'drum_cymbal_closed')
    # channelTwo.bar = machine.bar
    # channelThree = Channel('sample', 'bd_tek')
    # channelThree.bar = machine.bar
    # channelFour = Channel('sample', 'sn_dub')
    # channelFour.bar = machine.bar


    # # channelTwo = Channel('sample', 'sn_dub')

    # machine.add_channel(channelOne)
    # machine.add_channel(channelTwo)
    # machine.add_channel(channelThree)
    # machine.add_channel(channelFour)
    # machine.add_channel(channelTwo)
    # # print(machine.display())
    # # time.sleep(2)
    # # channelOne.add_step(0, 2, 0.25, None)
    # # print(14)
    # # print(machine.display())
    # channelTwo.add_step(0, 0, 0.5, {})
    # channelTwo.add_step(0, 2, 0.5, {})

    # channelTwo.add_step(0, 4, 0.5, {})
    # channelTwo.add_step(0, 6, 0.5, {})

    # channelTwo.add_step(0, 8, 0.5, {})
    # channelTwo.add_step(0, 10, 0.5, {})

    # channelTwo.add_step(0, 12, 0.5, {})
    # channelTwo.add_step(0, 14, 0.5, {})

    # channelThree.add_step(0, 0, 1, {})
    # channelThree.add_step(0, 1, 1, ':r')
    # channelThree.add_step(0, 2, 1, {})
    # # channelThree.add_step(0, 12, 0.5, None)
    # channelThree.add_step(0, 3, 0.5, None)
    # channelThree.add_step(0, 4, 0.5, {})
    # # channelThree.add_step(3, 0, 0.5, None)
    # # channelThree.add_step(0, 8, 0.25, {})
    # # channelThree.del_step(3, 0)
    # # channelThree.add_step(3, 0, 0.5, {})


    # channelFour.add_step(0, 0, 1, None)
    # channelFour.add_step(0, 1, 1, {})
    # channelFour.add_step(0, 2, 1, None)
    # channelFour.add_step(0, 4, 1, {})



    # # channelOne.add_step_with_sleep(0, {'n': 70}, 1.5, machine.get_default_sleep())
    # # channelTwo.add_step_with_sleep(0, None, machine.get_default_sleep(), machine.get_default_sleep())
    # # print(16)

    # # channelOne.add_step_with_sleep(0, None, 1.5, machine.get_default_sleep())
    # # # channelTwo.add_step_with_sleep(0, {}, machine.get_default_sleep(), machine.get_default_sleep())
    # # print(19)
    # # channelOne.add_step_with_sleep(0, {'n':62, "release": 0.5}, 1.5, machine.get_default_sleep())
    # # # channelTwo.add_step_with_sleep(0, None, machine.get_default_sleep(), machine.get_default_sleep())
    # # print(25)
    # # channelOne.add_step_with_sleep(0, {'n':61, "release": 0.5}, machine.get_default_sleep(), machine.get_default_sleep())
    # # # channelTwo.add_step_with_sleep(0, {}, machine.get_default_sleep(), machine.get_default_sleep())
    # # print(29)

    # # channelOne.add_step_with_sleep(1, {'n':63, "release": 0.5}, machine.get_default_sleep(), machine.get_default_sleep())
    # # channelTwo.add_step_with_sleep(1, {}, machine.get_default_sleep(), machine.get_default_sleep())
    # # print(machine.display())

    # # channelOne.add_step_with_sleep(0, {'n': 71}, 0.5, machine.get_default_sleep(), 2)
    # # channelOne.add_step_with_sleep(1, {'n': 72}, 0.75, machine.get_default_sleep(), 3)
    # # channelOne.add_step(0, 0, 1, {'note': 72})
    # # channelOne.add_step(1, 0, 0.5, {'note': 65})
    # # channelOne.add_step(1, 1, 0.5, {'note': 65})
    # # channelOne.add_step(2, 0, 0.1, {'note': 99})
    # # channelOne.add_step(2, 1, 0.1, {'note': 99})
    # # channelOne.add_step(2, 2, 0.25, {'note': 99})
    # # channelOne.add_step(2, 3, 0.1, {'note': 99})
    # # channelOne.add_step(4, 0, 1, None)
    # # channelOne.add_step(5, 0, 1, {'note': 50})

    # # channelOne.add_step(2, 3, 0.05, {'n': 97})
    # # channelOne.add_step(2, 1, 0.5)

    # # print(machine.display())
    # # print('OSC')
    # # channelOne.del_step(2, 1)
    # # print(machine.display())
    # sender = udp_client.SimpleUDPClient('127.0.0.1', 4560)
    # sender.send_message('/settings', ['bpm', machine.bpm])
    # # time.sleep(1)
    # sender.send_message('/settings', ['bar', machine.bar])
    # # time.sleep(0.2)
    # machine.pmax = 3
    # sender.send_message('/settings', ['pmax', machine.pmax])
    # # time.sleep(0.2)
    # machine.state = 'play'
    # sender.send_message('/settings', ['state', machine.state])

    # # channelThree.patterns[0][4] = None


    # sender.send_message('/channels', [machine.json()])
    # # time.sleep(2)

    # # sender.send_message('/state', ['play'])
    # # time.sleep(4)
    # # channelOne.del_step(2, 2)
    # # sender.send_message('/channel', [0, json.dumps(channelOne.__dict__)])

    # print(machine.display())
    # # for i, j in machine.channels[0].patterns[1][7].items():
    # #     print(i, j)
    # # time.sleep(8)
    # # machine.state = 'pause'
    # # sender.send_message('/state', [machine.state])
    # # print(machine.display_settings())
    # # time.sleep(8)
    # # machine.state = 'play'
    # # sender.send_message('/state', [machine.state])
    # # print(machine.display_settings())
    # # time.sleep(8)
    # # machine.state = 'stop'
    # # sender.send_message('/state', [machine.state])
    # # print(machine.display_settings())
    # channelOne.del_step(10, 10)
    # print(machine.channels[0].get_step(0, 15))

    # # exit()
    # # channelOne.add_step(1, 2, 0.36, {'n': 75})
    # # print(machine.display())

    # # print(machine.channels_to_list())
    # # print()
    # # print(machine.json())

    # # exit()

    # def on_instru_listener(channel: int, event: bool):
    #     # CHANNEL
    #     if pianoHat.layout == pianoHat.LAYOUT_CHANNEL:
    #         if event:
    #             pianoHat.layout = pianoHat.LAYOUT_STEP
    #             # On LED Octave Up
    #         return
    #     # STEP
    #     if pianoHat.layout == pianoHat.LAYOUT_STEP:
    #         if event:
    #             pianoHat.layout = pianoHat.LAYOUT_CHANNEL
    #             # On LED Instru
    #         return
    #     # NOTE
    #     if pianoHat.layout == pianoHat.LAYOUT_NOTE:
    #         if event:
    #             # TODO : stop recording live mod
    #             pianoHat.layout = pianoHat.LAYOUT_STEP
    #             # On LED Octave Up
    #         return

    # def on_octave_up_listener(channel:int, event: bool):
    #     # CHANNEL
    #     if pianoHat.layout == pianoHat.LAYOUT_CHANNEL:
    #         if event:
    #             if pianoHat.totalChannel > 0 and pianoHat.channel < pianoHat.totalChannel-1:
    #                 pianoHat.channel += 1
    #             else :
    #                 pianoHat.channel = 0
    #         return
    #     # STEP
    #     if pianoHat.layout == pianoHat.LAYOUT_STEP:
    #         if event:
    #             if pianoHat.mod == pianoHat.MOD_KEY:
    #                 pianoHat.mod = pianoHat.MOD_LIVE
    #             else:
    #                 pianoHat.mod = pianoHat.MOD_KEY
    #         return
    #     # NOTE
    #     if pianoHat.layout == pianoHat.LAYOUT_NOTE:
    #         if event:
    #             if pianoHat.octave < 10:
    #                 pianoHat.octave += 1
    #             else:
    #                 pianoHat.octave = 0
    #         return

    # def on_octave_down_listener(channel:int, event: bool):
    #     # CHANNEL
    #     if pianoHat.layout == pianoHat.LAYOUT_CHANNEL:
    #         if event:
    #             if pianoHat.channel > 0:
    #                 pianoHat.channel -= 1
    #                 return
    #             if pianoHat.totalChannel > 0:
    #                 pianoHat.channel = pianoHat.totalChannel-1
    #         return
    #     # STEP
    #     if pianoHat.layout == pianoHat.LAYOUT_STEP:
    #         # if event:
    #             # TODO : if already empty remove else empty
    #         return
    #     # NOTE
    #     if pianoHat.layout == pianoHat.LAYOUT_NOTE:
    #         if event:
    #             if pianoHat.octave > 0:
    #                 pianoHat.octave -= 1
    #             else:
    #                 pianoHat.octave = 10
    #         return

    # def on_note_listener(key:int, event: bool):
    #     # CHANNEL
    #     if pianoHat.layout == pianoHat.LAYOUT_CHANNEL:
    #         if event:
    #             if pianoHat.BLACK_KEYS.count(key) != 0:
    #                 pianoHat.pattern[0] = pianoHat.BLACK_KEYS.index(key)
    #             if pianoHat.WHITE_KEYS.count(key) != 0:
    #                 print(pianoHat.WHITE_KEYS, pianoHat.WHITE_KEYS.index(key));
    #                 pianoHat.pattern[1] = pianoHat.WHITE_KEYS.index(key)
    #         return
    #     # STEP
    #     if pianoHat.layout == pianoHat.LAYOUT_STEP:
    #         if event:
    #             pianoHat.step = key
    #             if len(machine.channels) > 0:
    #                 pianoHat.notes = machine.get_channel(pianoHat.channel).get_step(pianoHat.get_pattern(), pianoHat.step)
    #             pianoHat.layout = pianoHat.LAYOUT_NOTE
    #             # On LED Octave Down
    #         return

    # pianoHat = PianoHat()
    # print('PH', pianoHat.pattern)
    # on_note_listener(0, True)
    # on_note_listener(2, True)

    # print(pianoHat.get_pattern())

    # on_instru_listener(0, True)
    # on_octave_up_listener(1, True)
    # on_note_listener(8, True)
    # print(pianoHat.layout)
    # print(pianoHat.octave)
    # on_octave_up_listener(0, True)
    # print(pianoHat.octave)
    # print(pianoHat.get_pattern())
    # print(pianoHat.notes)



