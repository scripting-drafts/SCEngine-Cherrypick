import random
import numpy as np
import sys

class SamplesLibGenerate:
    def __init__(self, seed=50):
        # self.logger = Logger().logging()

        diminished = [2, 4, 6, 7, 9]
        major = [0, 2, 4, 5, 7, 9, 11, 12]
        minor = [0, 1, 3, 5, 7, 8, 10, 12]
        augmented = [3, 5, 6, 8, 10]

        # NAME s THE SCALE OF CHOICE
        s = diminished

        s = [x - 12 for x in s if x != 0] + s + [x + 12 for x in s if x != 0]
        self.scale = s

        # random.seed(seed)
    
    def get_harmonic_range(self, hr='higher'):
        if hr == 'higher':
            n = [x for x in range(69, 94)]
            return n
        elif hr == 'default':
            n = [x for x in range(33, 58)] # 33, 58

        elif hr == 'low':
            n = [x for x in range(21, 46)]

        else:
            # self.logger.debug('No harmonic range given: %s' % hr)
            sys.exit()

        return n

    def determine_notes_presence(self, chosen_notes):
        notes_presence = []
        for x in chosen_notes:
            # if x == chosen_notes[0]:
            #     notes_presence.append(x)
            # else:
            notes_presence.append(np.random.choice([x, 9999], p=[0.9, 0.1]))

        notes_presence = [x if x != 9999 else None for x in notes_presence]

        return notes_presence
    
    def get_notes(self, kind = 'bass'):
        kinds = {
            'piano': 64,
            'bass': 24
        }
        
        n = self.get_harmonic_range()
        notes_amount = random.randint(0, kinds[kind])
        # midi_notes = [n[np.random.choice(self.scale, p=[.5 for x in self.scale if x != self.scale[0]].insert(0, .6))]
        #                 for _ in range((notes_amount))]
        midi_notes = [n[x] for x in random.sample(self.scale, notes_amount, counts=[6 for _ in self.scale])]
        midi_notes = self.determine_notes_presence(midi_notes)

        return midi_notes