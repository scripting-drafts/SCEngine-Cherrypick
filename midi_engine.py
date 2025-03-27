import rtmidi
from time import sleep
import random

midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()
print(available_ports)

if available_ports:
    midiout.open_port(0)
    print('opened port')
else:
    midiout.open_virtual_port("My virtual output")
    print('opened virtual port')

# Midi ranges for A
# 21, 46
# 33, 58

# Midi Range
n = [x for x in range(33, 58)]

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
            sleep(0.3)
            midiout.send_message(note_off)

            rx1, rx2, rx3, rx4 = rx, rx1, rx2, rx3

            count += 1

            if count == 16:
                count = 1

        except KeyboardInterrupt:
            midiout.send_message(note_off)
            del midiout
            exit()