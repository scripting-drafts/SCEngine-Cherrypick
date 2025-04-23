from sys import exit
import random

def get_harmonic_range(texture='bass', note='A'):
        
        '''
        SUB
        9 - A - 13.57hz
        33- A1- 55

        BASS
        33- A1- 55hz
        45- A2- 110hz

        +++ BASS + MEDIUM SUB
        21- A0 - 27.50
        45- A2- 110hz

        MEDIUM
        45- A2- 110hz
        57- A3- 220hz
        
        +++ MEDIUM BROAD (+ SUB?)
        33- A1- 55hz
        57- A3- 220hz

        MEDIUM HIGH - Upper Bass
        57- A3- 220hz
        69- A4- 440hz
        
        HIGH - LEAD
        69- A4- 440hz
        81- A5 - 880hz
        
        HIGHER - LEAD
        81 - A5 - 880hz
        93 - A6 - 1760hz
        105- A7 - 3520hz
        
        HIGHEST - HH
        105 - A7 - 3520hz
        117 - A8 - 7040.00hz 

        +++ FULL SPECTRUM
        9 - A - 13.57hz
        117 - A8 - 7040.00hz 

        
        
        '''
        
        # df = pd.read_excel('scales/Midi_Notes.xlsx', header=0)    
        # len_text = len(hr[texture])
        # min_text = min(hr[texture])

        # for row in df.loc[:, df['Note Names']]:
        #         if row >= min_text:

        hr = {
                  'sub': range(9, 34),
                  'bass': range(33, 46),
                  '_bass_medium_sub': range(21, 46),
                  'medium': range(45, 58),
                  '_medium_broad': range(33, 58),
                  'medium_high': range(57, 70),
                  'high': range(69, 82),
                  'higher': range(81, 105),
                  'highest': range(105, 118)
                  
            }

        notes = {'a': [1, 1],
                 'b': [1, 0],
                 'c': [1, 1],
                 'd': [1, 1],
                 'e': [1, 0],
                 'f': [0, 1],
                 'g': [1, 1],
                 
                 }
        
        note = note.lower()

        below_tones = [x[0] for x in notes.values()]
        above_tones = [x[1] for x in notes.values()]

        rangy = hr[texture]
        note_keys = list(notes.keys())
        note_index = note_keys.index(note)
        resulting_notes = []

        for nut in rangy:
            if note == note_keys[-1]:
                i = 0
                resulting_notes.append(nut + below_tones[:note_index][i])
                i += 1
            if note == note_keys[0]:
                q = 0
                resulting_notes.append(nut + above_tones[note_index:][q])
                q += 1 
            else:
                z = 0
                chosen = random.choice([below_tones[:note_index], above_tones[note_index:]])
                resulting_notes.append(nut + chosen[z])
                z += 1

        return  resulting_notes