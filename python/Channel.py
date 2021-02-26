class Channel:
    def __init__(self, type = '', name = '', bar = 1):
        self.type     = type
        self.name     = name
        self.fxs      = {}
        self.patterns = []
        self.sleeps = []
        self.bar = bar

    def add_fx(self, fx):
        self.fxs[fx] = {}

    def del_fx(self, fx: str):
        if self.fxs.get(fx) != None:
            del(self.fxs[fx])

    def add_fx_option(self, fx: str, option: str, value):
        self.fxs[fx][option] = value

    def del_fx_option(self, fx: str, option: str):
        if self.fxs.get(fx) != None:
            if self.fxs[fx].get(option) != None:
                del(self.fxs[fx][option])

    def add_step(self, pattern: int, step: int, sleep: float, value = None):
        for i in range(int(pattern)+1):
            if int(i) >= len(self.patterns):
                self.patterns.insert(int(i), [])
        for i in range(int(pattern)+1):
            if int(i) >= len(self.sleeps):
                self.sleeps.insert(int(i), [])
        i = pattern
        total_sleep = 0

        self.patterns[pattern].insert(step, value)
        self.sleeps[pattern].insert(step, sleep)

        while i < len(self.patterns):
            total_sleep = 0
            for i_sl, sl in enumerate(self.sleeps[i]):
                total_sleep = total_sleep + sl
                if total_sleep > self.bar:
                    before = self.patterns[i][:i_sl]
                    after = self.patterns[i][i_sl:]
                    before_sl = self.sleeps[i][:i_sl]
                    after_sl = self.sleeps[i][i_sl:]
                    if len(after) != 0:
                        self.patterns[i] = before
                        self.sleeps[i] = before_sl
                        if len(self.patterns) > i+1:
                            after = after + self.patterns[i+1]
                            self.patterns[i+1] = after
                        else:
                            self.patterns.insert(i+1, after)

                        if len(self.sleeps) > i+1:
                            after_sl = after_sl + self.sleeps[i+1]
                            self.sleeps[i+1] = after_sl
                        else:
                            self.sleeps.insert(i+1, after_sl)
            i += 1

    def del_step(self, pattern: int, step: int):
        print('pat', self.patterns)
        print('sle', self.sleeps)
        del(self.patterns[pattern][step])
        del(self.sleeps[pattern][step])
        print('pat', self.patterns)
        print('sle', self.sleeps)

        i = 0
        i = pattern
        while i < len(self.patterns):
            total_sleep = 0
            for i_sl, sl in enumerate(self.sleeps[i]):
                total_sleep = total_sleep + sl
                print(len(self.sleeps) > (i+1), len(self.sleeps), (i+1))
            if total_sleep < self.bar and len(self.sleeps) > (i+1):
                for i_sl, sl in enumerate(self.sleeps[i+1]):
                    total_sleep = total_sleep + sl
                    if total_sleep < self.bar:
                        patt = self.patterns[i+1].pop(i_sl)
                        self.patterns[i].append(patt)
                        slee = self.sleeps[i+1].pop(i_sl)
                        self.sleeps[i].append(slee)
            i += 1

    def display(self, i):
        s = ''

        if self.type == 'synth':
            for pp in range(4):
                s = s+'| '
                if len(self.patterns) > pp:
                    for iii, ss in enumerate(self.patterns[pp]):
                        if ss == None:
                            s = s+'---- '
                        else:
                            s = s+str(ss['note'])
                            for ii in range(4-len(str(ss['note']))):
                                s = s+'-'
                            s = s + ' '
                        a = int(self.sleeps[pp][iii]/0.25)
                        if a > 1:
                            for iii in range(a-1):
                                s = s+'---- '
            s = s+"\t"+self.type+' : '+self.name

        if self.type == 'sample':
            for pp in range(4):
                s = s+'| '
                if len(self.patterns) > pp:
                    for iii, ss in enumerate(self.patterns[pp]):
                        if ss == None :
                            s = s+'None '
                        else:
                            s = s+'-X-- '
                        a = int(self.sleeps[pp][iii]/0.25)
                        if a > 1:
                            for iii in range(a-1):
                                s = s+'---- '

            s = s+"\t"+self.type+' : '+self.name
        s = s+"\n"
        s = s+"["+str(i)+"] "
        for pp in range(4):
            s = s+'| '
            if len(self.sleeps) > pp:
                for ss in self.sleeps[pp]:
                    if ss == None:
                        s = s+'---- '
                    else:
                        s = s+"{:.2f}".format(ss)+' '
                    a = int(ss/0.25)
                    if a > 1:
                        for ii in range(a-1):
                            s = s+'---- '
        s = s+"\t"+'sleeps '

        return s
