from Channel import Channel
from Machine import Machine
from os import walk
from PianoHat import PianoHat
from pythonosc import osc_message_builder
from pythonosc import udp_client
import glob
import json
import os
import pianohat
import random
import re
import signal
import sys
import time


# OSC init
# osc_sender = udp_client.SimpleUDPClient('127.0.0.1', 4560)
osc_sender = udp_client.SimpleUDPClient('192.168.1.15', 4560)

## Machine init
machine = Machine()
machine.bpm = 60
machine.pmax = 2
machine.bar = 2
machine.eighth = 0.25
osc_sender.send_message('/settings', ['bar', machine.bar])
osc_sender.send_message('/settings', ['pmax', machine.pmax])

## Channels init
bd_tek_channel = Channel('sample', 'bd_tek')
bd_tek_channel.bar  = machine.bar
machine.add_channel(bd_tek_channel)
# bd_tek_channel.patterns = [ [None for _ in range(8) ] for _ in range(40)]
# bd_tek_channel.sleeps = [ [0.25 for _ in range(8) ] for _ in range(40)]

drum_cymbal_closed_channel = Channel('sample', 'drum_cymbal_closed')
drum_cymbal_closed_channel.bar  = machine.bar
machine.add_channel(drum_cymbal_closed_channel)

fm_channel = Channel('synth', 'fm')
fm_channel.bar  = machine.bar
machine.add_channel(fm_channel)
## End channels init

## PianoHAT init
piano_hat = PianoHat()
piano_hat.pmax = machine.pmax


# KEY HANDLER
## OCTAVE UP
def handle_octave_up(key: int, pressed: bool):
    print_info('octave up')
    if piano_hat.layout == piano_hat.LAYOUT_CHANNEL and pressed:
        on_octave_up_channel(key, pressed)
        return
    if piano_hat.layout == piano_hat.LAYOUT_PATTERN and pressed:
        on_octave_up_pattern(key, pressed)
        return
    if piano_hat.layout == piano_hat.LAYOUT_STEP and pressed:
        on_octave_up_step(key, pressed)
        return
## OCTAVE DOWN
def handle_octave_down(key: int, pressed: bool):
    print_info('octave down')
    if piano_hat.layout == piano_hat.LAYOUT_CHANNEL and pressed:
        on_octave_down_channel(key, pressed)
        return
    if piano_hat.layout == piano_hat.LAYOUT_PATTERN and pressed:
        on_octave_down_pattern(key, pressed)
        return
    if piano_hat.layout == piano_hat.LAYOUT_STEP and pressed:
        on_octave_down_step(key, pressed)
        return
## NOTE
def handle_note(key: int, pressed: bool):
    print_info('note '+str(key))
    if piano_hat.layout == piano_hat.LAYOUT_CHANNEL and pressed:
        on_note_channel(key, pressed)
        return
    if piano_hat.layout == piano_hat.LAYOUT_PATTERN and pressed and piano_hat.WHITE_KEYS.count(key) != 0:
        on_note_pattern(key, pressed)
        return
    if piano_hat.layout == piano_hat.LAYOUT_STEP and pressed:
        on_note_step(key, pressed)
        return
    if piano_hat.layout == piano_hat.LAYOUT_MIDI and pressed:
        on_note_midi(key, pressed)
        return
## INSTRUMENT
def handle_instrument(key: int, pressed: bool):
    print_info('instrument')
    if piano_hat.layout == piano_hat.LAYOUT_CHANNEL and pressed:
        on_instrument_channel(key, pressed)
        return
    if piano_hat.layout == piano_hat.LAYOUT_PATTERN and pressed:
        on_instrument_pattern(key, pressed)
        return
    if piano_hat.layout == piano_hat.LAYOUT_STEP and pressed:
        on_instrument_step(key, pressed)
        return
    if piano_hat.layout == piano_hat.LAYOUT_MIDI and pressed:
        on_instrument_midi(key, pressed)
        return




# KEY_LAYOUT
## OCTAVE UP
### CHANNEL
def on_octave_up_channel(key: int, pressed: bool):
    if piano_hat.channel < len(machine.channels)-1:
        piano_hat.channel += 1
    else :
        piano_hat.channel = -1
    if piano_hat.channel == -1:
        leds_off()
        pianohat.set_led(15, True)
## PATTERN
def on_octave_up_pattern(key: int, pressed: bool):
    if machine.channels[piano_hat.channel].type == 'synth':
        piano_hat.layout = piano_hat.LAYOUT_STEP
        piano_hat.mod = piano_hat.MOD_LIVE
        piano_hat.step = 0
        pianohat.set_led(14, True)
