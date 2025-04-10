import colorama
import enhancements.mod_initializer as gui_enhancements
import enhancements.turquoise_logger as turquoise_logger
import pandas as pd
import numpy as np
import random
import re
import rtmidi
from time import sleep
from sys import exit
from time import sleep
from resources.timer import Timer
from enhancements.multireplacer import multireplacer_initializer
from resources.scales import section_scales
from resources.harmonic_ranges import get_harmonic_range

midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()

port = 0 # Side-Chain
first_silence = False # silence_pre function in the Timer class

colorama.init()
GREEN = colorama.Fore.GREEN
GRAY = colorama.Fore.LIGHTBLACK_EX
RESET = colorama.Fore.RESET
RED = colorama.Fore.RED

# gui_enhancements.run_music_engine()

tl_log = turquoise_logger.Logger()
log = tl_log.logging()

replacements_ports = {
    '[': '', ']':'',
    r'\'':'',
    ', ':'\n',
    '(':'',
    ')':'',
}

if available_ports:
    mr = multireplacer_initializer()
    listed_ports = mr.multireplace(re.sub(r'^\s', '', str(available_ports)), replacements_ports) # str([r'{} '.format(x) for x in available_ports]).split('\n')
    log.debug(f'Available Ports: \n\n{listed_ports} \n')
    selected_port = port
    midiout.open_port(selected_port)
    log.debug(f'Port #{selected_port} Open')
else:
    midiout.open_virtual_port("My virtual output")
    log.debug('W: Opened virtual port')

def select_scale(scales_data):
    scales_data_len = len(scales_data[:])

    scales_for_input = []
    for num, i, intervals, y in zip(range(1, scales_data_len + 1 ), scales_data['Name'], scales_data['Intervals'], scales_data['aka*']):
        if y != '-':
            scales_for_input.append([[f'{str(num)}. {i}, known like {y}  '], [intervals]])
        else:
            scales_for_input.append([[f'{str(num)}. {i}  '], [intervals]])

    scale_names_for_input = ''.join([''.join(s[0]) for s in scales_for_input]).replace('  ', '\n')
    scale_choice = int(input( f'\n {scale_names_for_input} \n')) - 1 # input
    scale = scales_for_input[scale_choice][1]
    scale = ''.join(scale)
    
    list_scale, s, s_gui_result = mutilate_scale(scale)

    # ???
    # scale_names_for_input = ''.join([''.join(s[1]) for s in scales_for_input]).replace('  ', '\n')

    name = ''.join(scales_for_input[scale_choice][0])
    name = ''.join(name.split('known like')[0])
    name = name[2:].replace(',', '')

    return scale, list_scale, s_gui_result, s, name

def mutilate_scale(scale):
    # log.debug(f'Default Scale: {scale}')
    s = []
    list_scale = [str(n) for n in scale.split('-')]
    for note in list_scale:
        if '#' in note:
            if '##' in note:
                note = note.replace(r'##', '')
                note = float(note) + 1.
            else:
                note = note.replace(r'#', '')
                note = float(note) + .5
        elif 'b' in note:
            if 'bb' in note:
                note = note.replace(r'bb', '')
                note = float(note) - 1.
            else:
                note = note.replace(r'b', '')
                note = float(note) - .5
        else:
            note = float(note)
        
        s.append(note)

    s_gui_result = make_scale_readable(s)

    return list_scale, s, s_gui_result

def make_scale_readable(s):
    s_gui_result = []

    for x in s:
        if x != s[-1]:
            s_gui_result.append('{:.2f}-'.format(x))
        elif x == s[-1]:
            s_gui_result.append('{:.2f}'.format(x))

    s_gui_result = ''.join(s_gui_result)

    return s_gui_result

def display_acquired_info(s):
    if s not in [scale for scale in normal_scales]:
        print('''
      
           {}
           {}
           {}
           {}
           
        {} <-> {}
              

      
            '''.format(scale, list_scale, s_gui_result, s, scale, s_gui_result))

def range_increments(start=33, stop=95, steps=None):
    i = 0
    hr = []
    for _ in steps:
        hr.append(start + steps[i] - 1)
        i += 1

<<<<<<< HEAD
    # 5 ~33-66
    hr = range_increments_extension(hr, steps, stop)
=======
    while hr[-1] <= stop:
        hr = range_increments_extension(hr, steps)
        
    hr = [hr.remove(x) for x in hr if x > stop]
>>>>>>> parent of 00d0d64 (harmonic range increments)

    hr = list(set(hr))

    return hr

def range_increments_extension(hr, steps, stop):
    i = 0
    start = hr[-1]
    while start + steps[i] - 1 < stop:
        hr.append(start + steps[i] - 1)
        i += 1

    return hr

