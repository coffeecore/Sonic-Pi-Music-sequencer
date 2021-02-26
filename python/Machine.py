import json

class Machine:
    def __init__(self):
        self.bpm      = 60
        self.bar      = 4
        self.pmax     = 1
        self.state    = 'stop'
        self.channels = []

    def add_channel(self, channel, position = None):
        if position == None:
            self.channels.append(channel)
            return;
        self.channels.remove(position)
        self.channels.insert(position, channel)

    def del_channel(self, position = None):
        if position == None:
            if len(self.channels) > 0:
                self.channels.pop()
            return
        if len(self.channels) > position:
            self.channels.pop(position)

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
        s = s + "\n"
        return s

    def display_channels(self):
        s = ''
        for i, channel in enumerate(self.channels):
            s = s + self.display_channel(channel, i)
        return s

    def display_channel(self, channel, i = 0, ):
        s = "["+str(i)+"]["+channel.type+"] "+channel.name[:8]
        if len(channel.name) < 8:
             s = s + "\t"
        else:
            s = s + "... "
        s = s + channel.display(i, self.pmax)
        s = s + " "+channel.name+"\n\n"
        return s

    def channels_to_list(self):
        result = []
        for channel in self.channels:
            result.append(channel.__dict__)

        return result

    def json(self):
        return json.dumps(self.channels_to_list())
