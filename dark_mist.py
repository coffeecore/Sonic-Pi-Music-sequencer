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
    "name": "prophet",
    "fxs": {
      "slicer": {
        "probability": 0.7,
        "prob_pos": 1
      }
    },
    "patterns": [
        [{"note": ":e1", "release": 1, "cutoff": 70}, None, None, None],
        [None, None, None, None],
    ],
    "sleeps": [
        [1, 1, 1, 1],
        [1, 1, 1, 1]
    ]
  },
  {
    "type": "sample",
    "name": "guit_em9",
    "fxs": {
      "slicer": {
        "phase": 0.125,
      }
    },
    "patterns": [
        [{"rate": 0.5}, None, None, None],
        [{"rate": 0.5}, None, None, None],
    ],
    "sleeps": [
        [1, 1, 1, 1],
        [1, 1, 1, 1]
    ]
  },
]

# i = [{'type': 'synth', 'name': 'tb303', 'fxs': {}, 'patterns': [[{'note': 60}, None, {'note': 61, 'release': 0.5}, {'note': 60}], [{'note': 62, 'release': 0.5}, None, {'note': 63, 'release': 0.5}]], 'sleeps': [[1.5, 1.5, 0.25, 0.25], [1.5, 0.25, 0.25]]}, {'type': 'sample', 'name': 'sn_dub', 'fxs': {}, 'patterns': [[None, {}, None, {}], [{}]], 'sleeps': [[0.25, 0.25, 0.25, 0.25], [0.25]]}]



sender.send_message('/settings', ['eighth', 4])
time.sleep(0.2)
sender.send_message('/settings', ['bar', 4])
time.sleep(0.2)
sender.send_message('/settings', ['pmax', 2])
time.sleep(0.2)
for ic, c in enumerate(i):
  print(c['type'], c['name'])
  # sender.send_message('/channel/add', [ic, c['type'], c['name'], json.dumps(c['fxs'])])
  sender.send_message('/add', ['channel', ic, c['type'], c['name'], json.dumps(c['fxs'])])
  # time.sleep(0.2)
  for ip, p in enumerate(c['patterns']):
    # sender.send_message('/channel/pattern/add', [ic, ip])
    sender.send_message('/add', ['pattern', ic, ip])
    # time.sleep(0.2)
    for i_s, s in enumerate(p):
      print([ic, ip, i_s, c['sleeps'][ip][i_s], json.dumps(s)])
      # sender.send_message('/channel/pattern/step/add', [ic, ip, i_s, c['sleeps'][ip][i_s], json.dumps(s)])
      sender.send_message('/add', ['step', ic, ip, i_s, c['sleeps'][ip][i_s], json.dumps(s)])
      # time.sleep(0.2)
# sender.send_message('/channels', [json.dumps(i)])
sender.send_message('/settings', ['state', 'play'])
# exit()

time.sleep(8)
while True:
    for i in [100, 130, 70]:
      print("CHANGE")
      p = random.choice([0.125, 0.25])
      sender.send_message('/channel/options', ["synth_0", json.dumps({"cutoff": i, "note": ":e1", "release": 8, "cutoff": 70})])
      sender.send_message('/channel/fxs', ["sample_1", "slicer", json.dumps({"phase": p})])

      sender.send_message('/channel', [0, json.dumps({
        "type": "synth",
        "name": "prophet",
        "fxs": {
          "slicer": {
            "probability": 0.7,
            "prob_pos": 1
          }
        },
        "patterns": [
            [{"note": ":e1", "release": 8, "cutoff": i}, None, None, None],
        ],
        "sleeps": [
          [1, 1, 1, 1]
        ]
      })])
      sender.send_message('/channel', [1, json.dumps({
        "type": "sample",
        "name": "guit_em9",
        "fxs": {
          "slicer": {
            "phase": p,
          }
        },
        "patterns": [
            [{"rate": 0.5}, None, None, None],
        ],
        "sleeps": [
          [1, 1, 1, 1]
        ]
      })])


      time.sleep(8)


