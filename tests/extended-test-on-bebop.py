import pandas as pd
import numpy as np
from itertools import cycle
import random
import re
import rtmidi
from time import sleep
from ..resources.multireplacer import multireplacer_initializer

midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()

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

def section_standard_scales(chosen_geoscale, df):
    # Ecclesiastical
    if chosen_geoscale == 'Major & Natural Minor (N.M.)':
        scales_data = df.iloc[0:7]
    elif chosen_geoscale == 'Harmonic Minor (H.M.)':
        scales_data = df.iloc[7:14]
    elif chosen_geoscale == 'Melodic Minor (M.M.)':
        scales_data = df.iloc[14:21]
        # Bebop
    elif chosen_geoscale == 'Bebop':
        scales_data = df.iloc[0:4]
    elif chosen_geoscale == 'Blues':
        scales_data = df.iloc[4:9]
    elif chosen_geoscale == 'Gypsy':
        scales_data = df.iloc[9:13]
    elif chosen_geoscale == 'Pentatonics':
        scales_data = df.iloc[13:18]
    elif chosen_geoscale == 'Whole-Half':
        scales_data = df.iloc[18:21]
    elif chosen_geoscale == 'Other':
        scales_data = df.iloc[21:34]

    return scales_data

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

    print(scale)
    
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

df = pd.read_excel('../resources/scales/Scales-Standard.xlsx', sheet_name='Bebop', index_col=0, header=0)
geographically_located_scales = set([geo for geo in df.index.to_list() if geo is not np.nan])
sorted_geographically_scales = sorted(geographically_located_scales)

len_geo_scales = len(sorted_geographically_scales)
listed_geo_scales = ''.join([f'{str(num)}. {i}  ' for num, i in zip(range(1, len_geo_scales + 1 ), sorted_geographically_scales)])
formatted_geo_scales = listed_geo_scales.replace('  ', '\n')

scales = int(input(f'\n{formatted_geo_scales}')) - 1 # input
chosen_geoloc = sorted(set([geo for geo in df.index.to_list() if geo is not np.nan]))[scales]

print(f'6 - Scales - {chosen_geoloc} Group')


# clear()
scales_data = section_standard_scales(chosen_geoloc, df)
scale, list_scale, s_gui_result, s = select_scale(scales_data)


n=[i for i in range(33, 94)]
n = [[e, i] for i, e in zip(cycle(s), n)]

# print(n)

harmonic_range = [33, 94]
s = s + [x + 12 for x in s if x != 0] + [x + 24 for x in s if x != 0]

def range_increments(start=33, stop=95, steps=s):
    i = 0
    hr = []
    for _ in steps:
        hr.append(start + steps[i] - 1)
        i += 1

    print(hr)

    return hr
        
hr = range_increments()
print(hr)


with midiout:
    sleep(1)
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

            midiout.send_message(note_on)
            if remainder_use is not None:
                note_length = times.formulate_time(remainder)
            else:
                note_length = times.formulate_time()
            log.debug(f'{rx=}')
            log.debug(f'{note_length=}')
            sleep(note_length)

            if bend_receiver == None:
                print(f'Note On: {rx}')
            else:      
                print(f'Note On: {rx} Bend Receiver: {bend_receiver}')
    
            sleep(3)

            note_off = [0x80, rx, 0]
            midiout.send_message(note_off)
            print(f'Note Off: {rx}')
        

        except KeyboardInterrupt:
            midiout.send_message(note_off)
            del midiout
            exit()
# for i in cycle(s):
#     if i[:2] != 00:
#         random.choice()
# n = [harmonic_range[i] for i in s if i ==]

# print([x for x in range(*harmonic_range, cycle(s))])