## STEP
def on_octave_up_step(key: int, pressed: bool):
    if piano_hat.octave < 10:
        piano_hat.octave += 1
    else :
        piano_hat.octave = 0


## OCTAVE DOWN
### CHANNEL
def on_octave_down_channel(key: int, pressed: bool):
    if piano_hat.channel == -1:
        piano_hat.channel = len(machine.channels)-1
    else:
        piano_hat.channel -= 1
## PATTERN
def on_octave_down_pattern(key: int, pressed: bool):
    all_none = True
    for i in machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()]:
        if i is not None:
            all_none = False
    if all_none:
        del(machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()])
    else:
        machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()] = [None for _ in range(8)]
## STEP
def on_octave_down_step(key: int, pressed: bool):
    if piano_hat.octave == 0:
        piano_hat.octave = 10
    else:
        piano_hat.octave -= 1


## NOTE
### CHANNEL
def on_note_channel(key: int, pressed: bool):
    if piano_hat.BLACK_KEYS.count(key) != 0:
        piano_hat.pattern[0] = piano_hat.BLACK_KEYS.index(key)
    if piano_hat.WHITE_KEYS.count(key) != 0:
        piano_hat.pattern[1] = piano_hat.WHITE_KEYS.index(key)
    leds_channel_on()
### Pattern
def on_note_pattern(key: int, pressed: bool):
    if machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()][piano_hat.WHITE_KEYS.index(key)] is None:
        if machine.channels[piano_hat.channel].type == 'sample' or machine.channels[piano_hat.channel].type == 'external_sample':
            on_note_pattern_sample(key, pressed)
        if machine.channels[piano_hat.channel].type == 'synth':
            on_note_pattern_synth(key, pressed)
        return
    machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()][piano_hat.WHITE_KEYS.index(key)] = None
    leds_pattern_on(machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()])
def on_note_pattern_sample(key: int, pressed: bool):
    machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()][piano_hat.WHITE_KEYS.index(key)] = {}
    leds_pattern_on(machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()])
def on_note_pattern_synth(key: int, pressed: bool):
    piano_hat.layout = piano_hat.LAYOUT_STEP
    piano_hat.step = piano_hat.WHITE_KEYS.index(key)
    leds_step_on(machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()][piano_hat.step])
## STEP
def on_note_step(key: int, pressed: bool):
    if piano_hat.mod == piano_hat.MOD_LIVE and machine.channels[piano_hat.channel].type == 'synth':
        if piano_hat.step < 8:
            pianohat.set_led(14, False)
            time.sleep(0.05)
            pianohat.set_led(14, True)
            time.sleep(0.05)
            pianohat.set_led(14, False)
            machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()][piano_hat.step] = {"note": [piano_hat.key_to_midi_note(key)]}
            piano_hat.step = piano_hat.step + 1
            return
        # Back to layout pattern and mod key after 8 notes type
        piano_hat.step = 0
        piano_hat.layout = piano_hat.LAYOUT_PATTERN
        pianohat.set_led(14, False)
        piano_hat.mod = piano_hat.MOD_KEY
        osc_sender.send_message('/channel/json', [piano_hat.channel, json.dumps(machine.channels[piano_hat.channel].__dict__)])
        leds_pattern_on(machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()])
        return
    if piano_hat.mod == piano_hat.MOD_KEY and machine.channels[piano_hat.channel].type == 'synth':
        if machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()][piano_hat.step] is None:
            machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()][piano_hat.step] = {"note": []}
        if machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()][piano_hat.step]["note"].index(piano_hat.key_to_midi_note(key)) is not None:
            machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()][piano_hat.step]["note"].remove(piano_hat.key_to_midi_note(key))
            return
        machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()][piano_hat.step]["note"].append(piano_hat.key_to_midi_note(key))
        leds_step_on(machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()][piano_hat.step])
## MIDI
def on_note_midi(key: int, pressed: bool):
    note = piano_hat.key_to_midi_note(key)

## INSTRUMENT
### CHANNEL
def on_instrument_channel(key: int, pressed: bool):
    piano_hat.layout = piano_hat.LAYOUT_PATTERN
    if piano_hat.channel == -1:
        piano_hat.layout = piano_hat.LAYOUT_MIDI
        leds_off()
    elif len(machine.channels[piano_hat.channel].patterns) <= piano_hat.get_pattern():
        for i in range(piano_hat.get_pattern()+1):
            if len(machine.channels[piano_hat.channel].patterns) <= i:
                machine.channels[piano_hat.channel].patterns.insert(i, [None for _ in range(8) ])
                machine.channels[piano_hat.channel].sleeps.insert(i, [0.25 for _ in range(8) ])
    leds_pattern_on(machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()])
