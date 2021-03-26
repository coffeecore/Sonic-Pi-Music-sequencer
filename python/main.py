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


with open('./config.json') as json_file:
    config = json.load(json_file)


# OSC init
osc_sender = udp_client.SimpleUDPClient(config['osc']['host'], config['osc']['port'])

## Machine init
machine = Machine()
machine.bpm    = config['machine']['bpm']
machine.pmax   = config['machine']['pmax']
machine.bar    = config['machine']['bar']
machine.eighth = config['machine']['eighth']
osc_sender.send_message('/settings', ['bar', machine.bar])
osc_sender.send_message('/settings', ['pmax', machine.pmax])

## Channels init
for ch in config['channels']:
    channel = Channel(ch['type'], ch['name'])
    if ch.get('options') is not None:
        channel.options = ch['options']
    if ch.get('fxs') is not None:
        channel.fxs = ch['fxs']
    machine.add_channel(channel)

## PianoHAT init
piano_hat = PianoHat()

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
    if (piano_hat.layout == piano_hat.LAYOUT_STEP or piano_hat.layout == piano_hat.LAYOUT_MIDI) and pressed:
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
    if (piano_hat.layout == piano_hat.LAYOUT_STEP or piano_hat.layout == piano_hat.LAYOUT_MIDI) and pressed:
        on_octave_down_step(key, pressed)
        return
## NOTE
def handle_note(key: int, pressed: bool):
    print_info('note '+str(key))
    if piano_hat.layout == piano_hat.LAYOUT_CHANNEL and pressed:
        on_note_channel(key, pressed)
        return
    if piano_hat.layout == piano_hat.LAYOUT_PATTERN and pressed:
        on_note_pattern(key, pressed)
        return
    if piano_hat.layout == piano_hat.LAYOUT_STEP and pressed:
        on_note_step(key, pressed)
        return
    if piano_hat.layout == piano_hat.LAYOUT_MIDI:
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
        piano_hat.channel = 0
## PATTERN
def on_octave_up_pattern(key: int, pressed: bool):
    piano_hat.layout = piano_hat.LAYOUT_MIDI
    piano_hat.mod = piano_hat.MOD_LIVE
    leds_off()
    pianohat.set_led(14, True)
## STEP
def on_octave_up_step(key: int, pressed: bool):
    if piano_hat.octave < 10:
        piano_hat.octave += 1
    else :
        piano_hat.octave = 0
    if piano_hat.mod == piano_hat.MOD_KEY and machine.channels[piano_hat.channel].type == 'synth':
        leds_step_on(machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()][piano_hat.get_step()])


## OCTAVE DOWN
### CHANNEL
def on_octave_down_channel(key: int, pressed: bool):
    if piano_hat.channel == 0:
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
        leds_pattern_on(machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()])
## STEP
def on_octave_down_step(key: int, pressed: bool):
    if piano_hat.octave == 0:
        piano_hat.octave = 10
    else:
        piano_hat.octave -= 1
    if piano_hat.mod == piano_hat.MOD_KEY and machine.channels[piano_hat.channel].type == 'synth':
        leds_step_on(machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()][piano_hat.get_step()])


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
    if piano_hat.BLACK_KEYS.count(key) != 0 and key != 10:
        piano_hat.step[0] = piano_hat.BLACK_KEYS.index(key)
        leds_pattern_on(machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()])
    elif machine.channels[piano_hat.channel].type == 'sample' or machine.channels[piano_hat.channel].type == 'external_sample':
        if piano_hat.WHITE_KEYS.count(key) != 0:
            if machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()][piano_hat.WHITE_KEYS.index(key)] is None:
                on_note_pattern_sample(key, pressed)
            else:
                machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()][piano_hat.WHITE_KEYS.index(key)] = None
            leds_pattern_on(machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()])
            pianohat.set_led(15, True)
    elif machine.channels[piano_hat.channel].type == 'synth':
        if key == 10: # Last black key
            piano_hat.layout = piano_hat.LAYOUT_STEP
            piano_hat.mod = piano_hat.MOD_REC
            piano_hat.step[1] = 0
            pianohat.set_led(13, True)
        else:
            on_note_pattern_synth(key, pressed)
def on_note_pattern_sample(key: int, pressed: bool):
    machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()][piano_hat.WHITE_KEYS.index(key)] = {**{}, **machine.channels[piano_hat.channel].options}
    leds_pattern_on(machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()])
    pianohat.set_led(15, True)
def on_note_pattern_synth(key: int, pressed: bool):
    piano_hat.layout = piano_hat.LAYOUT_STEP
    piano_hat.step[1] = piano_hat.WHITE_KEYS.index(key)
    leds_step_on(machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()][piano_hat.get_step()])
