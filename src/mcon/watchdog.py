from mcon.command import Command


class Watchdog:
    def __init__(self, address: str, password: str, ratelimit: int):
        self.listeners: dict[str, (Command)] = {}
        
    
    def command(self, str: str):
        def wrapper(func: (Command)):
            self.listeners[str] = func
            return func
        return wrapper
        
    
    def start(self):
        pass