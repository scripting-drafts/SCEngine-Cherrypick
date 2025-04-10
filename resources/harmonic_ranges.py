def get_harmonic_range(hr='_medium_broad'):
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
        if hr == 'sub':  # 16 -> E 20.60hz
            n = [x for x in range(9, 34)]
        
        elif hr == 'bass':  # 16 -> E 20.60hz
            n = [x for x in range(33, 46)]

        elif hr == '_bass_medium_sub':
            n = [x for x in range(21, 46)]

        elif hr == 'medium':
            n = [x for x in range(45, 58)]

        elif hr == '_medium_broad':
            n = [x for x in range(33, 58)]

        elif hr == 'medium_high':
            n = [x for x in range(57, 70)]

        elif hr == 'high':
            n = [x for x in range(69, 82)]

        elif hr == 'higher':
            n = [x for x in range(81, 105)]
            return n
        
        elif hr == 'highest':
            n = [x for x in range(105, 118)]
            return n

        if hr == '_full_spectrum':
            n = [x for x in range(9, 118)]
        
        else:
            exit()

        return n