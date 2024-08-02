from pathlib import Path

from ..settings import roll_icons


def number_to_emoji(number: int):
    return ''.join([roll_icons[x] for x in str(number)] if number > 10 else [roll_icons[str(number)]])


def get_project_root() -> Path:
    return Path(__file__).parent.parent
