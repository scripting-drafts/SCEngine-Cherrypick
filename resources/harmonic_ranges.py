from sys import exit

def get_harmonic_range(intervals='bass', note='A'):
        
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

        notes = ['a', 1, 'b', 0.5, 'c', 1, 'd', 1, 'e', 0.5, 'f']
        note = note.lower()
        deviation = 0

        n = [n for n in notes if note == n]
        if n != 'a':
            i = 0
            distance = [i + interval for interval in notes[notes.index(note)] if interval is int()]
            i = 0

            hr = hr[intervals]
            hr = [distance + y for y in hr]

            return hr
        
        elif note == 'a':
            hr_a = [x for x in hr_a[intervals]]

            return hr
        
        else:
            AssertionError('We might have computed an unexistant tone')
            exit()