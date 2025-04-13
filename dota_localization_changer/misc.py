# -----------
# - r41ngee -
# -----------

import logging
import os
import json

with open("data/config.json", "r") as f:
    config = json.load(f)


def cls():
    os.system("cls")

def getLogLevel():
    config_logger_level_dict = {
        "info": logging.INFO,
        "error": logging.ERROR,
        "debug": logging.DEBUG,
        "warning": logging.WARNING,
        "warn": logging.WARN
    }

def keylog(key, val):
    logging.info(f"New value for key \"{key}\": \"{val}\"")

def endlog(code: int):
    logging.info(f"Program exit with code {hex(code)}")