import os.path
from time import time

SILENT = False

def set_silent(silent):
    global SILENT
    SILENT = silent

def timed(tag, message):
    global silent

    def decorated(func):
        def wrapper(*args, **kwargs):
            s_args = []
            if 'solver' in kwargs:
                s_args.append(kwargs['solver'])
            if 'model' in kwargs:
                s_args.append(kwargs['model'])

            if not SILENT: print_colors('{YELLOW}' + tag + '{ENDC}', message, ''.join(s_args), '...', end='\r')
            start = time()
            response = func(*args, **kwargs)
            if not SILENT: print_colors('{YELLOW}' + tag + '{ENDC}', message, '[{GREEN}done{ENDC}]', '{BLUE}' + '{:8.2f}ms'.format((time() - start) * 1000) + '{ENDC}')
            return response
        return wrapper
    return decorated

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_colors(*args, **kwargs):
    formatted = []
    for msg in args:
        formatted.append(str(msg).format(
            BLUE=bcolors.OKBLUE,
            GREEN=bcolors.OKGREEN,
            RED=bcolors.FAIL,
            YELLOW=bcolors.WARNING,
            ENDC=bcolors.ENDC
        ))
    print(*formatted, **kwargs)
