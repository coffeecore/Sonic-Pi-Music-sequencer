from pythonosc import osc_message_builder
from pythonosc import udp_client
import time
import json
import sys

sender = udp_client.SimpleUDPClient('127.0.0.1', 4560)

# sender.send_message('/measure', ['bar', 4])
# time.sleep(0.2)
sender.send_message('/state', ['play'])
time.sleep(0.2)

# for i in range(0, 50):
i = [
  {
    "type": "synth",
    "synth": "tb303",
    "opts": {
      "release": 0.125,
      "cutoff": 120,
      "res": 0.5,
      # "slide": 0.25
      # "amp": 0.5
    },
    "fxs": {
      "reverb": {
        "room": 0.9,
        "mix": 1
      }
    },
    "patterns": [
          [":a3", ":b3", ":c3"],
          [":a4", ":b4", ":c4", ":d4"],
          [":a5", ":b5", ":c5", ":d5"],
          [":a6", ":b6", ":c6", ":d6"],
        # "50", "51", "52",
        # ["53", "54", "55"],
    ]
  },
  {
    "type": "synth",
    "synth": "zawa",
    "opts": {
      "release": 0.5,
      "cutoff": 100,
      "res": 0.5,
      # "slide": 0.25
      # "amp": 0.5
    },
    "fxs": {
      # "reverb": {
      #   "room": 0.9,
      #   "mix": 1
      # }
    },
    "patterns": [
        # "60", "61", "62",
        # ["63", "64", "65"]
          [":e5", ":c5", ":c5", ":d5"],
          [":e5", ":c5", ":c5", ":d5"],
          [":f4", ":f5", None, ":d5"],
          [":d5", ":d5", None, ":f5"]
    ]
  },
  {
    # "type": "external_sample",
    # "sample": "/Users/antoine/Music/Sonic Pi/samples/Roland TR-909/BT/BT0A0A7.WAV",
    "type": "sample",
    "sample": "bd_tek",
    "opts": {
      ##| "release": 0.125,
      ##| "cutoff": 120,
        # "res": 0.5,
    },
    "fxs": {
      "distortion": {
        "distort": 0.99
      },
      # "reverb": {
      #   "room": 0.9,
      #   "mix": 1
      # }
    },
    "patterns": [
          [True, None, None, None],
          [True, None, None, True],
          [True, None, None, None],
          [True, None, None, True],
    ]
  },
  {
    # "type": "external_sample",
    # "sample": "/Users/antoine/Music/Sonic Pi/samples/Roland TR-909/HHCD/HHCD6.WAV",
    "type": "sample",
    "sample": "drum_cymbal_closed",
    "opts": {
      ##| "release": 0.125,
      ##| "cutoff": 120,
        # "res": 0.5,
        "amp": 0.3
    },
    "fxs": {
      # "distortion": {
      #   "distort": 0.99
      # },
      # "reverb": {
      #   "room": 0.9,
      #   "mix": 1
      # }
    },
    "patterns": [
          [True, True, True, True],
          [True, True, True, True],
          [True, True, True, True],
          [True, True, True, True],
    ]
  },
  {
    # "type": "external_sample",
    # "sample": "/Users/antoine/Music/Sonic Pi/samples/Roland TR-909/ST/ST0T0SA.WAV",
    "type": "sample",
    "sample": "sn_dub",
    "opts": {
      ##| "release": 0.125,
      ##| "cutoff": 120,
        # "res": 0.5,
    },
    "fxs": {
      # "distortion": {
      #   "distort": 0.99
      # },
      # "reverb": {
      #   "room": 0.9,
      #   "mix": 1
      # }
    },
    "patterns": [
        [
          None, None, True, None],
          [None, None, True, None
        ],
        [
          None, None, True, None],
          [None, None, True, None
        ],
    ]
  }
]
print(json.dumps(i))
sender.send_message('/settings', ['bpm', 100])
# time.sleep(0.25)
# sender.send_message('/bpm', [110])
# time.sleep(0.25)
# sender.send_message('/bpm', [120])
# time.sleep(0.25)

