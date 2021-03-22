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
            if len(self.channels) > 0:
                self.channels.pop()
            return
        if len(self.channels) > position:
            self.channels.pop(position)

    def get_channel(self, channel: int):
        if len(self.channels) > channel:
            return self.channels[channel]
        return None

    def display(self):
        s = self.display_settings()
        s = s + self.display_channels()
        return s

    def display_settings(self):
        s = "Settings :\n"
        s = s + "Bpm \t"+str(self.bpm)+"\n"
        s = s + "Bar \t"+str(self.bar)+"\n"
        s = s + "Pmax \t"+str(self.pmax)+"\n"
        s = s + "State \t"+self.state+"\n"
        s = s + "Eighth \t"+str(self.eighth)+"\n"
        s = s + "\n"
        return s

    def display_channels(self):
        s = ''
        for i, channel in enumerate(self.channels):
            s = s + self.display_channel(channel, i)
        return s

    def display_channel(self, channel, i = 0, eighth = 0.25):
        s = "["+str(i)+"]["+channel.type+"] "+channel.name[:8]
        if len(channel.name) < 5:
             s = s + "\t\t"
        elif len(channel.name) < 9:
             s = s + "\t"
        else:
            s = s + "... "
        s = s + channel.display(i, self.eighth, self.pmax)
        s = s + " "+channel.name+"\n\n"
        return s

    def json_channels(self):
        for i, channel in enumerate(self.channels):
            self.json_channel(i)

    def json_channel(self, i, file_prefix = 'channel_'):
        with open(self.CHANNELS_PATH+'/'+file_prefix+str(i)+'.json', 'w') as outfile:
            json.dump(self.channels[i].__dict__, outfile)

