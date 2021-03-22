from pythonosc import osc_message_builder
from pythonosc import udp_client
import time
import json
import sys
import random

sender = udp_client.SimpleUDPClient('127.0.0.1', 4560)

sender.send_message('/settings', ['bar', 1])
time.sleep(0.2)
sender.send_message('/settings', ['pmax', 2])
time.sleep(0.2)

sender.send_message('/settings', ['state', 'play'])
time.sleep(0.2)
instru = {
    "type": "synth",
    "name": "fm",
    "fxs": {
        "distortion": {
            "distort": 0.5
        },
        "reverb": {
            "room": 0.5
        }
    },
    "patterns": [
        [{"note":65}, {"note":65}, {"note":65}, {"note":65}],
        [{"note":64}, {"note":64}, {"note":64}, {"note":64}]
    ],
    "sleeps": [
        [0.25, 0.25, 0.25, 0.25],
        [0.25, 0.25, 0.25, 0.25]
    ],
    "default_step_options": {}
}
sender.send_message('/channel/json', [0, json.dumps(instru)])
