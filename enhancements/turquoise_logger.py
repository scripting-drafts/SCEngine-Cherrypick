import logging
import os

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
os.system('')

class Logger:
    def __init__(self):
        self.script_name = 'music_box'

    def RGB(self, red=None, green=None, blue=None, bg=False):
        '''Logger prettifier'''
        if(bg == False and red != None and green != None and blue != None):
            return f'\u001b[38;2;{red};{green};{blue}m'
        elif(bg == True and red != None and green != None and blue != None):
            return f'\u001b[48;2;{red};{green};{blue}m'
        elif(red == None and green == None and blue == None):
            return '\u001b[0m'

    def logging(self):
        '''Reusable logger'''
        g0 = self.RGB()
        g1 = self.RGB(127, 255, 212)
        g2 = self.RGB(0, 0, 128)
        bold = "\033[1m"
        reset = "\033[0m"
        logging.basicConfig(filename=f'resources/{self.script_name}.log', encoding='UTF-8', level=logging.DEBUG, format='%(asctime)s [%(name)s] %(message)s')
        
        logger = logging.getLogger(f'{self.script_name}')
        logger.setLevel(logging.DEBUG)

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter('%(asctime)s,%(msecs)03d {}{}[%(name)s]{}{} %(message)s'.format(bold, g1, g0, reset), '%H:%M:%S') # %(asctime)s,%(msecs)03d {}{}
        
        ch.setFormatter(formatter)
        logger.addHandler(ch)

        return logger
    