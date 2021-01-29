from pythonosc import osc_message_builder
from pythonosc import udp_client
import time
import json

sender = udp_client.SimpleUDPClient('127.0.0.1', 4560)

sender.send_message('/debug', [1])
time.sleep(0.2)

sender.send_message('/metronome', [0])
time.sleep(0.2)

sender.send_message('/bpm', [150])
time.sleep(0.2)

sender.send_message('/start', [1])
time.sleep(0.2)

sender.send_message('/pattern/max', [2])
time.sleep(0.2)

# exit()
# instrus = [
#     {
#         'type': 'synth',
#         'name': 'fm',
#         'fxs': [
#             # {
#             #     'name': 'reverb',
#             #     'opts' : {
#             #         'mix': 1,
#             #         'room': 1
#             #     }
#             # },
#             # {
#             #     'name': 'slicer',
#             #     'opts': {
#             #         'wave': 0,
#             #         'phase': 0.25
#             #     }
#             # }
#         ],
#         'opts': {
#             # 'release': 0.01,
#             # 'amp': 0.75,
#             # 'attack': 0.1,
#             # 'res': 0
#         },
#         'patterns': [
#             [None, None, ':c4', ':e4', None, None, ':g4', ':c4', None, ':e4', None, None, ':c4', None, ':g4', None],
#             # [None, None, ':c2', ':e2', None, None, ':g2', ':c2', None, [':e2', ':e4'], None, None, 'chord(:E3, :minor)', None, ':g2', None]
#         ]
#     },
#     {
#         'type': 'sample',
#         'name': 'drum_cymbal_closed',
#         'fxs': [],
#         'opts': {
#             'release': 1,
#             'amp': 5,
#             'attack': 1,
#             'res': 0
#         },
#         'patterns': [
#             [
#                 1, None, 1, None, 
#                 1, None, 1, None, 
#                 1, None, 1, None, 
#                 1, None, 1, None
#             ],
#             [
#                 1, None, 1, None, 
#                 1, None, 1, None, 
#                 1, None, 1, None, 
#                 1, None, 1, None
#             ]
#         ]
#     },
#     # {
#     #     'type': 'sample',
#     #     'name': 'drum_bass_hard',
#     #     'fxs':[],
#     #     'opts': {
#     #         # 'release': 1,
#     #         # 'amp': 5,
#     #         # 'attack': 1,
#     #         # 'res': 0
#     #     },
#     #     'patterns': [
#     #         [
#     #             1, None, None, None, 
#     #             None, None, None, None, 
#     #             1, None, None, None, 
#     #             None, None, 1, None
#     #         ],
#     #         [
#     #             1, None, None, None, 
#     #             None, None, None, None, 
#     #             1, None, None, None, 
#     #             None, None, 1, None
#     #         ]
#     #     ]
#     # },
#     # {
#     #     'type': 'sample',
#     #     'name': 'sn_dub',
#     #     'fxs': [
#     #         # {
#     #         #     'name': 'reverb',
#     #         #     'opts' : {
#     #         #         'mix': 0.5,
#     #         #         'room': 0.5
#     #         #     }
#     #         # }
#     #     ],
#     #     'opts': {
#     #         # 'release': 1,
#     #         # 'amp': 5,
#     #         # 'attack': 1,
#     #         # 'res': 0,
#     #         # 'pan': -1
#     #     },
#     #     'patterns': [
#     #         [
#     #             None, None, None, None, 
#     #             1, None, None, None, 
#     #             None, None, None, None, 
#     #             1, None, None, None
#     #         ],
#     #         [
#     #             None, None, None, None, 
#     #             1, None, None, None, 
#     #             None, None, None, None, 
#     #             1, None, None, None
#     #         ]
#     #     ]
#     # }
# ]
instrus = [
    {
        'type': 'synth',
        'name': ':tb303',
        'opts': {
            'release': 1,
            'cutoff': 100
        },
        'fxs': {
            # ':reverb': {
            #     'mix': 0.5,
            #     'room': 1
            # },
            ':distortion': {
                'distort': 0.999
            }
        },
        'patterns': [
            [':e1', None, ':e3', None, ':e1', None, ':e3', None, ':e1', None, ':e3', None, ':e1', None, ':e3', None],
            # ['[:f2, :f4]', None, 'chord(:e, :major)', None]
            [[':f2', ':f4'], None, 'chord(:E3, :major)', None, [':f2', ':f4'], None, 'chord(:E3, :major)', None, [':f2', ':f4'], None, 'chord(:E3, :major)', None, [':f2', ':f4'], None, 'chord(:E3, :major)', None]
        ]
    },
    {
        'type': 'sample',
        'name': ':bd_tek',
        'opts': {
            'release': 1,
            'cutoff': 100
        },
        'fxs': {
            # ':reverb': {
            #     'mix': 0.5,
            #     'room': 1
            # },
            ':distortion': {
                'distort': 0.999
            }
        },
        'patterns': [
            [1, None, 1, None, 1, None, 1, None, 1, None, 1, None, 1, None, 1, None],
            # ['[:f2, :f4]', None, 'chord(:e, :major)', None]
            [1, None, 1, None, 1, None, 1, None, 1, None, 1, None, 1, None, 1, None],
        ]
    }
]
sender.send_message('/json', [json.dumps(instrus)])
time.sleep(5)
instrus = [
    {
        'type': 'synth',
        'name': ':tb303',
        'opts': {
            'release': 1,
            'cutoff': 130
        },
        'fxs': {
            # ':reverb': {
            #     'mix': 1,
            #     'room': 1
            # },
            ':distortion': {
                'distort': 0.1
            }
        },
        'patterns': [
            [':e1', None, ':e3', None, ':e1', None, ':e3', None, ':e1', None, ':e3', None, ':e1', None, ':e3', None],
            # ['[:f2, :f4]', None, 'chord(:e, :major)', None]
            [[':f2', ':f4'], None, 'chord(:E3, :major)', None, [':f2', ':f4'], None, 'chord(:E3, :major)', None, [':f2', ':f4'], None, 'chord(:E3, :major)', None, [':f2', ':f4'], None, 'chord(:E3, :major)', None]
        ]
    }
]
sender.send_message('/json', [json.dumps(instrus)])
time.sleep(5)
instrus = [
    {
        'type': 'synth',
        'name': ':tb303',
        'opts': {
            'release': 1,
            'cutoff': 100
        },
        'fxs': {
            # ':reverb': {
            #     'mix': 0.5,
            #     'room': 1
            # },
            ':distortion': {
                'distort': 0.999
            }
        },
        'patterns': [
            [':e1', None, ':e3', None, ':e1', None, ':e3', None, ':e1', None, ':e3', None, ':e1', None, ':e3', None],
            # ['[:f2, :f4]', None, 'chord(:e, :major)', None]
            [[':f2', ':f4'], None, 'chord(:E3, :major)', None, [':f2', ':f4'], None, 'chord(:E3, :major)', None, [':f2', ':f4'], None, 'chord(:E3, :major)', None, [':f2', ':f4'], None, 'chord(:E3, :major)', None]
        ]
    },
    {
        'type': 'sample',
        'name': ':bd_tek',
        'opts': {
            'release': 1,
            'cutoff': 100
        },
        'fxs': {
            # ':reverb': {
            #     'mix': 0.5,
            #     'room': 1
            # },
            ':distortion': {
                'distort': 0.999
            }
        },
        'patterns': [
            [1, None, 1, None, 1, None, 1, None, 1, None, 1, None, 1, None, 1, None],
            # ['[:f2, :f4]', None, 'chord(:e, :major)', None]
            [1, None, 1, None, 1, None, 1, None, 1, None, 1, None, 1, None, 1, None],
        ]
    }
]
sender.send_message('/json', [json.dumps(instrus)])

