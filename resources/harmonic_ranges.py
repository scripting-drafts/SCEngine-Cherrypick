def get_harmonic_range(hr='medium'):
        '''
        SUB
        9 - A - 13.57hz
        33- A1- 55

        BASS
        33- A1- 55
        45- A2- 110hz


        93- A6- 1760
        '''
        if hr == 'higher':
            n = [x for x in range(69, 94)]
            return n
        elif hr == 'default':
            n = [x for x in range(33, 58)] # 33, 58

        elif hr == 'low':
            n = [x for x in range(21, 46)]

        elif hr == 'total':
            n = [x for x in range(21, 94)]

        elif hr == 'medium':
            n = [x for x in range(33, 94)]

        elif hr == 'bass':  # 16 -> E 20.60hz
            n = [x for x in range(33, 46)]

        elif hr == 'sub':  # 16 -> E 20.60hz
            n = [x for x in range(9, 34)]

        else:
            exit()

        return n