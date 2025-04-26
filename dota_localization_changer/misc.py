# -----------
# - r41ngee -
# -----------

import subprocess


def cls():
    """Очищает консоль.

    Использует команду cls/clear через subprocess для очистки консоли.
    Работает на Windows и Unix-подобных системах.
    """
    import os

    if os.name == "nt":  # Windows
        subprocess.run("cls", shell=True)
    else:  # Unix/Linux/MacOS
        subprocess.run("clear", shell=True)
