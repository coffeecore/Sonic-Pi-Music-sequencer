from pythonosc import osc_message_builder
from pythonosc import udp_client
import time
import json
import random

sender = udp_client.SimpleUDPClient('127.0.0.1', 4560)

# sender.send_message('/record/start', [1])
# time.sleep(12)
# sender.send_message('/record/stop', [1])
# time.sleep(0.2)
# sender.send_message('/record/save', [1])
# time.sleep(0.2)
# sender.send_message('/reset', [1])
# # time.sleep(0.2)
# exit()

# sender.send_message('/debug', [0])
# time.sleep(0.2)

# sender.send_message('/metronome', [1])
# time.sleep(0.2)

sender.send_message('/bpm', [60])
time.sleep(0.2)

sender.send_message('/pattern/max', [8])
time.sleep(0.2)

"""
live_loop :dark_mist do
  print "DARK"
  co = (line 70, 130, steps: 2).tick
  print co
  with_fx :slicer, probability: 0.7, prob_pos: 1 do
    synth :prophet, note: :e1, release: 8, cutoff: co
  end

  with_fx :slicer, phase: [0.125, 0.25].choose do
    sample :guit_em9, rate: 0.5
  end
  sleep 8
end

live_loop :crashing_waves do
  print "CRASH"
  with_fx :slicer, wave: 0, phase: 0.25 do
    sample :loop_mika, rate: 1
  end
  sleep 16
end
"""
instrus = [
    {
        'type': 'synth',
        'name': 'prophet',
        'fxs': [
            {
                'name': 'slicer',
                'opts': {
                    'probability': 0.7,
                    'prob_pos': 1
                }
            }
        ],
        'opts': {
            'release': 8
        },
        'patterns': [
            [':e1', None, None, None, None, None, None, None],
            [':a2', None, None, None, None, None, None, None],
            [':e1', None, None, None, None, None, None, None],
            [':a2', None, None, None, None, None, None, None],
            [':e1', None, None, None, None, None, None, None],
            [':a2', None, None, None, None, None, None, None],
            [':e1', None, None, None, None, None, None, None],
            [':a2', None, None, None, None, None, None, None]
        ]
    },
    {
        'type': 'sample',
        'name': 'guit_em9',
        'fxs': [
            {
                'name': 'slicer',
                'opts': {
                    'phase': 0.125,
                }
            }
        ],
        'opts': {
            'rate': 0.5
        },
        'patterns': [
            [1, None, None, None, None, None, None, None],
            [1, None, None, None, None, None, None, None],
            [1, None, None, None, None, None, None, None],
            [1, None, None, None, None, None, None, None],
            [1, None, None, None, None, None, None, None],
            [1, None, None, None, None, None, None, None],
            [1, None, None, None, None, None, None, None],
            [1, None, None, None, None, None, None, None]
        ]
    },
    {
        'type': 'sample',
        'name': 'loop_mika',
        'fxs': [
            {
                'name': 'slicer',
                'opts': {
                    'wave': 0,
                    'phase': 0.25
                }
            }
        ],
        'opts': {
            'rate': 0.5
        },
        'patterns': [
            [1,    None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [1,    None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [1,    None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [1,    None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None]
        ]
    }
]

for k in range(len(instrus)) :
    sender.send_message('/instru/add/complete', [json.dumps(instrus[k])])
    time.sleep(0.2)
# time.sleep(1)
sender.send_message('/start', [1])
time.sleep(0.2)
# print("PATTERN")
# sender.send_message('/instru/pattern/add', [0])
# time.sleep(0.2)
# sender.send_message('/instru/pattern/add', [0])

# time.sleep(2)

# print("REMOEdsdsd")
# sender.send_message('/instru/pattern/remove', [0, 1])

# sender.send_message('/instru/step/add', [0, 0, 1, ':g1'])
# time.sleep(10)


# print("ENDPATTERN")


# for k in range(len(instrus)) :
# for i in range(8) :
    # print(i)
while True:
    for kk in range(8) :
        # print(kk)
        # instruOne = instrus[0];
        # instruOne['opts']['cutoff'] = 70+((130-70)/8)*kk
        # instruTwo = instrus[1]
        # instruTwo['fxs'][0]['opts']['phase'] = random.choice([0.125, 0.25])
        print(kk)
        opts = [0]
        opts.append('cutoff')
        opts.append(70+((130-70)/8)*kk)
        sender.send_message('/instru/options/change', opts)
        opts = [1]
        opts.append('phase')
        opts.append(random.choice([0.125, 0.25]))
        sender.send_message('/instru/fxs/change', opts)
        time.sleep(2)
        # sender.send_message('/instru/change/complete', [json.dumps(instruOne)])
        # sender.send_message('/instru/change/complete', [json.dumps(instruTwo)])
        # time.sleep(2)

# print("METRONOME")
# sender.send_message('/metronome', [0])
# time.sleep(0.2)
# print("PAUSE")
# sender.send_message('/pause', [1])
# time.sleep(0.2)
# sender.send_message('/start', [1])
# time.sleep(0.2)
# for kk in range(8) :
#     print(kk)
#     opts = [0]
#     opts.append('cutoff')
#     opts.append(70+((130-70)/8)*kk)
#     sender.send_message('/instru/options/change', opts)
#     opts = [1]
#     opts.append('phase')
#     opts.append(random.choice([0.125, 0.25]))
#     sender.send_message('/instru/fxs/change', opts)
#     time.sleep(2)
# time.sleep(8)
# sender.send_message('/pause', [1])
