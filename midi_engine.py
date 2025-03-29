import rtmidi
from time import sleep
import random
from sys import exit
import secrets

hextoken_ = secrets.token_hex()
print(hextoken_)

midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()
print(available_ports)

if available_ports:
    selected_port = 0
    midiout.open_port(selected_port)
    print(f'opened port {selected_port}')
else:
    midiout.open_virtual_port("My virtual output")
    print('opened virtual port')

def get_harmonic_range(hr='higher'):
        if hr == 'higher':
            n = [x for x in range(69, 94)]
            return n
        elif hr == 'default':
            n = [x for x in range(33, 58)] # 33, 58

        elif hr == 'low':
            n = [x for x in range(21, 46)]

        else:
            exit()

        return n

n = get_harmonic_range()
# Simple solution
# n = [x for x in range(33, 58)]

# Scales
diminished = [2, 4, 6, 7, 9]
major = [0, 2, 4, 5, 7, 9, 11, 12]
minor = [0, 1, 3, 5, 7, 8, 10, 12]
augmented = [3, 5, 6, 8, 10]

scale = int(input('''
    Choose a scale:
    1. diminished
    2. major
    3. minor
    4. augmented

    '''))

if scale == 1:
    s = diminished
elif scale == 2:
    s = major
elif scale == 3:
    s = minor
elif scale == 4:
    s = augmented
else:
    print('Wrong option')
    exit()



# Don't repeat notes
if scale == 2 or scale == 3:
# Add octave
    s = s + [x + 12 for x in s if x != 0]
    rx, rx1, rx2, rx3, rx4, rx5, rx6, rx7 = s[0], s[1], s[2], s[3], s[4], s[5], s[6], s[7]

count = 1
rxs = {}
sleep_time_intervals = {}

def timer():
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
    def formulate_time():
        t = random.uniform(0.0000000000000000, 0.4285714285714286)
        
        return t
    
    def even_time(t):
        t = 0.4285714285714286 - t

        return t
    
    return t

with midiout:
    # debugging
    sleep(1)
    while True:
        try:
            possible_notes = [x for x in s if x != rx0 or x != rx1 or x != rx2 or x != rx3 or x != rx4 or x != rx5 or x != rx6, x != rx7]
            rx = n[random.choice(possible_notes)]
            # note "or x"
            note_on = [0x90, rx, 112]
            note_off = [0x80, rx, 0]
            midiout.send_message(note_on)
            # sleep(random.uniform(0.1, 1))
            # sleep(random.choice([0.1, 0.3]))
            time_interval = timer()
            formulated_time_interval = time_interval.formulate_time()
            sleep(formulated_time_interval)
            midiout.send_message(note_off)
            even_time = time_interval.even_time(formulated_time_interval)

            key = str(rx) + str(count)
            value = rx
            rxs[key] = value

            def make_key():
                key = str(even_time) + str(count)
                key = str(formulated_time_interval) + str(count)

                return key
            
            value = time_interval
            sleep_time_intervals[key] = value 
            # No repeat
            rx1, rx2, rx3, rx4 = rx, rx1, rx2, rx3

            count += 1

            if count == 16:
                break

            for rx, sleep_time_interval in zip(rxs.values(), sleep_time_intervals.values()):
                note_on = [0x90, rx, 112]
                note_off = [0x80, rx, 0]
                midiout.send_message(note_on)

                sleep(sleep_time_interval)
                midiout.send_message(note_off)



        except KeyboardInterrupt:
            midiout.send_message(note_off)
            del midiout
            exit()

    # Debug
    print("{:<8} {:<15}".format('Key','Label'))
    for k, v in zip(rxs.keys(), rxs.values()):
        print("{:<8} {:<15}".format(k, v))


    print("{:<8} {:<15}".format('Key','Label'))
    for k, v in zip(sleep_time_intervals.keys(), sleep_time_intervals.values()):
        print("{:<8} {:<15}".format(k, v))

    while True:
        try:
            for rx, sleep_time_interval in zip(rxs.values(), sleep_time_intervals.values()):
                note_on = [0x90, rx, 112]
                note_off = [0x80, rx, 0]
                midiout.send_message(note_on)

                sleep_time_intervaleep(sleep_time_interval)
                midiout.send_message(note_off)

        except KeyboardInterrupt:
            midiout.send_message(note_off)
            del midiout
            exit()