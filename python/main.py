from Channel import Channel
from Machine import Machine
from os import walk
from PianoHat import PianoHat
from pythonosc import osc_message_builder
from pythonosc import udp_client
import glob
import json
import os
# import pianohat
import random
import re
import signal
import sys
import time


# OSC init
osc_sender = udp_client.SimpleUDPClient('127.0.0.1', 4560)
# osc_sender = udp_client.SimpleUDPClient('192.168.1.15', 4560)

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
def handle_octave_up(key: int, event: bool):
    if piano_hat.layout == piano_hat.LAYOUT_CHANNEL and pressed:
        on_octave_up_channel(key, event)
    if piano_hat.layout == piano_hat.LAYOUT_PATTERN and pressed:
        on_octave_up_pattern(key, event)
    if piano_hat.layout == piano_hat.LAYOUT_STEP and pressed:
        on_octave_up_step(key, event)
## OCTAVE DOWN
def handle_octave_down(key: int, event: bool):
    if piano_hat.layout == piano_hat.LAYOUT_CHANNEL and pressed:
        on_octave_down_channel(key, event)
    if piano_hat.layout == piano_hat.LAYOUT_PATTERN and pressed:
        on_octave_down_pattern(key, event)
    if piano_hat.layout == piano_hat.LAYOUT_STEP and pressed:
        on_octave_down_step(key, event)
## NOTE
def handle_note(key: int, event: bool):
    if piano_hat.layout == piano_hat.LAYOUT_CHANNEL and pressed:
        on_note_channel(key, event)
    if piano_hat.layout == piano_hat.LAYOUT_PATTERN and pressed and piano_hat.WHITE_KEYS.count(key) != 0:
        on_note_pattern(key, event)
    if piano_hat.layout == piano_hat.LAYOUT_STEP and pressed:
        on_note_step(key, event)
## INSTRUMENT
def handle_instrument(key: int, event: bool):
    if piano_hat.layout == piano_hat.LAYOUT_CHANNEL and pressed:
        on_instrument_channel(key, event)
    if piano_hat.layout == piano_hat.LAYOUT_PATTERN and pressed:
        on_instrument_pattern(key, event)
    if piano_hat.layout == piano_hat.LAYOUT_STEP and pressed:
        on_instrument_step(key, event)




# KEY_LAYOUT
## OCTAVE UP
### CHANNEL
def on_octave_up_channel(key: int, event: bool):
    if piano_hat.channel < len(machine.channels)-1:
        piano_hat.channel += 1
    else :
        piano_hat.channel = 0
## PATTERN
def on_octave_up_pattern(key: int, event: bool):
    if machine.channels[piano_hat.channel].type == 'synth':
        piano_hat.layout = piano_hat.LAYOUT_STEP
        piano_hat.mod = piano_hat.MOD_LIVE
        piano_hat.step = 0
## STEP
def on_octave_up_step(key: int, event: bool):
    if piano_hat.octave < 10:
        piano_hat.octave += 1
    else :
        piano_hat.octave = 0


## OCTAVE DOWN
### CHANNEL
def on_octave_down_channel(key: int, event: bool):
    if piano_hat.channel == 0:
        piano_hat.channel = len(machine.channels)-1
    else:
        piano_hat.channel -= 1
## PATTERN
def on_octave_down_pattern(key: int, event: bool):
    all_none = True
    for i in machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()]:
        if i is not None:
            all_none = False
    if all_none:
        del(machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()])
    else:
        machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()] = [None for _ in range(8)]
## STEP
def on_octave_down_step(key: int, event: bool):
    if piano_hat.octave == 0:
        piano_hat.octave = 10
    else:
        piano_hat.octave -= 1


## NOTE
### CHANNEL
def on_note_channel(key: int, event: bool):
    if piano_hat.BLACK_KEYS.count(key) != 0:
        piano_hat.pattern[0] = piano_hat.BLACK_KEYS.index(key)
    if piano_hat.WHITE_KEYS.count(key) != 0:
        piano_hat.pattern[1] = piano_hat.WHITE_KEYS.index(key)
    # pianohat.set_led(piano_hat.BLACK_KEYS[piano_hat.pattern[0]], True)
    # pianohat.set_led(piano_hat.WHITE_KEYS[piano_hat.pattern[1]], True)
### Pattern
def on_note_pattern(key: int, event: bool):
    if machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()][piano_hat.WHITE_KEYS.index(key)] is None:
        if machine.channels[piano_hat.channel].type == 'sample' or machine.channels[piano_hat.channel].type == 'external_sample':
            on_note_pattern_sample(key, event)
        if machine.channels[piano_hat.channel].type == 'synth':
            on_note_pattern_synth(key, event)
        return
    # pianohat.set_led(piano_hat.WHITE_KEYS[piano_hat.WHITE_KEYS.index(key)], False)
    machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()][piano_hat.WHITE_KEYS.index(key)] = None
