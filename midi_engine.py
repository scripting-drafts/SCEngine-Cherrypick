import rtmidi
from time import sleep
import random
from sys import exit

midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()
print(available_ports)

if available_ports:
    selected_port = 1
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

# Add octave
s = s + [x + 12 for x in s if x != 0]

# Don't repeat notes
rx, rx1, rx2, rx3, rx4, rx5, rx6 = s[0], s[1], s[2], s[3], s[4], s[5], s[6]

count = 1
rxs = {}
sls = {}

with midiout:
    sleep(1)
    while True:
        try:
            rx = n[random.choice([x for x in s if x != rx or x != rx1 or x != rx2 or x != rx3 or x != rx4 or x != rx5 or x != rx6])]
            note_on = [0x90, rx, 112]
            note_off = [0x80, rx, 0]
            midiout.send_message(note_on)
            # sleep(random.uniform(0.1, 1))
            # sleep(random.choice([0.1, 0.3]))
            sl = 1
            sleep(sl)
            midiout.send_message(note_off)

            key = str(rx) + str(count)
            value = rx
            rxs[key] = value 

            key = str(sl) + str(count)
            value = sl
            sls[key] = value 
            # No repeat
            rx1, rx2, rx3, rx4 = rx, rx1, rx2, rx3

            count += 1

            if count == 16:
                break

        except KeyboardInterrupt:
            midiout.send_message(note_off)
            del midiout
            exit()

    # Debug
    print("{:<8} {:<15}".format('Key','Label'))
    for k, v in zip(rxs.keys(), rxs.values()):
        print("{:<8} {:<15}".format(k, v))


    print("{:<8} {:<15}".format('Key','Label'))
    for k, v in zip(sls.keys(), sls.values()):
        print("{:<8} {:<15}".format(k, v))

    while True:
        try:
            for rx, sl in zip(rxs.values(), sls.values()):
                note_on = [0x90, rx, 112]
                note_off = [0x80, rx, 0]
                midiout.send_message(note_on)

                sleep(sl)
                midiout.send_message(note_off)

        except KeyboardInterrupt:
            midiout.send_message(note_off)
            del midiout
            exit()