sender.send_message('/channels', [json.dumps(i)])
time.sleep(1)
# print("PLAY")
# sender.send_message('/state', ['play'])
time.sleep(2)
# sender.send_message('/record/start', [1])
# # sender.send_message('/volume', [0])
# # sender.send_message('/state', ['synthfm0_state', 'pause'])
# time.sleep(8)
# sender.send_message('/record/stop', [1])
# time.sleep(0.2)
# sender.send_message('/record/save', [1])

# sender.send_message('/volume', [3])
# sender.send_message('/state', ['stop'])
# time.sleep(3)
# time.sleep(4)
# sender.send_message('/kill', ['synth_1'])
# sender.send_message('/kill', ['synth_0'])
# sender.send_message('/kill', ['ext_sample_1'])
# sender.send_message('/kill', ['synth_0'])

# sender.send_message('/measure', ['bar', 2])

# sender.send_message('/state', ['play'])


exit();
sender.send_message('/set', ['metronome_state', 0])
time.sleep(0.2)

sender.send_message('/set', ['bpm', 150])
time.sleep(0.2)

sender.send_message('/start', [1])
time.sleep(0.2)

sender.send_message('/set', ['pattern_max', 4])
time.sleep(0.2)

instrus = [
    {
        'type': 'synth',
        'name': ':tb303',
        'opts': {
            # 'cutoff': 70,
            # 'res': 0.999,
            # 'attack': 2,
            # 'release': 1
            'release': 0.125,
            'cutoff': 100,
            'res': 0.7,
            # 'wave': 2,
            # 'slide': 2
        },
        'fxs': {
        },
        'patterns': [
            # [':e1', None, ':g3', None, ':g4', ':f4', ':g3', None, ':e1', None, ':e3', ':g4', ':e1', None, ':e3', None],
            # ['[:f2, :f4]', None, 'chord(:e, :major)', None]
            # [[':f2', ':f4'], None, 'chord(:E3, :major)', None, [':f2', ':f4'], None, 'chord(:E3, :major)', None, [':f2', ':f4'], None, 'chord(:E3, :major)', None, [':f2', ':f4'], None, 'chord(:E3, :major)', None]
            [':f3', ':e3', ':c3', ':cs3'],
            [':f3', ':e3', ':c3', ':cs3'],
            [':f3', ':e3', ':c3', ':cs3'],
            [':f3', ':e3', ':c3', ':cs3']
        ]
    },
    {
        'type': 'external_sample',
        'name': '/Users/antoine/Music/Sonic Pi/samples/Roland TR-909/BT/BT0A0A7.WAV',
        'opts': {
            'release': 2,
            # 'cutoff': 100
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
            # [1, None, 1, None, 1, None, 1, None, 1, None, 1, None, 1, None, 1, None],
            # ['[:f2, :f4]', None, 'chord(:e, :major)', None]
            [1, 1, None, 1],
            [1, 1, None, 1],
            [1, 1, 1, 1],
            [1, 1, 1, 1],
        ]
    },
    {
        'type': 'external_sample',
        'name': '/Users/antoine/Music/Sonic Pi/samples/Roland TR-909/HHCD/HHCD0.WAV',
        'opts': {
            # 'release': 2,
            # 'cutoff': 100
        },
        'fxs': {
            # ':reverb': {
            #     'mix': 0.5,
            #     'room': 1
            # },
            # ':distortion': {
            #     'distort': 0.999
            # }
        },
        'patterns': [
            # [1, None, 1, None, 1, None, 1, None, 1, None, 1, None, 1, None, 1, None],
            # ['[:f2, :f4]', None, 'chord(:e, :major)', None]
            [1, 1, 1, 1],
            [1, 1, 1, 1],
            [1, 1, 1, 1],
            [1, 1, 1, 1],
        ]
    }
]

sender.send_message('/json', [json.dumps(instrus)])

