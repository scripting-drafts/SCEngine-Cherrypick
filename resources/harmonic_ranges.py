def get_harmonic_range(hr='medium'):
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

        else:
            exit()

        return n