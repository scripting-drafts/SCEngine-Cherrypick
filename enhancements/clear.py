from os import name, system
from sys import stdout

def clear():
   # for mac and linux(here, name is 'posix')
   if name == 'posix':
      _ = system('clear')
   else:
      # for windows platfrom
      _ = system('cls')