exit()
time.sleep(4)

instrus = [
    {
        'type': 'synth',
        'name': 'fm',
        'fxs': [
            {
                'name': 'distortion',
                'opts': {
                    'distort': 0.999
                }
            }
            # {
            #     'name': 'reverb',
            #     'opts' : {
            #         'mix': 0.5,
            #         'room': 1
            #     }
            # },
            # {
            #     'name': 'slicer',
            #     'opts': {
            #         'wave': 0,
            #         'phase': 0.5
            #     }
            # }
        ],
        'opts': {
            # 'release': 0.01,
            # 'amp': 0.75,
            # 'attack': 0.1,
            # 'res': 0
        },
        'patterns': [
            [None, None, ':c4', ':e4', None, None, ':g4', ':c4', None, ':e4', None, None, ':c4', None, ':g4', None],
            # [None, None, ':c2', ':e2', None, None, ':g2', ':c2', None, [':e2', ':e4'], None, None, 'chord(:E3, :minor)', None, ':g2', None]
        ]
    },
    {
        'type': 'sample',
        'name': 'drum_cymbal_closed',
        'fxs': [],
        'opts': {
            'release': 1,
            'amp': 5,
            'attack': 1,
            'res': 0.9
        },
        'patterns': [
            [
                1, None, 1, None, 
                1, None, 1, None, 
                1, None, 1, None, 
                1, None, 1, None
            ],
            [
                1, None, 1, None, 
                1, None, 1, None, 
                1, None, 1, None, 
                1, None, 1, None
            ]
        ]
    },
]
instrus2 = [
    {
        'type': 'synth',
        'name': 'fm',
        'fxs': [
            # {
            #     'name': 'reverb',
            #     'opts' : {
            #         'mix': 1,
            #         'room': 1
            #     }
            # },
            # {
            #     'name': 'slicer',
            #     'opts': {
            #         'wave': 0,
            #         'phase': 0.25
            #     }
            # }
        ],
        'opts': {
            # 'release': 0.01,
            # 'amp': 0.75,
            # 'attack': 0.1,
            # 'res': 0
        },
        'patterns': [
            [None, None, ':c4', ':e4', None, None, ':g4', ':c4', None, ':e4', None, None, ':c4', None, ':g4', None],
            # [None, None, ':c2', ':e2', None, None, ':g2', ':c2', None, [':e2', ':e4'], None, None, 'chord(:E3, :minor)', None, ':g2', None]
        ]
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
        'patterns': [
            [
                1, None, 1, None, 
                1, None, 1, None, 
                1, None, 1, None, 
                1, None, 1, None
            ],
            [
                1, None, 1, None, 
                1, None, 1, None, 
                1, None, 1, None, 
                1, None, 1, None
            ]
        ]
    },
]