def debug_midi_roll():
    log.debug("{:<8} {:<15}".format('Key','Label'))
    for k, v in zip(rxs.keys(), rxs.values()):
        log.debug("{:<8} {:<15}".format(k, v))

    if first_silence == True:
        log.debug("{:<8} {:<15}".format('Key','Label'))
        for k, v in zip(silence_pre.keys(), silence_pre.values()):
            log.debug("{:<8} {:<15}".format(k, v))

    log.debug("{:<8} {:<15}".format('Key','Label'))
    for k, v in zip(silence_during.keys(), silence_during.values()):
        log.debug("{:<8} {:<15}".format(k, v))

    log.debug("{:<8} {:<15}".format('Key','Label'))
    for k, v in zip(silence_after.keys(), silence_after.values()):
        log.debug("{:<8} {:<15}".format(k, v))

normal_scales = {
    'diminished': [2, 4, 6, 7, 9],
    'major': [0, 2, 4, 5, 7, 9, 11, 12],
    'minor': [0, 1, 3, 5, 7, 8, 10, 12],
    'augmented': [3, 5, 6, 8, 10]
        }
# clear()

scale = int(input('''
    Choose a scale or a group:
    1. Standard
    2. Other
                  
    3. Diminished
    4. Major            
    5. Minor
    6. Augmented

    '''))

if scale == 1:
    modes = ['Ecclesiastical Modes', 'Bebop']

    scales_option = int(input('''
    1. Ecclesiastical Modes
    2. Bebop, Blues and more

    '''))
    mode = ''.join([modes[scales_option - 1]])
    log.debug(f'{mode}')  # log debug
    
    df = pd.read_excel('resources/scales/Scales-Standard.xlsx', sheet_name=mode, index_col=0, header=0)
    geographically_located_scales = set([geo for geo in df.index.to_list() if geo is not np.nan])
    sorted_geographically_scales = sorted(geographically_located_scales)

    len_geo_scales = len(sorted_geographically_scales)
    listed_geo_scales = ''.join([f'{str(num)}. {i}  ' for num, i in zip(range(1, len_geo_scales + 1 ), sorted_geographically_scales)])
    formatted_geo_scales = listed_geo_scales.replace('  ', '\n')

    scales = int(input(f'\n{formatted_geo_scales}')) - 1 # (list vs GUI) input debug
    chosen_geoloc = sorted(set([geo for geo in df.index.to_list() if geo is not np.nan]))[scales]

    log.debug(f'{mode} - {chosen_geoloc}')

    # clear()
    scales_data = section_scales.section_scales(chosen_geoloc, df)
    scale, list_scale, s_gui_result, s, name = select_scale(scales_data)

    log.debug(f'{mode} - {chosen_geoloc} - {name}')

elif scale == 2:
    log.info('Geolocation Groups')
    sheet = 'Generic'
    df = pd.read_excel('resources/scales/Scales-Other.xlsx', sheet_name=sheet, index_col=0, header=0)
    geographically_located_scales = set([geo for geo in df.index.to_list() if geo is not np.nan])
    sorted_geographically_scales = sorted(geographically_located_scales)
    
    len_geo_scales = len(sorted_geographically_scales)
    listed_geo_scales = ''.join([f'{str(num)}. {i}  ' for num, i in zip(range(1, len_geo_scales + 1 ), sorted_geographically_scales)])
    formatted_geo_scales = listed_geo_scales.replace('  ', '\n')
    
    scales = int(input(f'\n{formatted_geo_scales}')) - 1 # (list vs GUI)
    chosen_geoloc = sorted(set([geo for geo in df.index.to_list() if geo is not np.nan]))[scales]
    
    # clear()
    log.info(f'Geolocation Groups - {chosen_geoloc}')
    scales_data = section_scales.section_scales(chosen_geoloc, df)
    scale, list_scale, s_gui_result, s, name = select_scale(scales_data)

    log.info(f'Geolocation Groups - {chosen_geoloc} - {name}')

elif scale in [x for x in range(3, 7)]:
    # # keys = normal_scales.keys()
    # # it = [i for i in normal_scales.items()]
    scale = scale - 3
    normal_scales = normal_scales.items()
    normal_scales = [list(i) for i in normal_scales]
    print(normal_scales[scale][1], normal_scales[scale][0])
    s = normal_scales[scale][1]
    log.info(f'3, 4, 5, 6 - Normal Scale Groups - {normal_scales[scale][0]} chosen')

else:
    print('Wrong option')
    exit()

