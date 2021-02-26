from pythonosc import osc_message_builder
from pythonosc import udp_client
import time
import json
import sys
import random

sender = udp_client.SimpleUDPClient('127.0.0.1', 4560)

# sender.send_message('/settings', ['pmax', 1])

instrus = []

bpm = 60
bar = 4
eighth = 4
pmax = 1

def show(instrus):
    print('#########################\tBPM\t'+str(bpm))
    print('##        PiSON        ##\tBAR\t'+str(bar))
    print('#########################\tEIGHTH\t'+str(eighth))
    print('                         \tPMAX\t'+str(pmax))
    print('')
    for i, instru in enumerate(instrus):
        s = "["+str(i)+"] "
        if instru['type'] == 'synth':
            for p in instru['patterns']:
                s = s+'| '
                for ss in p:
                    if ss == None :
                        s = s+'---- '
                    else:
                        s = s+ss+'- '
            s = s+"\t"+instru['type']+' : '+instru['synth']+' '+str(instru['opts'])

        if instru['type'] == 'sample':
            for p in instru['patterns']:
                s = s+'| '
                for ss in p:
                    if ss == None :
                        s = s+'---- '
                    else:
                        s = s+'-X-- '
            s = s+"\t"+instru['type']+' : '+instru['sample']+' '+str(instru['opts'])
        time.sleep(0.5)
        print(s)
        s = "["+str(i)+"] "
        for st in instru['steps']:
            s = s+'| '
            for ss in st:
                if ss == None :
                    s = s+'---- '
                else:
                    s = s+str(ss)+' '
        s = s+"\t"+'steps'
        print(s)
        print('')
while True:
    show(instrus)
    print('Feature (0 : channel, 1 : settings) : ')
    feature = input()
    if feature == 'quit' or feature == 'q':
        exit()

    if int(feature) == 0:
        print('Channel : ')
        channel = input()
        if channel == 'quit' or channel == 'q':
            continue
        channel = int(channel)
        print('Type (0 : synth, 1 : sample) : ')
        type = int(input())

        if type == 0:
            type = 'synth'
        if type == 1:
            type = 'sample'

        # SYNTH
        if type == 'synth':
            print('Synth : ')
            name = input()

            if channel >= len(instrus):
                instrus.insert(channel, {})
                instrus[channel] = {
                    # "type": type,
                    # "synth": name,
                    "opts": {
                    },
                    "fxs": {
                    },
                    "patterns": [
                    ],
                    "steps": [
                    ]
                }
            instrus[channel]['type'] = type
            instrus[channel]['synth'] = name
            print('Pattern : ')
            pattern = input()

            while pattern != 'quit' and pattern != 'q':
                print(instrus[channel])
                if pattern != '':
                    for i in range(int(pattern)+1):
                        if int(i) >= len(instrus[channel]['patterns']):
                            instrus[channel]['patterns'].insert(int(i), [])

                        if int(i) >= len(instrus[channel]['steps']):
                            instrus[channel]['steps'].insert(int(i), [])
                else:
                    pattern = len(instrus[channel]['patterns'])
                    instrus[channel]['patterns'].append([])
                    instrus[channel]['steps'].append([])
                print('Position : ')
                position = input()
                while position != 'quit' and position != 'q':
                    print(instrus[channel])
                    if position != '':
                        for i in range(int(position)+1):
                            if int(i) >= len(instrus[channel]['patterns'][int(pattern)]):
                                instrus[channel]['patterns'][int(pattern)].insert(int(i), None)

                            if int(i) >= len(instrus[channel]['steps'][int(pattern)]):
                                instrus[channel]['steps'][int(pattern)].insert(int(i), 0.25)
                    else:
                        position = len(instrus[channel]['patterns'][int(pattern)])
                        instrus[channel]['patterns'][int(pattern)].append(None)
                        instrus[channel]['steps'][int(pattern)].append(0.25)

                    print('Note : ')
                    note = input()
                    if note == 'n':
                        instrus[channel]['patterns'][int(pattern)][int(position)] = None
                    elif note != '':
                        instrus[channel]['patterns'][int(pattern)][int(position)] = note

                    instrus[channel]['steps'][int(pattern)][int(position)] = 0.25

                    print('Position : ')
                    position = input()

                print('Pattern : ')
                pattern = input()

        if type == 'sample':
            print('Sample : ')
            name = input()

            if channel >= len(instrus):
                instrus.insert(channel, {})
                instrus[channel] = {
                    # "type": type,
                    # "sample": name,
                    "opts": {
                    },
                    "fxs": {
                    },
                    "patterns": [
                    ],
                    "steps": [
                    ]
                }
            instrus[channel]['type'] = type
            instrus[channel]['sample'] = name
            print('Pattern : ')
            pattern = input()

            while pattern != 'quit' and pattern != 'q':
                if pattern != '':
                    for i in range(int(pattern)+1):
                        if int(i) >= len(instrus[channel]['patterns']):
                            instrus[channel]['patterns'].insert(int(i), [])

                        if int(i) >= len(instrus[channel]['steps']):
                            instrus[channel]['steps'].insert(int(i), [])
                else:
                    pattern = len(instrus[channel]['patterns'])
                    instrus[channel]['patterns'].append([])
                    instrus[channel]['steps'].append([])
                print('Position : ')
                position = input()
                while position != 'quit' and position != 'q':
                    if position != '':
                        for i in range(int(position)+1):
                            if int(i) >= len(instrus[channel]['patterns'][int(pattern)]):
                                instrus[channel]['patterns'][int(pattern)].insert(int(i), None)

                            if int(i) >= len(instrus[channel]['steps'][int(pattern)]):
                                instrus[channel]['steps'][int(pattern)].insert(int(i), 0.25)
                    else:
                        position = len(instrus[channel]['patterns'][int(pattern)])
                        instrus[channel]['patterns'][int(pattern)].append(None)
                        instrus[channel]['steps'][int(pattern)].append(0.25)

                    print('Note : ')
                    note = input()
                    if note == 'n':
                        instrus[channel]['patterns'][int(pattern)][int(position)] = None
                    elif note != '':
                        instrus[channel]['patterns'][int(pattern)][int(position)] = True

                    instrus[channel]['steps'][int(pattern)][int(position)] = 0.25

                    print('Position : ')
                    position = input()

                print('Pattern : ')
                pattern = input()

    # SETTINGS
    if int(feature) == 1:
        print('Setting :')
        setting = input()
        while setting != 'quit' and setting != 'q':
            print('Value :')
            value = input()
            if value != '':
                sender.send_message('/settings', [setting, int(value)])
            print('Setting :')
            setting = input()

    # OPTIONS
    if int(feature) == 2:
        print('Channel : ')
        channel = input()
        while channel != 'quit' and channel != 'q':
            type = instrus[int(channel)]['type']
            print('Option : ')
            option = input()
            while option != 'quit' and option != 'q':
                print('Value : ')
                value = input()
                if value == 'del':
                    if option in instrus[int(channel)]['opts']:
                        del(instrus[int(channel)]['opts'][option])
                elif value != "":
                    sender.send_message('/channel/options', [type+'_'+channel, json.dumps({option: float(value)})])
                    instrus[int(channel)]['opts'][option] = float(value)
                print('Option : ')
                option = input()

            print('Channel : ')
            channel = input()


    # OPTIONS
    # if feature == 3:

    sender.send_message('/channels', [json.dumps(instrus)])
    sender.send_message('/state', ['play'])

    continue
