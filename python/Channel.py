class Channel:
    def __init__(self, type = '', name = '', bar = 1):
        self.type                 = type
        self.name                 = name
        self.fxs                  = {}
        self.patterns             = []
        self.sleeps               = []
        self.bar                  = bar
        self.options              = {}
