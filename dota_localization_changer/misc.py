# -----------
# - r41ngee -
# -----------

import logging
import os


def cls():
    os.system("cls")


def keylog(key, val):
    logging.info(f'New value for key "{key}": "{val}"')


def endlog(code: int):
    logging.info(f"Program exit with code {hex(code)}")
