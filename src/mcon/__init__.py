from mcon.database import Playtime

from mcon.watchdog import Watchdog
from mcon.command import Command


def from_config(config_path: str) -> Watchdog:
    with open(config_path, "r") as file:
        return Watchdog()
