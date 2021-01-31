from pythonosc import osc_message_builder
from pythonosc import udp_client
import time
import json

sender = udp_client.SimpleUDPClient('127.0.0.1', 4560)

sender.send_message('/debug', [1])
time.sleep(0.2)

sender.send_message('/metronome', [0])
time.sleep(0.2)

sender.send_message('/bpm', [60])
time.sleep(0.2)

sender.send_message('/start', [1])
time.sleep(0.2)

sender.send_message('/pattern/max', [2])
time.sleep(0.2)

instrus = [
    {
        'type': 'synth',
        'name': ':tb303',
        'opts': {
            'cutoff': 75,
            'res': 0.99999999,
            # 'attack': 2,
            # 'release': 1
        },
        'fxs': {
        },
        'patterns': [
            [':e1', None, ':g3', None, ':g4', ':f4', ':g3', None, ':e1', None, ':e3', ':g4', ':e1', None, ':e3', None],
            # ['[:f2, :f4]', None, 'chord(:e, :major)', None]
            [[':f2', ':f4'], None, 'chord(:E3, :major)', None, [':f2', ':f4'], None, 'chord(:E3, :major)', None, [':f2', ':f4'], None, 'chord(:E3, :major)', None, [':f2', ':f4'], None, 'chord(:E3, :major)', None]
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
            [1, None, 1, None, 1, None, 1, None, 1, None, 1, None, 1, None, 1, None],
            # ['[:f2, :f4]', None, 'chord(:e, :major)', None]
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]
    }
]

sender.send_message('/json', [json.dumps(instrus)])

