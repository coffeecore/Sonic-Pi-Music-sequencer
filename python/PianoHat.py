from Machine import Machine
import pianohat

class PianoHat:
    LAYOUT_CHANNEL = 0
    LAYOUT_PATTERN = 1
    LAYOUT_STEP    = 2
    LAYOUT_NOTE    = 3
    LAYOUT_MIDI    = 4

    LAYOUTS = [
        'Channel',
        'Pattern',
        'Step',
        'Note',
        'Midi',
    ]

    MOD_KEY        = 0
    MOD_LIVE       = 1

    MODS = [
        'Key',
        'Live'
    ]

    BLACK_KEYS = [1, 3, 6, 8, 10]
    WHITE_KEYS = [0, 2, 4, 5, 7, 9, 11, 12]

    def __init__(self):
        self.octave       = 5
        self.channel      = -1
        self.pattern      = [0, 0]
        self.step         = 0
        self.layout       = self.LAYOUT_CHANNEL
        self.mod          = self.MOD_KEY
        self.notes        = []

    def get_pattern(self):
        return (self.pattern[0])*7+(self.pattern[1])

    def key_to_midi_note(self, key: int):
        return (self.octave)*12+key

    def midi_note_to_key(self, note: int):
        return (self.octave)*12-note*(-1)

    def get_layout(self):
        return self.LAYOUTS[self.layout]
    def get_mod(self):
        return self.MODS[self.mod]
