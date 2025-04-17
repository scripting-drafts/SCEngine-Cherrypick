from subprocess import Popen, PIPE, STDOUT
import sys
user_input = ['1', '2', '1', '4']

communicate_argument = '\n'.join(''.join(user_input))
p = Popen([sys.executable, 'music_engine-sustain_trials.py'], stdout=PIPE, stdin=PIPE, stderr=STDOUT, encoding='utf-8')

stdout, stderr = p.communicate(communicate_argument)

print(stdout)

'''TODO: Testing for the frequency precision
Given shortest harmonic ranges (BASS 33-45)
When shortest Scales (Scottish Pentatonic - 1214)
Then OK

Given longest harmonic ranges (full spectrum)
When any scale is applied
Then all OK

Modify parameters in order to adjust to
dominants and rythms
'''