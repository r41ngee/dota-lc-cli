import logging
import os


def clear_console():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def keylog(key, val):
    logging.info(f"New value for key \"{key}\": \"{val}\"")

def endlog(code: int):
    logging.info(f"Program exit with code {hex(code)}")