from Machine import Machine
from Channel import Channel
from PianoHat import PianoHat

from pythonosc import osc_message_builder
from pythonosc import udp_client
import time
import json
import sys
import random

machine = Machine()
machine.bpm = 120
# machine.bar = 1
# print(machine.display())

channelOne = Channel('synth', 'fm')
channelOne.bar = machine.bar

for i in range(16):
    # channelOne.add_step(0, i, 0.25, {"note": random.choice(range(128)), "res": 2, "cutoff": 80, "amp": 0.5})
    # channelOne.add_step(1, i, 0.25, {"note": random.choice(range(128)), "res": 2, "cutoff": 80, "amp": 0.5})
    channelOne.add_step(0, i, 0.25, {"note": i+50, "res": 2, "cutoff": 80, "amp": 0.5})
    channelOne.add_step(1, i, 0.25, {"note": 60+i, "res": 2, "cutoff": 80, "amp": 0.5})

# channelOne.add_step(0, 0, 0.25, {"note": ":g4", "res": 2, "cutoff": 80, "amp": 0.5})
# channelOne.add_step(0, 1, 0.25, None)
# channelOne.add_step(0, 2, 0.25, {"note": ":a4", "res": 2, "cutoff": 80, "amp": 0.5, "attack": 2})
# channelOne.add_step(0, 3, 0.25, {"note": ":g4", "res": 2, "cutoff": 80, "amp": 0.5})
# channelOne.add_step(0, 4, 0.25, {"note": ":a4", "res": 2, "cutoff": 80, "amp": 0.5, "release": 2})
# print(machine.display())
# time.sleep(2)
# channelOne.add_step(0, 2, 0.25, None)

# channelOne.add_fx('reverb')
# channelOne.add_fx_option('reverb', 'room', 1)

channelTwo = Channel('sample', 'drum_cymbal_closed')
channelTwo.bar = machine.bar
channelThree = Channel('sample', 'bd_tek')
channelThree.bar = machine.bar
channelFour = Channel('sample', 'sn_dub')
channelFour.bar = machine.bar


# channelTwo = Channel('sample', 'sn_dub')

machine.add_channel(channelOne)
machine.add_channel(channelTwo)
machine.add_channel(channelThree)
machine.add_channel(channelFour)
machine.add_channel(channelTwo)
# print(machine.display())
# time.sleep(2)
# channelOne.add_step(0, 2, 0.25, None)
# print(14)
# print(machine.display())
channelTwo.add_step(0, 0, 0.5, {})
channelTwo.add_step(0, 2, 0.5, {})

channelTwo.add_step(0, 4, 0.5, {})
channelTwo.add_step(0, 6, 0.5, {})

channelTwo.add_step(0, 8, 0.5, {})
channelTwo.add_step(0, 10, 0.5, {})

channelTwo.add_step(0, 12, 0.5, {})
channelTwo.add_step(0, 14, 0.5, {})

channelThree.add_step(0, 0, 1, {})
channelThree.add_step(0, 1, 1, None)
channelThree.add_step(0, 2, 1, {})
# channelThree.add_step(0, 12, 0.5, None)
channelThree.add_step(0, 3, 0.5, None)
channelThree.add_step(0, 4, 0.5, {})
# channelThree.add_step(3, 0, 0.5, None)
# channelThree.add_step(0, 8, 0.25, {})
# channelThree.del_step(3, 0)
# channelThree.add_step(3, 0, 0.5, {})


channelFour.add_step(0, 0, 1, None)
channelFour.add_step(0, 1, 1, {})
channelFour.add_step(0, 2, 1, None)
channelFour.add_step(0, 4, 1, {})



# channelOne.add_step_with_sleep(0, {'n': 70}, 1.5, machine.get_default_sleep())
# channelTwo.add_step_with_sleep(0, None, machine.get_default_sleep(), machine.get_default_sleep())
# print(16)

# channelOne.add_step_with_sleep(0, None, 1.5, machine.get_default_sleep())
# # channelTwo.add_step_with_sleep(0, {}, machine.get_default_sleep(), machine.get_default_sleep())
# print(19)
# channelOne.add_step_with_sleep(0, {'n':62, "release": 0.5}, 1.5, machine.get_default_sleep())
# # channelTwo.add_step_with_sleep(0, None, machine.get_default_sleep(), machine.get_default_sleep())
# print(25)
# channelOne.add_step_with_sleep(0, {'n':61, "release": 0.5}, machine.get_default_sleep(), machine.get_default_sleep())
# # channelTwo.add_step_with_sleep(0, {}, machine.get_default_sleep(), machine.get_default_sleep())
# print(29)

# channelOne.add_step_with_sleep(1, {'n':63, "release": 0.5}, machine.get_default_sleep(), machine.get_default_sleep())
# channelTwo.add_step_with_sleep(1, {}, machine.get_default_sleep(), machine.get_default_sleep())
# print(machine.display())

# channelOne.add_step_with_sleep(0, {'n': 71}, 0.5, machine.get_default_sleep(), 2)
# channelOne.add_step_with_sleep(1, {'n': 72}, 0.75, machine.get_default_sleep(), 3)
# channelOne.add_step(0, 0, 1, {'note': 72})
# channelOne.add_step(1, 0, 0.5, {'note': 65})
# channelOne.add_step(1, 1, 0.5, {'note': 65})
# channelOne.add_step(2, 0, 0.1, {'note': 99})
# channelOne.add_step(2, 1, 0.1, {'note': 99})
# channelOne.add_step(2, 2, 0.25, {'note': 99})
# channelOne.add_step(2, 3, 0.1, {'note': 99})
# channelOne.add_step(4, 0, 1, None)
# channelOne.add_step(5, 0, 1, {'note': 50})

