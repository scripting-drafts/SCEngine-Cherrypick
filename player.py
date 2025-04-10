from sys import argv
import re
from time import sleep
import rtmidi

midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()

port = 0 # Side-Chain
file = argv[1]
first_silence = False

f = open(file, 'r', encoding='utf-8').readlines()

# remove 2025-04-10 14:22:40,007 [music_box]
f = [line.split('[music_box]')[1].strip() for line in f]

# books = [''.join(f).split('')]
# f = [line.split(' ') for line in f]
# f = [line.strip() for line in f]

if first_silence == False:
    notes = ''.join(f).split('Key      Label')[1:]
    # notes, silence_during, silence_after = ''.join(notes).split(' ')[1], ''.join(silence_during).split(' ')[1], ''.join(silence_after).split(' ')[1]
else:   ### TODOOOOOOOOO
    notes, silence_pre, silence_during, silence_after = f.split('Key      Label')
    notes, silence_pre, silence_during, silence_after = ''.join(notes).split(' ')[1], ''.join(silence_during).split(' ')[1], ''.join(silence_after).split(' ')[1]


for note in ''.join(f).split('Key      Label')[1:]:
    print(note)

# while True:
#         try:
#             for bars_count in range(1, 33):
#                 if first_silence == True:
#                     sleep(silence_pre[bars_count])
                
#                 note_on = [0x90, notes[bars_count], 112]
#                 midiout.send_message(note_on)
#                 sleep(silence_during[bars_count])

#                 note_off = [0x80, notes[bars_count], 0]
#                 midiout.send_message(note_off)
#                 sleep(silence_after[bars_count])

#         except KeyboardInterrupt:
#             midiout.send_message(note_off)
#             del midiout
#             exit()