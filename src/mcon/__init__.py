import json5

from mcon.database import Playtime

from mcon.watchdog import Watchdog


def from_config(config_path: str) -> Watchdog:
    with open(config_path, "r") as file:
        config = json5.loads(file.read())

        watchdog = Watchdog(
            address=config["rcon"]["address"],
            password=config["rcon"]["password"],
            interval=config["watchdog"]["command_interval"],
            interval_overrides=config["watchdog"]["command_interval_override"]
        )
        
        return watchdog
