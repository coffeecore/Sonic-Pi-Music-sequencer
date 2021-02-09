from pythonosc import osc_message_builder
from pythonosc import udp_client
import time
import json
import sys

sender = udp_client.SimpleUDPClient('127.0.0.1', 4560)

# sender.send_message('/measure', ['bar', 4])
# time.sleep(0.2)
# sender.send_message('/state', ['play'])
# time.sleep(0.2)

# for i in range(0, 50):
i = [
  {
    "type": "synth",
    "synth": "tb303",
    "opts": {
      # "release": 0.125,
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
      # "release": 0.5,
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

# i = [
#   {
#     "type": "synth",
#     "synth": "prophet",
#     "opts": {
#       "release": 8,
#       "cutoff": 70
#     },
#     "fxs": {
#       "slicer": {
#         "probability": 0.7,
#         "prob_pos": 1
#       }
#     },
#     "patterns": [
#         [":e1", None, None, None],
#         [None, None, None, None],
#     ]
#   },
  # {
  #   "type": "sample",
  #   "sample": "guit_em9",
  #   "opts": {
  #     "rate": 0.5,
  #   },
  #   "fxs": {
  #     "slicer": {
  #       "phase": 0.125,
  #     }
  #   },
  #   "patterns": [
  #       [True, None, None, None],
  #       [None, None, None, None],
  #   ]
  # },
  # {
  #   "type": "synth",
  #   "synth": "prophet",
  #   "opts": {
  #     "release": 8,
  #     "cutoff": 100
  #   },
  #   "fxs": {
  #     "slicer": {
  #       "probability": 0.7,
  #       "prob_pos": 1
  #     }
  #   },
  #   "patterns": [
  #       [None, None, None, None],
  #       [":e1", None, None, None],
  #   ]
  # },
  # {
  #   "type": "sample",
  #   "sample": "guit_em9",
  #   "opts": {
  #     "rate": 0.5,
  #   },
  #   "fxs": {
  #     "slicer": {
  #       "phase": 0.25,
  #     }
  #   },
  #   "patterns": [
  #       [None, None, None, None],
  #       [True, None, None, None],
  #   ]
  # },
  # {
  #   "type": "sample",
  #   "sample": "loop_mika",
  #   "opts": {
  #       "rate": 0.5
  #   },
  #   "fxs": {
  #       "slicer": {
  #           "wave": 0,
  #           "phase": 0.25
  #       },
  #   },
  #   "patterns": [
  #       [True, None, None, None],
  #       [None, None, None, None],
  #   ]
  # }
# ]

print(json.dumps(i))
# sender.send_message('/settings', ['pmax', 2])
# sender.send_message('/settings', ['bpm', 1000])
# time.sleep(0.25)
# sender.send_message('/bpm', [110])
# time.sleep(0.25)
# sender.send_message('/bpm', [120])
# time.sleep(0.25)

sender.send_message('/channels', [json.dumps(i)])
sender.send_message('/state', ['play'])
# time.sleep(0.2)
time.sleep(8)
# sender.send_message('/a', ["synth_0", json.dumps({"amp": 0})])
# time.sleep(0.1)
for i in range(99, -1, -10):
  print("opts")
#   print(i)
  sender.send_message('/channel/options', ["synth_0", json.dumps({"amp": (i/100)})])
# sender.send_message('/channel/options', ["synth_0", json.dumps({"amp": 0})])
  sender.send_message('/channel', [0, json.dumps({
      "type": "synth",
      "synth": "tb303",
      "opts": {
        "amp": (i/100),
        # "release": 0.125,
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
    },)])
  sender.send_message('/channel/fxs', ["sample_2", "distortion", json.dumps({"distort": (i/100)})])

  sender.send_message('/channel', [2, json.dumps({
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
        "distort": (i/1000)
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
  })])
  time.sleep(0.25)
time.sleep(4.784365)
for i in range(0, 101, 10):
  print("opts")
#   print(i)
  sender.send_message('/channel/options', ["synth_0", json.dumps({"amp": (i/100)})])
# sender.send_message('/channel/options', ["synth_0", json.dumps({"amp": 0})])
  sender.send_message('/channel', [0, json.dumps({
    "type": "synth",
    "synth": "tb303",
    "opts": {
      "amp": (i/100),
      # "release": 0.125,
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
  },)])

  sender.send_message('/channel/fxs', ["sample_2", "distortion", json.dumps({"distort": (i/1000)})])

  sender.send_message('/channel', [2, json.dumps({
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
        "distort": (i/1000)
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
  })])
  time.sleep(0.25)
sender.send_message('/channel/fxs', ["synth_0", "reverb", json.dumps({"room": 0,"mix": 0})])
time.sleep(2)
sender.send_message('/channel/fxs', ["synth_0", "reverb", json.dumps({"room": 0.5,"mix": 0.5})])
time.sleep(1)
sender.send_message('/channel/fxs', ["synth_0", "reverb", json.dumps({"room": 0.9,"mix": 1})])
time.sleep(1)

  # print("fxs")
  # sender.send_message('/channel/fxs', ["synth_0", "reverb", json.dumps({"room": 0})])
  # time.sleep(0.5)
# i = {
#     "type": "synth",
#     "synth": "tb303",
#     "opts": {
#       "amp": 0
#     },
#     "fxs": {
#     },
#     "patterns": [
#           [":a3", ":b3", ":c3"],
#           [":a4", ":b4", ":c4", ":d4"],
#           [":a5", ":b5", ":c5", ":d5"],
#           [":a6", ":b6", ":c6", ":d6"],
#         # "50", "51", "52",
#         # ["53", "54", "55"],
#     ]
#   }
# sender.send_message('/channel', [0, json.dumps(i)])

exit()
