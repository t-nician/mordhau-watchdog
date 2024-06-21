from dataclasses import dataclass, field

from mcon.watchdog import Watchdog


@dataclass
class Session:
    watchdog: Watchdog
    
    def prestart():
        pass
    
    def start(self):
        self.prestart()
        self.watchdog.start()
        