### PATTERN
def on_instrument_pattern(key: int, pressed: bool):
    piano_hat.layout = piano_hat.LAYOUT_CHANNEL
    osc_sender.send_message('/channel/json', [piano_hat.channel, json.dumps(machine.channels[piano_hat.channel].__dict__)])
    leds_channel_on()
## STEP
def on_instrument_step(key: int, pressed: bool):
    piano_hat.layout = piano_hat.LAYOUT_PATTERN
    pianohat.set_led(14, False)
    piano_hat.mod = piano_hat.MOD_KEY
    osc_sender.send_message('/channel/json', [piano_hat.channel, json.dumps(machine.channels[piano_hat.channel].__dict__)])
    leds_pattern_on(machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()])
## NOTE
def on_instrument_midi(key: int, pressed: bool):
    piano_hat.layout = piano_hat.LAYOUT_CHANNEL
    leds_pattern_on(machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()])


# LED HANDLER
def leds_off():
    for i in range(16):
        pianohat.set_led(i, False)
def leds_on(sleep = 0):
    for i in range(16):
        pianohat.set_led(i, True)
        if sleep != 0:
            time.sleep(sleep)
            pianohat.set_led(i, False)
            time.sleep(sleep)
def leds_channel_on():
    leds_off()
    pianohat.set_led(piano_hat.BLACK_KEYS[piano_hat.pattern[0]], True)
    pianohat.set_led(piano_hat.WHITE_KEYS[piano_hat.pattern[1]], True)
def leds_pattern_on(pattern):
    leds_off()
    if len(pattern) > 0:
        for i, step in enumerate(pattern):
            if step is not None:
                pianohat.set_led(piano_hat.WHITE_KEYS[i], True)
            else:
                pianohat.set_led(piano_hat.WHITE_KEYS[i], False)
def leds_step_on(step):
    leds_off()
    if step.get("note") is not None:
        for i, note in enumerate(step.get("note")):
            if none is not None:
                k_l = [piano_hat.WHITE_KEYS] + [piano_hat.BLACK_KEYS]
                pianohat.set_led(k_l[k_l.index(piano_hat.midi_note_to_key(key))], True)
                continue
            pianohat.set_led(k_l[k_l.index(piano_hat.midi_note_to_key(key))], False)

def print_info(key_string: str):
    print('#############################')
    print('KEY '+key_string)
    print('LAYOUT '+str(piano_hat.layout))
    print('MOD '+str(piano_hat.mod))
    print('CHANNEL '+str(piano_hat.channel))
    print('OCTAVE '+str(piano_hat.octave))
    print('STEP '+str(piano_hat.step))
    print('PATTERNS '+str(machine.channels[piano_hat.channel].patterns))




# PIANOHAT PCB INIT
pianohat.auto_leds(False)
pianohat.on_instrument(handle_instrument)
pianohat.on_note(handle_note)
pianohat.on_octave_up(handle_octave_up)
pianohat.on_octave_down(handle_octave_down)
leds_off()
leds_on(0.01)
leds_off()

def signal_handler(signal, frame):
  leds_off()
  print()
  sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)
signal.pause()

exit()















def handle_octave_up(key: int, pressed: bool):
    # print('OCTAVE UP pressed : '+str(pressed))
    if piano_hat.layout == piano_hat.LAYOUT_CHANNEL and pressed:
        # print('LAYOUT : Channel')
        # print('CHANNEL : '+str(piano_hat.channel))
        if piano_hat.channel < len(machine.channels)-1:
            piano_hat.channel += 1
        else :
            piano_hat.channel = 0
        print('CHANNEL : '+str(piano_hat.channel))
        return
    if piano_hat.layout == piano_hat.LAYOUT_PATTERN and pressed:
        piano_hat.layout = piano_hat.LAYOUT_NOTE
        return

    if piano_hat.layout == piano_hat.LAYOUT_STEP and pressed:
        if piano_hat.octave < 10-1:
            piano_hat.octave += 1
        else :
            piano_hat.octave = 0
        print('OCTAVE : '+str(piano_hat.octave))

