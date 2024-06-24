import json5

from mcon.watchdog import Watchdog


def from_config(config_path: str) -> Watchdog:
    with open(config_path, "r") as file:
        config = json5.loads(file.read())

        watchdog = Watchdog(
            host=config["host"],
            port=config["port"],
            passwd=config["password"],
        )
        
        return watchdog
    