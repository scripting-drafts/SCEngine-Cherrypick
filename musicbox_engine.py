import colorama
import enhancements.mod_initializer as gui_enhancements
import enhancements.turquoise_logger as turquoise_logger
import random
import re
import rtmidi
from sys import exit
from time import sleep
from resources.timer import Timer
from resources.multireplacer import multireplacer_initializer
import pandas as pd

colorama.init()
GREEN = colorama.Fore.GREEN
GRAY = colorama.Fore.LIGHTBLACK_EX
RESET = colorama.Fore.RESET
RED = colorama.Fore.RED

gui_enhancements.run_music_box()

tl_log = turquoise_logger.Logger()
log = tl_log.logging()

replacements = {
    '[': '', ']': '', '\'': '', ', ': '\n'
}

midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()

if available_ports:
    mr = multireplacer_initializer()
    listed_ports = mr.multireplace(re.sub(r'^\s', '', str(available_ports)), replacements) # str([r'{} '.format(x) for x in available_ports]).split('\n')
    log.debug(f'Available Ports: \n\n{listed_ports} \n')
    selected_port = 0
    midiout.open_port(selected_port)
    log.debug(f'Port #{selected_port} Open')
else:
    midiout.open_virtual_port("My virtual output")
    log.debug('W: Opened virtual port')

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

# df = pd.read_excel(f'resources/{scales}.xlsx', sheet_name='Sheet1', header=0)

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

bars_count = 1
rxs = {}
dts = {}
sls = {}
remainder, remainder_use = None, None

times = Timer()

with midiout:
    # debugging
    sleep(1)
    while True:
        try:
            rx = n[random.choice([x for x in s if x != rx or x != rx1 or x != rx2 or x != rx3 or x != rx4 or x != rx5 or x != rx6])]
            note_on = [0x90, rx, 112]
            midiout.send_message(note_on)
            if remainder_use is not None:
                note_length = times.formulate_time(remainder)
            else:
                note_length = times.formulate_time()
            log.debug(f'{rx=}')
            log.debug(f'{note_length=}')
            sleep(note_length)

            note_off = [0x80, rx, 0]
            midiout.send_message(note_off)
            silence_balancer, remainder = times.even_time(note_length)
            log.debug(f'{silence_balancer=}')

            remainder_use = random.choice([remainder, 0.])
            remainder_use = remainder_use if remainder is not None else 0
            sleep(silence_balancer + remainder_use)

            key = bars_count
            rxs[key] = (rx)
            dts[key] = (note_length)
            sls[key] = (silence_balancer)

            bars_count += 1

            if bars_count == 17:
                break

        except KeyboardInterrupt:
            midiout.send_message(note_off)
            del midiout
            exit()

    # Debug
    log.debug("{:<8} {:<15}".format('Key','Label'))
    for k, v in zip(rxs.keys(), rxs.values()):
        log.debug("{:<8} {:<15}".format(k, v))

    log.debug("{:<8} {:<15}".format('Key','Label'))
    for k, v in zip(dts.keys(), dts.values()):
        log.debug("{:<8} {:<15}".format(k, v))

    log.debug("{:<8} {:<15}".format('Key','Label'))
    for k, v in zip(sls.keys(), sls.values()):
        log.debug("{:<8} {:<15}".format(k, v))

    while True:
        try:
            for bars_count in range(1, 17):
                note_on = [0x90, rxs[bars_count], 112]
                midiout.send_message(note_on)
                sleep(dts[bars_count])

                note_off = [0x80, rxs[bars_count], 0]
                midiout.send_message(note_off)
                sleep(sls[bars_count])

        except KeyboardInterrupt:
            midiout.send_message(note_off)
            del midiout
            exit()