def handle_octave_down(key:int, pressed: bool):
    # print('OCTAVE DOWN pressed : '+str(pressed))
    if piano_hat.layout == piano_hat.LAYOUT_CHANNEL and pressed:
        # print('LAYOUT : Channel')
        # print('CHANNEL : '+str(piano_hat.channel))
        if piano_hat.channel == 0:
            piano_hat.channel = len(machine.channels)-1
        else:
            piano_hat.channel -= 1
        print('CHANNEL : '+str(piano_hat.channel))
        return
    if piano_hat.layout == piano_hat.LAYOUT_PATTERN and pressed:
        print(str(machine.channels[piano_hat.channel].patterns))
        leds_off()
        all_none = True
        for i in machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()]:
            if i is not None:
                all_none = False
        if all_none:
            del(machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()])
        else :
            machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()] = [None for _ in range(8) ]
        print(str(machine.channels[piano_hat.channel].patterns))
        return
    if piano_hat.layout == piano_hat.LAYOUT_STEP and pressed:
        if piano_hat.octave == 0:
            piano_hat.octave = 10-1
        else:
            piano_hat.octave -= 1
        print('OCTAVE : '+str(piano_hat.octave))

def handle_note(key:int, pressed: bool):
    # print('NOTE pressed : '+str(pressed))
    if piano_hat.layout == piano_hat.LAYOUT_CHANNEL and pressed:
        leds_off()
        if piano_hat.BLACK_KEYS.count(key) != 0:
            piano_hat.pattern[0] = piano_hat.BLACK_KEYS.index(key)
        if piano_hat.WHITE_KEYS.count(key) != 0:
            piano_hat.pattern[1] = piano_hat.WHITE_KEYS.index(key)
        pianohat.set_led(piano_hat.BLACK_KEYS[piano_hat.pattern[0]], True)
        pianohat.set_led(piano_hat.WHITE_KEYS[piano_hat.pattern[1]], True)
        # print('Piano Hat patterns : '+str(piano_hat.pattern))
        return
    if piano_hat.layout == piano_hat.LAYOUT_PATTERN and pressed and piano_hat.WHITE_KEYS.count(key) != 0:
        if machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()][piano_hat.WHITE_KEYS.index(key)] is None:
            if machine.channels[piano_hat.channel].type == 'sample' and machine.channels[piano_hat.channel].type == 'external_sample':
                pianohat.set_led(piano_hat.WHITE_KEYS[piano_hat.WHITE_KEYS.index(key)], True)
                machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()][piano_hat.WHITE_KEYS.index(key)] = {}
                return
            if machine.channels[piano_hat.channel].type == 'synth':
                piano_hat.layout = piano_hat.LAYOUT_STEP
                piano_hat.step = piano_hat.WHITE_KEYS.index(key)
                print(str(piano_hat.layout))
                return
        pianohat.set_led(piano_hat.WHITE_KEYS[piano_hat.WHITE_KEYS.index(key)], False)
        machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()][piano_hat.WHITE_KEYS.index(key)] = None
        print(str(machine.channels[piano_hat.channel].patterns))
        return
    if piano_hat.layout == piano_hat.LAYOUT_STEP and pressed:
        if machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()][piano_hat.step] is None:
            machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()][piano_hat.step] = {"note": []}
        machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()][piano_hat.step]['note'].append(piano_hat.key_to_midi_note(key))
        return
    if piano_hat.layout == piano_hat.LAYOUT_NOTE and pressed:
        if machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()][piano_hat.step] is None:
            machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()][piano_hat.step] = {"note": []}
        machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()][piano_hat.step]['note'].append(piano_hat.key_to_midi_note(key))


