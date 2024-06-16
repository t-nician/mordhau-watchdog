import json5

from mcon.database import Playtime

from mcon.watchdog import Watchdog
from mcon.command import Command


def from_config(config_path: str) -> Watchdog:
    with open(config_path, "r") as file:
        config = json5.loads(file.read())
        watchdog = Watchdog(
            address=config["rcon"]["address"],
            password=config["rcon"]["password"],
            ratelimit=config["rcon"]["ratelimit"]
        )
        
        
        return watchdog