while True :
    print('ONE')
    sender.send_message('/json/channel', [0, json.dumps(instrus[0])])
    time.sleep(0.5)
    sender.send_message('/json/channel', [1, json.dumps(instrus2[1])])
    time.sleep(10)
    print('TOW')
    sender.send_message('/json/channel', [0, json.dumps(instrus2[0])])
    time.sleep(0.5)
    sender.send_message('/json/channel', [1, json.dumps(instrus[1])])
    time.sleep(10)


exit()

for k in range(len(instrus)) :
    print([instrus[k]['type'], instrus[k]['name']])
    print(instrus[k])
    # if k == 0 :
    sender.send_message('/instru/add/complete', [json.dumps(instrus[k])])
    time.sleep(0.25)
    #     continue
    # sender.send_message('/instru/add', [instrus[k]['type'], instrus[k]['name']])
    # time.sleep(0.25)
    # # exit()

    # for kk in range(len(instrus[k]['patterns'])):
    #     for kkk in range(len(instrus[k]['patterns'][kk])):
    #         if instrus[k]['patterns'][kk][kkk] is not None :
    #             print([k, kk, kkk, instrus[k]['patterns'][kk][kkk]])
    #             sender.send_message('/instru/step/add', [k, kk, kkk, instrus[k]['patterns'][kk][kkk]])
    #             time.sleep(0.2)

time.sleep(10)
print('REMOVE fxs')
sender.send_message('/instru/fx/remove/all', [0])
time.sleep(5)
print('ADD step')
sender.send_message('/instru/step/add', [0, 0, 2, ':g1'])

exit()
# time.sleep(5)

for k in range(len(instrus)) :
    opts = [k]
    for kk, v in instrus[k]['opts'].items() :
        opts.append(kk)
        opts.append(v)
    print(opts)
    sender.send_message('/instru/options/change', opts)
    time.sleep(0.25)

# time.sleep(5)

for k in range(len(instrus)) :
    fxs = [k]
    for kk in range(len(instrus[k]['fxs'])) :
        fxs.append(instrus[k]['fxs'][kk]['name'])
        for kkk, vv  in instrus[k]['fxs'][kk]['opts'].items() :
            if kkk == 'name' :
                continue
            fxs.append(kkk)
            fxs.append(vv)
        print(fxs)
        sender.send_message('/instru/fx/add', fxs)
        time.sleep(0.25)

time.sleep(5)
# sender.send_message('/instru/fx/change', [0, 0, 'room', 0.5])
time.sleep(5)

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