## STEP
def on_note_step(key: int, pressed: bool):
    if piano_hat.mod == piano_hat.MOD_REC and machine.channels[piano_hat.channel].type == 'synth':
        if piano_hat.step[1] < 8:
            pianohat.set_led(13, False)
            time.sleep(0.05)
            pianohat.set_led(13, True)
            note = piano_hat.key_to_midi_note(key)
            osc_sender.send_message('/channel/play', [piano_hat.channel, note])
            machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()][piano_hat.get_step()] = {"note": [note]}
            piano_hat.step[1] = piano_hat.step[1] + 1
            return
        # Back to layout pattern and mod key after 8 notes type
        piano_hat.step[1] = 0
        piano_hat.layout = piano_hat.LAYOUT_PATTERN
        pianohat.set_led(13, False)
        piano_hat.mod = piano_hat.MOD_KEY
        osc_sender.send_message('/channel/json', [piano_hat.channel, json.dumps(machine.channels[piano_hat.channel].__dict__)])
        leds_pattern_on(machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()])
        pianohat.set_led(15, True)
        return
    if piano_hat.mod == piano_hat.MOD_KEY and machine.channels[piano_hat.channel].type == 'synth':
        if machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()][piano_hat.get_step()] is None:
            machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()][piano_hat.get_step()] = {**{"note": []}, **machine.channels[piano_hat.channel].options}
        if machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()][piano_hat.get_step()]["note"].count(piano_hat.key_to_midi_note(key)) != 0:
            machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()][piano_hat.get_step()]["note"].remove(piano_hat.key_to_midi_note(key))
            if len(machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()][piano_hat.get_step()]["note"]) == 0:
                machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()][piano_hat.get_step()] = None
        else :
            note = piano_hat.key_to_midi_note(key)
            machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()][piano_hat.get_step()]["note"].append(note)
            # osc_sender.send_message('/channel/play', [piano_hat.channel, note])
        leds_step_on(machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()][piano_hat.get_step()])
## MIDI
def on_note_midi(key: int, pressed: bool):
    if pressed:
        pianohat.set_led(key, True)
        time.sleep(0.01)
        pianohat.set_led(key, False)
    note = 0
    if machine.channels[piano_hat.channel].type == 'synth':
        note = piano_hat.key_to_midi_note(key)
    if pressed:
        osc_sender.send_message('/channel/play/on', [piano_hat.channel, note])
    else:
        osc_sender.send_message('/channel/play/off', [piano_hat.channel, note])


## INSTRUMENT
### CHANNEL
def on_instrument_channel(key: int, pressed: bool):
    piano_hat.layout = piano_hat.LAYOUT_PATTERN
    if len(machine.channels[piano_hat.channel].patterns) <= piano_hat.get_pattern():
        for i in range(piano_hat.get_pattern()+1):
            if len(machine.channels[piano_hat.channel].patterns) <= i:
                machine.channels[piano_hat.channel].patterns.insert(i, [None for _ in range(8) ])
                machine.channels[piano_hat.channel].sleeps.insert(i, [0.25 for _ in range(8) ])
    leds_pattern_on(machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()])
    pianohat.set_led(15, True)
### PATTERN
def on_instrument_pattern(key: int, pressed: bool):
    piano_hat.layout = piano_hat.LAYOUT_CHANNEL
    osc_sender.send_message('/channel/json', [piano_hat.channel, json.dumps(machine.channels[piano_hat.channel].__dict__)])
    leds_channel_on()
## STEP
def on_instrument_step(key: int, pressed: bool):
    piano_hat.layout = piano_hat.LAYOUT_PATTERN
    pianohat.set_led(13, False)
    piano_hat.mod = piano_hat.MOD_KEY
    osc_sender.send_message('/channel/json', [piano_hat.channel, json.dumps(machine.channels[piano_hat.channel].__dict__)])
    leds_pattern_on(machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()])
    pianohat.set_led(15, True)
## NOTE
def on_instrument_midi(key: int, pressed: bool):
    piano_hat.layout = piano_hat.LAYOUT_PATTERN
    piano_hat.mod = piano_hat.MOD_KEY
    pianohat.set_led(14, False)
    leds_pattern_on(machine.channels[piano_hat.channel].patterns[piano_hat.get_pattern()])
    pianohat.set_led(15, True)


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
        pianohat.set_led(piano_hat.BLACK_KEYS[piano_hat.step[0]], True)
        for i, step in enumerate(pattern):
            if step is not None:
                pianohat.set_led(piano_hat.WHITE_KEYS[i], True)
            else:
                pianohat.set_led(piano_hat.WHITE_KEYS[i], False)
def leds_step_on(step):
    leds_off()
    if step is not None and step.get("note") is not None:
        for i, note in enumerate(step.get("note")):
            if note is not None:
                k_l = piano_hat.WHITE_KEYS + piano_hat.BLACK_KEYS
                if k_l.count(piano_hat.midi_note_to_key(note)) != 0:
                    pianohat.set_led(k_l[k_l.index(piano_hat.midi_note_to_key(note))], True)
            # pianohat.set_led(k_l[k_l.index(piano_hat.midi_note_to_key(note))], False)

# MISC FUNCTIONS
def print_info(key_string: str):
    print('##########################')
    print('## Sonic Pi - Piano HAT ##')
    print('##########################')
    print('KEY : '+key_string)
    print('LAYOUT : '+str(piano_hat.layout))
    print(piano_hat.get_layout())
    print('MOD : '+str(piano_hat.mod))
    print(piano_hat.get_mod())
    print('CHANNEL : '+str(piano_hat.channel))
    print(machine.channels[piano_hat.channel].type+' : '+machine.channels[piano_hat.channel].name)
    print('OCTAVE : '+str(piano_hat.octave))
    print('PATTERN : '+str(piano_hat.get_pattern()))
    print('STEP : '+str(piano_hat.get_step()))
    print('PATTERNS : '+str(machine.channels[piano_hat.channel].patterns))
    print('##########################')
    print()

def signal_handler(signal, frame):
  leds_off()
  print()
  sys.exit(0)

# PIANOHAT PCB INIT
pianohat.auto_leds(False)
pianohat.on_instrument(handle_instrument)
pianohat.on_note(handle_note)
pianohat.on_octave_up(handle_octave_up)
pianohat.on_octave_down(handle_octave_down)
leds_off()
leds_on(0.01)
leds_off()
leds_channel_on()

signal.signal(signal.SIGINT, signal_handler)
signal.pause()
