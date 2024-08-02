from pathlib import Path

from ..settings import dice_roll_icons


def number_to_emoji(number: int):
    return ''.join([dice_roll_icons[x] for x in str(number)] if number > 10 else [dice_roll_icons[str(number)]])


def get_project_root() -> Path:
    return Path(__file__).parent.parent
