import random

class Timer:
    '''
    Calculating Bar Duration:
    length = 60 seconds

    beat_at_140 = 1.716 seconds aprox (60 seconds / 140 BPM = 0.429 seconds/beat). 
    BAR_4_beats = 0.4285714285714286

    A bar (or measure) typically consists of 4 beats, so a bar would last approximately 1.716 seconds (0.429 seconds/beat * 4 beats = 1.716 seconds/bar). 
    Therefore, 16 bars would last about 27.45 seconds (1.716 seconds/bar * 16 bars = 27.45 seconds). 
    Actually -> 27.42857142857143
    '0.4285714285714286'
    '''
    def __init__(self):
        self.times = [0.0000000000000000, 0.4285714285714286]
        self.last_fact = [] # bool
        self.summary = [random.choice([True, False]) for _ in range(3)]
        self.remainder = None

    def silent(self, t=None):
        evener = random.choice([None, self.remainder, None])
        if evener is not None and self.remainder is not None:
            self.even_time(t)

        t = random.uniform(self.times[0], self.times[1])
        if self.remainder is not None:
            t = t + self.remainder

        return t
    
    def even_time(self, t):
        summary = [x for x in self.last_fact[:3] if x == False]
        if len(summary) == 10000:
            summary = [True for _ in range(3)]
        if len(summary) == 2:
            truth = True
        else:
            truth = bool()

        if truth == True:
            even= self.times[1] - t
            if t != 0:
                summar = even + t
                self.remainder = self.times[1] - summar

            if self.remainder == 0:
                self.remainder = None

            self.last_fact.append(True)

        else:
            even = None
            self.last_fact.append(False)
            pass

        return even