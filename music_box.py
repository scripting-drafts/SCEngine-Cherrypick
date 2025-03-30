import rtmidi
from time import sleep
import random
from sys import exit
import colorama
import enhancements.turquoise_logger as turquoise_logger
import enhancements.mod_initializer as gui_enhancements

colorama.init()
GREEN = colorama.Fore.GREEN
GRAY = colorama.Fore.LIGHTBLACK_EX
RESET = colorama.Fore.RESET
RED = colorama.Fore.RED

gui_enhancements.run_music_box_engine()
logg = turquoise_logger.Logger()
log = logg.logging()

midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()
log.debug(f'Available Ports: {available_ports}')

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

class Timer:
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
    def formulate_time(self, remainder=None):
        t = random.uniform(0.0000000000000000, 0.4285714285714286)
        if remainder is not None:
            t = t + remainder
        
        return t
    
    def even_time(self, t):
        even= 0.4285714285714286 - t
        if t != 0:
            summary = even + t
            remainder = 0.4285714285714286 - summary

        if remainder == 0:
            remainder = None

        return even, remainder

bars_count = 1
rxs = {}
dts = {}
sls = {}
remainder, remainder_use = None, None

with midiout:
    # debugging
    sleep(1)
    while True:
        try:
            rx = n[random.choice([x for x in s if x != rx or x != rx1 or x != rx2 or x != rx3 or x != rx4 or x != rx5 or x != rx6])]
            note_on = [0x90, rx, 112]
            midiout.send_message(note_on)
            if remainder_use is not None:
                note_length = Timer().formulate_time(remainder)
            else:
                note_length = Timer().formulate_time()
            log.debug(f'{rx=}')
            log.debug(f'{note_length=}')
            sleep(note_length)

            note_off = [0x80, rx, 0]
            midiout.send_message(note_off)
            silence_balancer, remainder = Timer().even_time(note_length)
            log.debug(f'{silence_balancer=}')

            remainder_use = random.choice([remainder, 0.])
            remainder_use = remainder_use if remainder is not None else 0
            sleep(silence_balancer + remainder_use)
            # Always None
            # log.debug(f'{remainder=}')
            
            # def save_melody_roll(bars_count, rx, note_length, silence_balancer):
            key = bars_count
            rxs[key] = (rx)
            dts[key] = (note_length)
            sls[key] = (silence_balancer)
            
            # save_melody_roll(bars_count, rx, note_length, silence_balancer)
            # No repeat notes
            # rx1, rx2, rx3, rx4 = rx, rx1, rx2, rx3

            bars_count += 1

            if bars_count == 17:
                break

            # for rx, note_length, silence_balancer in zip(rxs.values(), dts.values(), sls.values()):
            #     note_on = [0x90, rx, 112]
            #     midiout.send_message(note_on)
            #     sleep(note_length)

            #     note_off = [0x80, rx, 0]
            #     midiout.send_message(note_off)
            #     sleep(silence_balancer)



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