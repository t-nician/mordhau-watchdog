from mcon.watchdog import Watchdog


def from_config(config_path: str) -> Watchdog:
    with open(config_path, "r") as file:
        pass