def on_note_pattern_sample(key: int, event: bool):
    # pianohat.set_led(piano_hat.WHITE_KEYS[piano_hat.WHITE_KEYS.index(key)], True)
    machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()][piano_hat.WHITE_KEYS.index(key)] = {}
def on_note_pattern_synth(key: int, event: bool):
    piano_hat.layout = piano_hat.LAYOUT_STEP
    piano_hat.step = piano_hat.WHITE_KEYS.index(key)
## STEP
def on_note_step(key: int, event: bool):
    if piano_hat.mod == piano_hat.MOD_LIVE and machine.channels[piano_hat.channel].type == 'synth':
        if piano_hat.step < 8:
            machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()][piano_hat.step] = {"note": [piano_hat.midi_note(key)]}
            piano_hat.step = piano_hat.step + 1
        return
    if piano_hat.mod == piano_hat.MOD_KEY and machine.channels[piano_hat.channel].type == 'synth':
        if machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()][piano_hat.step] is None:
            machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()][piano_hat.step] = {"note": []}
        if machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()][piano_hat.step]["note"].index(piano_hat.midi_note(key)) is not None:
            machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()][piano_hat.step]["note"].remove(piano_hat.midi_note(key))
            return
        machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()][piano_hat.step]["note"].append(piano_hat.midi_note(key))


## INSTRUMENT
### CHANNEL
def on_instrument_channel(key: int, event: bool):
    piano_hat.layout = piano_hat.LAYOUT_PATTERN
    if len(machine.channels[piano_hat.channel].patterns) <= piano_hat.get_pattern():
        for i in range(piano_hat.get_pattern()+1):
            if len(machine.channels[piano_hat.channel].patterns) <= i:
                machine.channels[piano_hat.channel].patterns.insert(i, [None for _ in range(8) ])
                machine.channels[piano_hat.channel].sleeps.insert(i, [0.25 for _ in range(8) ])
### PATTERN
def on_instrument_pattern(key: int, event: bool):
    piano_hat.layout = piano_hat.LAYOUT_CHANNEL
    osc_sender.send_message('/channel/json', [piano_hat.channel, json.dumps(machine.channels[piano_hat.channel].__dict__)])
## STEP
def on_instrument_step(key: int, event: bool):
    piano_hat.layout = piano_hat.LAYOUT_PATTERN
    osc_sender.send_message('/channel/json', [piano_hat.channel, json.dumps(machine.channels[piano_hat.channel].__dict__)])




# LED HANDLER
def leds_off():
    for i in range(16):
        pianohat.set_led(i, False)
def leds_on():
    for i in range(16):
        pianohat.set_led(i, True)
def leds_channel_on():
    pianohat.set_led(piano_hat.BLACK_KEYS[piano_hat.pattern[0]], True)
    pianohat.set_led(piano_hat.WHITE_KEYS[piano_hat.pattern[1]], True)
def leds_pattern_on(pattern):
    if len(pattern) > 0:
        for step in range(len(pattern)):
            if step is not None:
                pianohat.set_led(piano_hat.WHITE_KEYS[step], True)
                continue
            pianohat.set_led(step, False)
def leds_step_on(step):
    if step.get("note") is not None:
        for i, note in enumerate(step.get("note")):
            if none is not None:
                k_l = [piano_hat.WHITE_KEYS] + [piano_hat.BLACK_KEYS]
                pianohat.set_led(k_l[k_l.index(((piano_hat.octave)*12-note))*(-1)], True)
                continue
            pianohat.set_led(k_l[k_l.index(((piano_hat.octave)*12-note))*(-1)], False)




# PIANOHAT PCB INIT
leds_off()
leds_on()
leds_off()
pianohat.auto_leds(False)
pianohat.on_instrument(lambda key, event: piano_hat.handle_instrument(key, event, machine))
pianohat.on_note(lambda key, event: piano_hat.handle_note(key, event, machine))
pianohat.on_octave_up(lambda key, event: piano_hat.handle_octave_up(key, event, machine))
pianohat.on_octave_down(lambda key, event: piano_hat.handle_octave_down(key, event, machine))

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
        machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()][piano_hat.step]['note'].append(piano_hat.midi_note(key))
        return
    if piano_hat.layout == piano_hat.LAYOUT_NOTE and pressed:
        if machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()][piano_hat.step] is None:
            machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()][piano_hat.step] = {"note": []}
        machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()][piano_hat.step]['note'].append(piano_hat.midi_note(key))


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
