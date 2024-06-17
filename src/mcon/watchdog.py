import time
import asyncio

from rcon.source import Client


class Watchdog:
    def __init__(self, address: str, password: str, interval: int, interval_overrides: dict[str, int]):
        self.listeners: dict[str, (str)] = {}
        
        self.address = address
        self.password = password
        
        self.command_interval = interval
        self.interval_overrides = interval_overrides
        
        self.client = None
        
    
    def command(self, str: str):
        def wrapper(func: (str)):
            self.listeners[str] = func
            return func
        return wrapper
    
    
    def send(self, command: str) -> str:
        return self.client.run(command)
    
    
    def start(self):
        seconds_since_interval = 0
        seconds_since_override_interval = {}
        
        for command, _ in self.interval_overrides.items():
            seconds_since_override_interval[command] = 0
        
        (host, port) = self.address.split(":")
        
        with Client(host, int(port), passwd=self.password) as client:
            self.client = client
            
            while True:
                seconds_since_interval += 1
                
                if seconds_since_interval >= self.command_interval:
                    for command, callback in self.listeners.items():
                        if not self.interval_overrides[command]:
                            callback(self.send(command)) # TODO get command from rcon!
                
                for command, current_time in seconds_since_override_interval.items():
                    current_time += 1
                    seconds_since_override_interval[command] = current_time
                    
                    if current_time >= self.interval_overrides[command]:
                        self.listeners[command](self.send(command)) # TODO get command! from rcon!
                        seconds_since_override_interval[command] = 0
                
                time.sleep(1)