from pythonosc import osc_message_builder
from pythonosc import udp_client
import time
import json
import sys
import random

sender = udp_client.SimpleUDPClient('127.0.0.1', 4560)


i = [
  {
    "type": "synth",
    "synth": "prophet",
    "opts": {
      "release": 8,
      "cutoff": 70
    },
    "fxs": {
      "slicer": {
        "probability": 0.7,
        "prob_pos": 1
      }
    },
    "patterns": [
        [":e1", None, None, None],
    ]
  },
  {
    "type": "sample",
    "sample": "guit_em9",
    "opts": {
      "rate": 0.5,
    },
    "fxs": {
      "slicer": {
        "phase": 0.125,
      }
    },
    "patterns": [
        [True, None, None, None],
    ]
  },
  {
    "type": "sample",
    "sample": "loop_mika",
    "opts": {
        "rate": 0.5
    },
    "fxs": {
        "slicer": {
            "wave": 0,
            "phase": 0.25
        },
    },
    "patterns": [
        [True, None, None, None],
    ]
  }
]

sender.send_message('/settings', ['eighth', 1])
time.sleep(0.2)
sender.send_message('/settings', ['bar', 8])
time.sleep(0.2)
sender.send_message('/settings', ['pmax', 1])
time.sleep(0.2)



sender.send_message('/channels', [json.dumps(i)])
sender.send_message('/state', ['play'])
time.sleep(8)
while True:
    for i in [100, 130, 70]:
      print("CHANGE")
      p = random.choice([0.125, 0.25])
      sender.send_message('/channel/options', ["synth_0", json.dumps({"cutoff": i})])
      sender.send_message('/channel/fxs', ["sample_1", "slicer", json.dumps({"phase": p})])

      sender.send_message('/channel', [0, json.dumps({
        "type": "synth",
        "synth": "prophet",
        "opts": {
          "release": 8,
          "cutoff": i
        },
        "fxs": {
          "slicer": {
            "probability": 0.7,
            "prob_pos": 1
          }
        },
        "patterns": [
            [":e1", None, None, None],
        ]
      })])
      sender.send_message('/channel', [1, json.dumps({
        "type": "sample",
        "sample": "guit_em9",
        "opts": {
          "rate": 0.5,
        },
        "fxs": {
          "slicer": {
            "phase": p,
          }
        },
        "patterns": [
            [True, None, None, None],
        ]
      },)])


      time.sleep(8)


