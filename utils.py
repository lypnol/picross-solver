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

            if not SILENT: print(tag, message, ''.join(s_args), '...                       ', end='\r')
            start = time()
            response = func(*args, **kwargs)
            if not SILENT: print(tag, message, '{:.2f}ms'.format((time() - start) * 1000))
            return response
        return wrapper
    return decorated
