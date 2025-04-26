# -----------
# - r41ngee -
# -----------

import subprocess


def cls():
    """Очищает консоль.

    Использует команду cls через subprocess для очистки консоли.
    Работает только в Windows.
    """
    subprocess.run("cls", shell=True)
