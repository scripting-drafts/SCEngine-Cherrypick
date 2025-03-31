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
    # def __init__(self):
    #     ftime_uniform = range(0.0000000000000000, 0.4285714285714286)

    #     self.ftime_uniform = ftime_uniform

    def formulate_time(self, remainder=None):
        t = random.uniform(0.0000000000000000, 0.4285714285714286)
        if remainder is not None:
            t = t + remainder
        
        return t
    
    def even_time(self, t):
        even= 0.4285714285714286 - t
        if t != 0:
            summary = even + t
            remainder = 0.4285714285714286 - summary

        if remainder == 0:
            remainder = None

        return even, remainder