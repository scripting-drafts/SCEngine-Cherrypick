import colorama

import enhancements.mod_initializer as gui_enhancements
import enhancements.turquoise_logger as turquoise_logger
import pandas as pd
import numpy as np
from itertools import cycle
import random
import re
import rtmidi
from time import sleep
from enhancements.clear import clear
from sys import exit
from time import sleep
from resources.timer import Timer
from resources.multireplacer import multireplacer_initializer
from resources.scales import section_scales


midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()

colorama.init()
GREEN = colorama.Fore.GREEN
GRAY = colorama.Fore.LIGHTBLACK_EX
RESET = colorama.Fore.RESET
RED = colorama.Fore.RED

gui_enhancements.run_music_engine()

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
    selected_port = 0
    midiout.open_port(selected_port)
else:
    midiout.open_virtual_port("My virtual output")


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

    scale_names_for_input = ''.join([''.join(s[1]) for s in scales_for_input]).replace('  ', '\n')

    return scale, list_scale, s_gui_result, s

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
#    log.debug('Scale Result: {}'.format(s_gui_result))

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

    return hr

normal_scales = {
    'diminished': [2, 4, 6, 7, 9],
    'major': [0, 2, 4, 5, 7, 9, 11, 12],
    'minor': [0, 1, 3, 5, 7, 8, 10, 12],
    'augmented': [3, 5, 6, 8, 10]
        }
clear()

scale = int(input('''
    Choose a scale or a group:
    1. Standard
    2. Other
                  
    3. diminished
    4. minor            
    5. major
    6. augmented

    '''))

if scale == 1:
    modes = ['Ecclesiastical Modes', 'Bebop']

    scales_option = int(input('''
    1. Ecclesiastical Modes
    2. Bebop, Blues and more

    '''))
    mode = ''.join([modes[scales_option - 1]])
    log.info(f'6 - {mode} Scales - Choose One')  # log debug
    
    df = pd.read_excel('resources/scales/Scales-Standard.xlsx', sheet_name=mode, index_col=0, header=0)
    geographically_located_scales = set([geo for geo in df.index.to_list() if geo is not np.nan])
    sorted_geographically_scales = sorted(geographically_located_scales)

    len_geo_scales = len(sorted_geographically_scales)
    listed_geo_scales = ''.join([f'{str(num)}. {i}  ' for num, i in zip(range(1, len_geo_scales + 1 ), sorted_geographically_scales)])
    formatted_geo_scales = listed_geo_scales.replace('  ', '\n')

    scales = int(input(f'\n{formatted_geo_scales}')) - 1 # (list vs GUI) input debug
    chosen_geoloc = sorted(set([geo for geo in df.index.to_list() if geo is not np.nan]))[scales]

    print(f'1 - Scales - {chosen_geoloc} Group')

    clear()
    scales_data = section_scales.section_scales(chosen_geoloc, df)
    scale, list_scale, s_gui_result, s = select_scale(scales_data)

    # debug
    # n=[i for i in range(33, 94)]
    # n = [[e, i] for i, e in zip(cycle(s), n)]

elif scale == 2:
    log.info('2 - Scale Grouped by Geolocation - Choose a Group')
    sheet = 'Generic'
    df = pd.read_excel('resources/scales/Scales-Other.xlsx', sheet_name=sheet, index_col=0, header=0)
    geographically_located_scales = set([geo for geo in df.index.to_list() if geo is not np.nan])
    sorted_geographically_scales = sorted(geographically_located_scales)
    
    len_geo_scales = len(sorted_geographically_scales)
    listed_geo_scales = ''.join([f'{str(num)}. {i}  ' for num, i in zip(range(1, len_geo_scales + 1 ), sorted_geographically_scales)])
    formatted_geo_scales = listed_geo_scales.replace('  ', '\n')
    
    scales = int(input(f'\n{formatted_geo_scales}')) - 1 # (list vs GUI)
    chosen_geoloc = sorted(set([geo for geo in df.index.to_list() if geo is not np.nan]))[scales]
    
    clear()
    log.info(f'2 - Scale Groups - {chosen_geoloc}')
    scales_data = section_scales.section_scales(chosen_geoloc, df)
    scale, list_scale, s_gui_result, s = select_scale(scales_data)

elif scale in [x + 1 for x in range(1, len(normal_scales) + 1)]:
    # keys = normal_scales.keys()
    # it = normal_scales.items()
    # s = it[scale]
    # log.info(f'3, 4, 5, 6 - Normal Scale Groups - {keys[scale]} chosen')
    # TODO
    pass

else:
    print('Wrong option')
    exit()

display_acquired_info(s)

harmonic_range = [33, 94]
s = s + [x + 12 for x in s if x != 0] + [x + 24 for x in s if x != 0]
hr = range_increments(start=harmonic_range[0], stop=harmonic_range[1], steps=s)

bars_count = 1 
rxs = {}
bend = {}
dts = {}
sls = {}

remainder, remainder_use = None, None
times = Timer()




print(hr)

with midiout:
    sleep(.3)
    while True:
        try:
            note = random.choice(hr)
            case = None
            bend_receiver = None
            print(str(note))

            if '.5' in str(note):
                case = 1
                center = hr.index(note)
                if center in range(len(hr), len(hr) - 3) and center in range(len(hr), len(hr) + 3):
                    distribution = [hr[x] for x in range(center - 3, center + 3)]
                    bend_receiver = random.choice(distribution)
                else:
                    bend_receiver = random.choice(hr)

                rx = note # [x for x in s if x != rx or x != rx1 or x != rx2 or x != rx3 or x != rx4 or x != rx5 or x != rx6]
                note_on = [0xE0, rx, bend_receiver]
            elif '.0' in str(note):
                case = 2
                rx = note # [x for x in s if x != rx or x != rx1 or x != rx2 or x != rx3 or x != rx4 or x != rx5 or x != rx6]
                note_on = [0x90, rx, 112]
                bend_receiver = None

            midiout.send_message(note_on)

            if remainder_use is not None:
                note_length = times.formulate_time(remainder)
            else:
                note_length = times.formulate_time()

            if bend_receiver is not None:
                log.debug(f'Note On: {rx}')
                log.debug(f'{note_length=}')
            else:      
                log.debug(f'Note On: {rx} Bend Receiver: {bend_receiver}')
                log.debug(f'{note_length=}')
    
            note_off = [0x80, rx, 0]
            midiout.send_message(note_off)
            silence_balancer, remainder = times.even_time(note_length)
            log.debug(f'{silence_balancer=}')

            remainder_use = random.choice([remainder, 0.])
            remainder_use = remainder_use if remainder is not None else 0
            sleep(silence_balancer + remainder_use)

            log.debug(f'Note Off: {rx}')
        
            # Bars and vuelta length
            key = bars_count
            rxs[key] = (rx)
            bend[key] = bend_receiver
            dts[key] = (note_length)
            sls[key] = (silence_balancer)

            bars_count += 1

            if bars_count == 17:
                break

        except KeyboardInterrupt:
            midiout.send_message(note_off)
            del midiout
            exit()

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