def handle_instrument(key: int, pressed: bool):
    # print('INSTRU pressed : '+str(pressed))
    print(str(piano_hat.layout))
    if piano_hat.layout == piano_hat.LAYOUT_CHANNEL and pressed:
        leds_off()
        piano_hat.layout = piano_hat.LAYOUT_PATTERN
        if len(machine.channels[piano_hat.channel].patterns) <= piano_hat.get_pattern():
            for i in range(piano_hat.get_pattern()+1):
                if len(machine.channels[piano_hat.channel].patterns) <= i:
                    machine.channels[piano_hat.channel].patterns.insert(i, [None for _ in range(8) ])
                    machine.channels[piano_hat.channel].sleeps.insert(i, [0.25 for _ in range(8) ])
        print(str(machine.channels[piano_hat.channel].patterns))
        for i, p in enumerate(machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()]):
            if p is not None:
                pianohat.set_led(piano_hat.WHITE_KEYS[i], True)
            else:
                pianohat.set_led(piano_hat.WHITE_KEYS[i], False)
        return
    if piano_hat.layout == piano_hat.LAYOUT_PATTERN and pressed:
        leds_off()
        piano_hat.layout = piano_hat.LAYOUT_CHANNEL
        pianohat.set_led(piano_hat.BLACK_KEYS[piano_hat.pattern[0]], True)
        pianohat.set_led(piano_hat.WHITE_KEYS[piano_hat.pattern[1]], True)
        osc_sender.send_message('/channel/json', [piano_hat.channel, json.dumps(machine.channels[piano_hat.channel].__dict__)])
        return
    if piano_hat.layout == piano_hat.LAYOUT_STEP and pressed:
        piano_hat.layout = piano_hat.LAYOUT_PATTERN
        osc_sender.send_message('/channel/json', [piano_hat.channel, json.dumps(machine.channels[piano_hat.channel].__dict__)])
        for i, p in enumerate(machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()]):
            if p is not None:
                pianohat.set_led(piano_hat.WHITE_KEYS[i], True)
            else:
                pianohat.set_led(piano_hat.WHITE_KEYS[i], False)




def handle_note2(key:int, pressed: bool):
    print('NOTE pressed : '+str(pressed))

    if piano_hat.layout == piano_hat.LAYOUT_CHANNEL and pressed:
        leds_off()
        if piano_hat.BLACK_KEYS.count(key) != 0:
            piano_hat.pattern[0] = piano_hat.BLACK_KEYS.index(key)
        if piano_hat.WHITE_KEYS.count(key) != 0:
            piano_hat.pattern[1] = piano_hat.WHITE_KEYS.index(key)
        pianohat.set_led(piano_hat.BLACK_KEYS[piano_hat.pattern[0]], True)
        pianohat.set_led(piano_hat.WHITE_KEYS[piano_hat.pattern[1]], True)
        print('Piano Hat patterns : '+str(piano_hat.pattern))
        return

    if piano_hat.layout == piano_hat.LAYOUT_PATTERN and pressed and piano_hat.WHITE_KEYS.count(key) != 0:
        if machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()][piano_hat.WHITE_KEYS.index(key)] is None:
            machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()][piano_hat.WHITE_KEYS.index(key)] = {}
            pianohat.set_led(key, True)
        else:
            machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()][piano_hat.WHITE_KEYS.index(key)] = None
            pianohat.set_led(key, False)
        osc_sender.send_message('/channel/json', [0, json.dumps(machine.channels[piano_hat.channel].__dict__)])

        print('MACHINE paterns : '+str(machine.channels[piano_hat.channel].patterns))

def handle_instrument2(key: int, pressed: bool):
    print('INSTRU pressed : '+str(pressed))

    if piano_hat.layout == piano_hat.LAYOUT_CHANNEL and pressed:
        leds_off()
        piano_hat.layout = piano_hat.LAYOUT_PATTERN
        if len(machine.get_channel(piano_hat.channel).patterns) <= piano_hat.get_pattern():
            machine.channels[piano_hat.channel].patterns.insert(piano_hat.get_pattern(), [])
            machine.channels[piano_hat.channel].sleeps.insert(piano_hat.get_pattern(), [])
            for i in range(8):
                # if i % 2 == 0:
                    machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()].append(None)
                    machine.channels[piano_hat.channel].sleeps[piano_hat.get_pattern()].append(0.25)
                # else:
                    # machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()].append('a')
        for i, j in enumerate(machine.get_channel(piano_hat.channel).patterns[piano_hat.get_pattern()]):
            if (j is not None):
                pianohat.set_led(piano_hat.WHITE_KEYS[i], True)
        print('MACHINE paterns : '+str(machine.channels[piano_hat.channel].patterns))
        return 
    if piano_hat.layout == piano_hat.LAYOUT_PATTERN and pressed:
        piano_hat.layout = piano_hat.LAYOUT_CHANNEL
        leds_off()
        pianohat.set_led(piano_hat.BLACK_KEYS[piano_hat.pattern[0]], True)
        pianohat.set_led(piano_hat.WHITE_KEYS[piano_hat.pattern[0]], True)


def leds_off():
    for i in range(16):
        pianohat.set_led(i, False)

# def handle_note(channel, pressed):
#     print(channel)
#     print(pressed)

leds_off()
# Pianohat init
pianohat.auto_leds(False)
pianohat.on_note(handle_note)
pianohat.on_octave_up(handle_octave_up)
pianohat.on_octave_down(handle_octave_down)
pianohat.on_instrument(handle_instrument)

signal.pause()
