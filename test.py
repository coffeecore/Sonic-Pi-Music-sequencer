from pythonosc import osc_message_builder
from pythonosc import udp_client
import time

sender = udp_client.SimpleUDPClient('127.0.0.1', 4560)

sender.send_message('/debug', [1])
time.sleep(0.2)

sender.send_message('/metronome', [1])
time.sleep(0.2)

sender.send_message('/bpm', [100])
time.sleep(0.25)

sender.send_message('/start', [1])
time.sleep(3)

instrus = {
    0: {
        'type': 'synth',
        'name': 'pretty_bell',
        'fxs': [],
        'opts': {
            'release': 0.01,
            'amp': 0.75,
            'attack': 0.1,
            'res': 0
        },
        'steps': [None, None, ':c4', ':e4', None, None, ':g4', ':c4', None, ':e4', None, None, ':c4', None, ':g4', None]
    },
    1: {
        'type': 'sample',
        'name': 'drum_cymbal_closed',
        'fxs': [
            {
                'name': 'reverb',
                'mix': 1,
                'room': 1
            }
        ],
        'opts': {
            'release': 1,
            'amp': 5,
            'attack': 1,
            'res': 0
        },
        'steps': [
        1, None, 1, None, 
        1, None, 1, None, 
        1, None, 1, None, 
        1, None, 1, None]
    },
    2: {
        'type': 'sample',
        'name': 'drum_bass_hard',
        'fxs':[],
        'opts': {
            'release': 1,
            'amp': 5,
            'attack': 1,
            'res': 0
        },
        'steps': [
            1, None, None, None, 
            None, None, None, None, 
            1, None, None, None, 
            None, None, 1, None
        ]
    },
    3: {
        'type': 'sample',
        'name': 'sn_dub',
        'fxs': [],
        'opts': {
            'release': 1,
            'amp': 5,
            'attack': 1,
            'res': 0
        },
        'steps': [
            None, None, None, None, 
            1, None, None, None, 
            None, None, None, None, 
            1, None, None, None
        ]
    }
}

for k, i in instrus.items() :
    print([i['type'], k, i['name']])
    sender.send_message('/instru/add', [i['type'], k, i['name']])
    time.sleep(0.25)
    for kk in range(len(i['steps'])):
        if i['steps'][kk] is not None :
            sender.send_message('/instru/step/add', [k, kk, i['steps'][kk]])
            time.sleep(0.25)

time.sleep(3)

for k, i in instrus.items() :
    opts = [k]
    for kk, v in i['opts'].items() :
        opts.append(kk)
        opts.append(v)
    sender.send_message('/instru/options/add', opts)
    time.sleep(0.25)

time.sleep(3)

for k, i in instrus.items() :
    for kk in range(len(i['fxs'])) :
        fxs = [k]
        for vv in i['fxs'][kk] :
            fxs.append(vv)
        sender.send_message('/instru/fx/add', fxs)
        time.sleep(0.25)

time.sleep(3)

for k, i in instrus.items() :
    for kk in range(len(i['fxs'])) :
        sender.send_message('/instru/fx/remove', [k, kk])
        time.sleep(0.25)

time.sleep(3)

for k, i in instrus.items() :
    sender.send_message('/instru/options/remove/all', [k])
    time.sleep(0.25)



# sender.send_message('/instru/remove', [0])
# time.sleep(0.2)
# sender.send_message('/instru/remove', [1])
# time.sleep(0.2)
# sender.send_message('/instru/remove', [2])
# time.sleep(0.2)
# sender.send_message('/instru/remove', [3])
# time.sleep(0.2)

# sender.send_message('/instru/add', ['synth', 3, 'fm'])
# time.sleep(0.25)
# # sender.send_message('/instru/change', ['synth', 3, 'fm'])
# # time.sleep(0.25)
# sender.send_message('/instru/options/change', [3, 'release', 0.01, 'amp', 0.75, 'attack', 0.1, 'res', 0])
# # time.sleep(0.25)
# sender.send_message('/instru/step/add', [3, 2, ':c4'])
# time.sleep(3)
# sender.send_message('/instru/options/change', [3, 'release', 0.01, 'amp', 0.75, 'attack', 0.1, 'res', 0])
# time.sleep(3)

# sender.send_message('/instru/step/add', [3, 3, ':e4'])
# time.sleep(0.25)
# sender.send_message('/instru/step/add', [3, 6, ':g4'])
# time.sleep(0.25)
# sender.send_message('/instru/step/add', [3, 7, ':c4'])
# time.sleep(0.25)
# sender.send_message('/instru/step/add', [3, 9, ':e4'])
# time.sleep(0.25)
# sender.send_message('/instru/step/add', [3, 12, ':c4'])
# time.sleep(0.25)
# sender.send_message('/instru/step/add', [3, 14, ':g4'])
# time.sleep(0.25)

# sender.send_message('/instru/add', ['sample', 0, 'drum_tom_mid_hard'])
# time.sleep(0.2)
# sender.send_message('/instru/change', ['sample', 0, 'drum_bass_hard'])
# time.sleep(0.2)
# sender.send_message('/instru/step/add', [0, 0, 1])
# time.sleep(0.2)
# sender.send_message('/instru/step/add', [0, 8, 1])
# time.sleep(0.2)
# sender.send_message('/instru/step/add', [0, 14, 1])
# time.sleep(0.2)

# sender.send_message('/instru/add', ['sample', 1, 'drum_cymbal_closed'])
# time.sleep(0.2)
# for i in range(0,8):
#     sender.send_message('/instru/step/add', [1, i*2, 1])
#     time.sleep(0.2)



# sender.send_message('/instru/add', ['sample', 2, 'drum_snare_hard'])
# time.sleep(0.2)
# sender.send_message('/instru/step/add', [2, 4, 1])
# time.sleep(0.2)
# sender.send_message('/instru/step/add', [2, 12, 1])
# time.sleep(0.2)


# time.sleep(3)

# sender.send_message('/instru/step/remove', [0, 3])
# time.sleep(0.2)
# sender.send_message('/instru/options/remove', [1, 'release'])
# time.sleep(0.2)
# sender.send_message('/instru/fx/add', [3, 'reverb', 'mix', 1, 'room', 1])
# # time.sleep(3)
# # sender.send_message('/instru/options/remove/all', [3])
# time.sleep(3)

# # time.sleep(3)
# sender.send_message('/instru/fx/remove', [3, 0])
# time.sleep(0.2)

# sender.send_message('/instru/remove', [0])

# sender.send_message('/instru/fx/add', [0, 0, 'reverb', 'mix', 1, 'room', 1])
# time.sleep(0.2)
# sender.send_message('/eighth', [2])
# time.sleep(3)

# sender.send_message('/eighth', [4])
