import json

class Machine:
    SAMPLES_FOLDER = "/Users/antoine/Music/Sonic Pi/samples"
    CHANNELS_PATH  = "/Users/antoine/Music/Sonic Pi/.data"

    def __init__(self):
        self.bpm      = 60
        self.bar      = 4
        self.pmax     = 1
        self.state    = 'stop'
        self.channels = []
        self.eighth   = 0.125

    def add_channel(self, channel, position = None):
        if position == None:
            self.channels.append(channel)
            return;
        self.channels.insert(position, channel)

    def del_channel(self, position = None):
        if position == None:
            position = len(self.channels)-1
        if len(self.channels) > position:
            self.channels.pop(position)
