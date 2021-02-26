class PianoHat:
    LAYOUT_CHANNEL = 0
    LAYOUT_PATTERN = 1
    LAYOUT_STEP    = 2
    LAYOUT_NOTE    = 3

    MOD_KEY        = 0
    MOD_LIVE       = 1

    BLACK_KEYS = [1, 3, 6, 8, 10]
    WHITE_KEYS = [0, 2, 4, 5, 7, 9, 11, 12]

    def __init__(self):
        self.octave       = 0
        self.channel      = 0
        self.pattern      = [0, 0]
        self.step         = 0
        self.layout       = self.LAYOUT_CHANNEL
        self.mod          = self.MOD_KEY
        self.notes        = []
        self.totalChannel = 0

    def get_pattern(self):
        return (self.pattern[0])*7+(self.pattern[1])

    def midi_note(self, key: int):
        return (self.octave)*12+key

    # def on_instru_listener(self, channel: int, event: bool):
    #     # CHANNEL
    #     if self.layout == self.LAYOUT_CHANNEL:
    #         if event:
    #             self.layout = self.LAYOUT_STEP
    #             # On LED Octave Up
    #         return

    # def on_octave_up_listener(self, channel:int, event: bool):
    #     # CHANNEL
    #     if self.layout == self.LAYOUT_CHANNEL:
    #         if event:
    #             if self.totalChannel > 0 and self.channel < self.totalChannel-1:
    #                 self.channel += 1
    #             else :
    #                 self.channel = 0
    #         return

    # def on_octave_down_listener(self, channel:int, event: bool):
    #     # CHANNEL
    #     if self.layout == self.LAYOUT_CHANNEL:
    #         if event:
    #             if self.channel > 0:
    #                 self.channel -= 1
    #                 return
    #             if self.totalChannel > 0:
    #                 self.channel = self.totalChannel-1
    #         return

    # def on_note_listener(self, key:int, event: bool):
    #     # CHANNEL
    #     if self.layout == self.LAYOUT_CHANNEL:
    #         if event:
    #             if self.BLACK_KEYS.count(key) != 0:
    #                 self.pattern[0] = self.BLACK_KEYS.index(key)
    #             if self.WHITE_KEYS.count(key) != 0:
    #                 self.pattern[1] = self.WHITE_KEYS.index(key)
    #         return
