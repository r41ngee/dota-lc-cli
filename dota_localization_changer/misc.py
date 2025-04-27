# -----------
# - r41ngee -
# -----------

"""Вспомогательные функции для Dota 2 Localization Changer."""

import os
import subprocess


def cls() -> None:
    """Очищает консоль.

    Использует команду cls/clear через subprocess для очистки консоли.
    Работает на Windows и Unix-подобных системах.
    """
    os.system("cls" if os.name == "nt" else "clear")


def run_command(command: str, check: bool = True) -> subprocess.CompletedProcess:
    """Запускает команду в подпроцессе.

    Args:
        command: Команда для выполнения
        check: Если True, вызывает исключение при ненулевом коде возврата

    Returns:
        Объект CompletedProcess с результатами выполнения команды
    """
    return subprocess.run(
        command, shell=True, check=check, capture_output=True, text=True
    )
