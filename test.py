from subprocess import Popen, PIPE, STDOUT
import sys
user_input = ['1', '1', '3', '7']

communicate_argument = '\n'.join(''.join(user_input))
p = Popen([sys.executable, 'music_engine-sustain_trials.py'], stdout=PIPE, stdin=PIPE, stderr=STDOUT, encoding='utf-8')

stdout, stderr = p.communicate(communicate_argument)

print(stdout)