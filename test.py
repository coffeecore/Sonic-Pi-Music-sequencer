from pythonosc import osc_message_builder
from pythonosc import udp_client
import time
import json

sender = udp_client.SimpleUDPClient('127.0.0.1', 4560)

sender.send_message('/debug', [1])
time.sleep(0.2)

sender.send_message('/metronome', [1])
time.sleep(0.2)

sender.send_message('/bpm', [60])
time.sleep(0.25)

sender.send_message('/start', [1])
time.sleep(3)

instrus = [
    {
        'type': 'synth',
        'name': 'fm',
        'fxs': [
            {
                'name': 'reverb',
                'opts' : {
                    'mix': 1,
                    'room': 1
                }
            }
        ],
        'opts': {
            # 'release': 0.01,
            # 'amp': 0.75,
            # 'attack': 0.1,
            # 'res': 0
        },
        'steps': [None, None, ':c4', ':e4', None, None, ':g4', ':c4', None, ':e4', None, None, ':c4', None, ':g4', None]
    },
    {
        'type': 'sample',
        'name': 'drum_cymbal_closed',
        'fxs': [],
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
    {
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
    {
        'type': 'sample',
        'name': 'sn_dub',
        'fxs': [],
        'opts': {
            # 'release': 1,
            # 'amp': 5,
            # 'attack': 1,
            # 'res': 0,
            # 'pan': -1
        },
        'steps': [
            None, None, None, None, 
            1, None, None, None, 
            None, None, None, None, 
            1, None, None, None
        ]
    }
]

for k in range(len(instrus)) :
    print([instrus[k]['type'], instrus[k]['name']])
    print(instrus[k])
    if k == 0 :
        sender.send_message('/instru/add/complete', [json.dumps(instrus[k])])
        time.sleep(0.25)
        continue
    sender.send_message('/instru/add', [instrus[k]['type'], instrus[k]['name']])
    time.sleep(0.25)
    # exit()

    for kk in range(len(instrus[k]['steps'])):
        if instrus[k]['steps'][kk] is not None :
            print([k, kk, instrus[k]['steps'][kk]])
            sender.send_message('/instru/step/add', [k, kk, instrus[k]['steps'][kk]])
            time.sleep(0.25)

time.sleep(5)

# for k in range(len(instrus)) :
#     opts = [k]
#     for kk, v in instrus[k]['opts'].items() :
#         opts.append(kk)
#         opts.append(v)
#     print(opts)
#     sender.send_message('/instru/options/change', opts)
#     time.sleep(0.25)

# time.sleep(5)

# for k in range(len(instrus)) :
#     fxs = [k]
#     for kk in range(len(instrus[k]['fxs'])) :
#         fxs.append(instrus[k]['fxs'][kk]['name'])
#         for k, vv  in instrus[k]['fxs'][kk].items() :
#             if k == 'name' :
#                 continue
#             fxs.append(k)
#             fxs.append(vv)
#         print(fxs)
#         sender.send_message('/instru/fx/add', fxs)
#         time.sleep(0.25)

# time.sleep(5)
# sender.send_message('/instru/fx/change', [0, 0, 'room', 0.5])
# time.sleep(5)

for k in range(len(instrus)) :
    for kk in range(len(instrus[k]['fxs'])) :
        print([k, kk])
        sender.send_message('/instru/fx/remove', [k, kk])
        time.sleep(0.25)

# time.sleep(3)

# for k in range(len(instrus)) :
#     print([k])
#     sender.send_message('/instru/options/remove/all', [k])
#     time.sleep(0.25)