harmonic_range = get_harmonic_range('medium')
# harmonic_range = [33, 94] Perfect
# s = s + [x + 12 for x in s if x != 0] + [x + 24 for x in s if x != 0]
hr = range_increments(start=harmonic_range[0], stop=harmonic_range[1], steps=s)

# display_acquired_info(s)

bars_count = 1 
rxs = {}
bend = {}
silence_pre = {} if first_silence == True else None
silence_during = {}
silence_after = {}

times = Timer()

'''
"0x90" Breakdown of MIDI MESSAGE:
"0x9": This part of the status byte (0x90) indicates that the message is a "Note On" message. 
"0": This part of the status byte (0x90) specifies that the message is intended for channel 1. 

'''

def debug_t():
    log.debug(f'{t=}')

def debug_bend_receiver():
    if bend_receiver is not None:
        log.debug(f'Note On: {rx}')
        
    else:      
        log.debug(f'Note On: {rx} Bend Receiver: {bend_receiver}')
        

t = 27.42857142857143
log.debug(hr)

with midiout:
    sleep(.3)
    while True:
        try:
            key = bars_count
            notes = random.sample(hr, k=random.randint(2, 8))
            case = None
            bend_receiver = None
            

            for note in notes:
                # DEBUG
                if first_silence == True:
                    if random.choice([True, True, False]) == True:
                        t, position = times.silent(t, 'Pre')
                        silence_pre[key] = (t)
                    else:
                        position = f'Pre: {t}'
                        t = 0.

                    silence_pre[key] = (t)
                    sleep(t)
                    log.debug(position)


                if '.5' in str(note):
                    case = 1
                    center = hr.index(note) # RANDOM SAMAAAAAMPLES:!
                    if center in range(len(hr), len(hr) - 3) and center in range(len(hr), len(hr) + 3):
                        distribution = [hr[x] for x in range(center - 3, center + 3)]
                        bend_receiver = random.choice(distribution)
                    else:
                        bend_receiver = random.choice(hr)

                    rx = note # [x for x in s if x != rx or x != rx1 or x != rx2 or x != rx3 or x != rx4 or x != rx5 or x != rx6]
                    note_on = [0xE0, rx, bend_receiver]
                if '.0' in str(note) or '.' not in str(note):
                    case = 2
                    rx = note # [x for x in s if x != rx or x != rx1 or x != rx2 or x != rx3 or x != rx4 or x != rx5 or x != rx6]
                    note_on = [0x90, rx, 112]
                    bend_receiver = None

                midiout.send_message(note_on)
                debug_bend_receiver()

                rxs[key] = (rx)
                bend[key] = (bend_receiver)

                t, position = times.silent(t, 'Sustain')
                silence_during[key] = (t)
                sleep(t)
                log.debug(position)


                # Notes off and sustain dev
                sustained_notes = []
        
                if random.uniform(0., 1.) < .7:
                    note_off = [0x80, rx, 0]
                    midiout.send_message(note_off)
                    log.debug(f'Note OFF: {rx}')
                    
                elif random.uniform(0., 1.) >= .7:
                    sustained_notes.append([rx, bars_count])

                    if len(sustained_notes) > 2:
                        for n in sustained_notes:
                            rx = n[0]
                            note_off = [0x80, rx, 0]
                            midiout.send_message(note_off)
                            log.debug(f'Note OFF: {rx}')
                
                elif len(sustained_notes) != 0:
                    if random.uniform(0., 1.) > .4:
                        rx = random.choice([sustained_notes])
                        rx = rx[0]
                        note_off = [0x80, rx, 0]
                        midiout.send_message(note_off)
                        log.debug(f'Note OFF: {rx}')

                elif bars_count == 33:
                    for n in sustained_notes:
                        rx = n[0]
                        note_off = [0x80, rx, 0]
                        midiout.send_message(note_off)
                        log.debug(f'Note OFF: {rx}')

                # End of notes off and sustain dev

                t, position = times.silent(t, 'After')
                silence_after[key] = (t)
                sleep(t)
                log.debug(position)

            bars_count += 1

            if bars_count == 33:
                break

        except KeyboardInterrupt:
            midiout.send_message(note_off)
            del midiout
            exit()

    debug_midi_roll()

    while True:
        try:
            for bars_count in range(1, 33):
                if first_silence == True:
                    sleep(silence_pre[bars_count])
                
                note_on = [0x90, rxs[bars_count], 112]
                midiout.send_message(note_on)
                sleep(silence_during[bars_count])

                note_off = [0x80, rxs[bars_count], 0]
                midiout.send_message(note_off)
                sleep(silence_after[bars_count])

        except KeyboardInterrupt:
            midiout.send_message(note_off)
            del midiout
            exit()


