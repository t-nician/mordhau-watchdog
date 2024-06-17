import time

from rcon.source import Client
from dataclasses import dataclass, field, fields, asdict

from mcon.command import Command
from mcon.quirks import playfab, mordhau


@dataclass
class Watchdog:
    host: str = field(default="")
    port: int = field(default=0)
    
    password: str = field(default="")
    
    
    def command(self, command: any, interval_seconds: int = 5):
        def wrapper(callback: (any)):
            pass
        return wrapper
    
    
    def start(self):
        pass