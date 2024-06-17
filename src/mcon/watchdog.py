import time

from rcon.source import Client
from dataclasses import dataclass, field, asdict

from mcon.command import Command
from mcon.quirks import playfab, mordhau

@dataclass
class Watchdog:
    pass