# channelOne.add_step(2, 3, 0.05, {'n': 97})
# channelOne.add_step(2, 1, 0.5)

# print(machine.display())
# print('OSC')
# channelOne.del_step(2, 1)
# print(machine.display())
sender = udp_client.SimpleUDPClient('127.0.0.1', 4560)
sender.send_message('/settings', ['bpm', machine.bpm])
# time.sleep(1)
sender.send_message('/settings', ['bar', machine.bar])
# time.sleep(0.2)
machine.pmax = 2
sender.send_message('/settings', ['pmax', machine.pmax])
# time.sleep(0.2)
machine.state = 'play'
sender.send_message('/state', [machine.state])

# channelThree.patterns[0][4] = None


sender.send_message('/channels', [machine.json()])
# time.sleep(2)

# sender.send_message('/state', ['play'])
# time.sleep(4)
# channelOne.del_step(2, 2)
# sender.send_message('/channel', [0, json.dumps(channelOne.__dict__)])

print(machine.display())

time.sleep(8)
machine.state = 'pause'
sender.send_message('/state', [machine.state])
print(machine.display_settings())
time.sleep(8)
machine.state = 'play'
sender.send_message('/state', [machine.state])
print(machine.display_settings())
time.sleep(8)
machine.state = 'stop'
sender.send_message('/state', [machine.state])
print(machine.display_settings())



exit()
# channelOne.add_step(1, 2, 0.36, {'n': 75})
# print(machine.display())

# print(machine.channels_to_list())
# print()
# print(machine.json())

exit()

def on_instru_listener(channel: int, event: bool):
    # CHANNEL
    if pianoHat.layout == pianoHat.LAYOUT_CHANNEL:
        if event:
            pianoHat.layout = pianoHat.LAYOUT_STEP
            # On LED Octave Up
        return
    # STEP
    if pianoHat.layout == pianoHat.LAYOUT_STEP:
        if event:
            pianoHat.layout = pianoHat.LAYOUT_CHANNEL
            # On LED Instru
        return
    # NOTE
    if pianoHat.layout == pianoHat.LAYOUT_NOTE:
        if event:
            # TODO : stop recording live mod
            pianoHat.layout = pianoHat.LAYOUT_STEP
            # On LED Octave Up
        return

def on_octave_up_listener(channel:int, event: bool):
    # CHANNEL
    if pianoHat.layout == pianoHat.LAYOUT_CHANNEL:
        if event:
            if pianoHat.totalChannel > 0 and pianoHat.channel < pianoHat.totalChannel-1:
                pianoHat.channel += 1
            else :
                pianoHat.channel = 0
        return
    # STEP
    if pianoHat.layout == pianoHat.LAYOUT_STEP:
        if event:
            if pianoHat.mod == pianoHat.MOD_KEY:
                pianoHat.mod = pianoHat.MOD_LIVE
            else:
                pianoHat.mod = pianoHat.MOD_KEY
        return
    # NOTE
    if pianoHat.layout == pianoHat.LAYOUT_NOTE:
        if event:
            if pianoHat.octave < 10:
                pianoHat.octave += 1
            else:
                pianoHat.octave = 0
        return

def on_octave_down_listener(channel:int, event: bool):
    # CHANNEL
    if pianoHat.layout == pianoHat.LAYOUT_CHANNEL:
        if event:
            if pianoHat.channel > 0:
                pianoHat.channel -= 1
                return
            if pianoHat.totalChannel > 0:
                pianoHat.channel = pianoHat.totalChannel-1
        return
    # STEP
    if pianoHat.layout == pianoHat.LAYOUT_STEP:
        # if event:
            # TODO : if already empty remove else empty
        return
    # NOTE
    if pianoHat.layout == pianoHat.LAYOUT_NOTE:
        if event:
            if pianoHat.octave > 0:
                pianoHat.octave -= 1
            else:
                pianoHat.octave = 10
        return

def on_note_listener(key:int, event: bool):
    # CHANNEL
    if pianoHat.layout == pianoHat.LAYOUT_CHANNEL:
        if event:
            if pianoHat.BLACK_KEYS.count(key) != 0:
                pianoHat.pattern[0] = pianoHat.BLACK_KEYS.index(key)
            if pianoHat.WHITE_KEYS.count(key) != 0:
                pianoHat.pattern[1] = pianoHat.WHITE_KEYS.index(key)
        return
    # STEP
    if pianoHat.layout == pianoHat.LAYOUT_STEP:
        if event:
            pianoHat.step = key
            if len(machine.channels) > 0:
                pianoHat.notes = machine.channels[pianoHat.channel].patterns[pianoHat.get_pattern()][pianoHat.step]
            pianoHat.layout = pianoHat.LAYOUT_NOTE
            # On LED Octave Down
        return


# print(machine.json())

pianoHat = PianoHat()
# print(pianoHat.get_pattern())
on_note_listener(0, True)
# print(pianoHat.get_pattern())
on_note_listener(0, True)
# print(pianoHat.get_pattern())
on_instru_listener(0, True)
# print(pianoHat.mod)
on_octave_up_listener(0, True)
# print(pianoHat.mod)
on_note_listener(0, True)
# print(pianoHat.layout)
# print(pianoHat.octave)
on_octave_up_listener(0, True)
# print(pianoHat.octave)
# print(pianoHat.notes)
# print(machine.channels)
# print(machine.display())
# piano.on_note(pianoHat.on_note)


