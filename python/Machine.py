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
        s = ''
        for i, channel in enumerate(self.channels):
            s = s + "["+str(i)+"]["+channel.type+"] "+channel.name[:8]
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
