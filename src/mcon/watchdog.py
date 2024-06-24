import time

from rcon.source import rcon, Client

from enum import Enum

from asyncio import run
from dataclasses import dataclass, field, fields, asdict, replace


class BroadcastType(Enum):
    UNKNOWN = "unknown"
    CHAT = "chat"


@dataclass
class BroadcastListener:
    callback: () = field(default=lambda *_: _)
    type: BroadcastType = field(default=BroadcastType.UNKNOWN)


@dataclass
class Watchdog:
    host: str = field(default="")
    port: int = field(default=0)
    passwd: str = field(default="")
    
    listeners: list[BroadcastListener] = field(default_factory=list)
    async_execution: list[tuple[str, str]] = field(default_factory=list)
    transformer: () = field(default=lambda *_: _)

    client: None | Client = field(default=None)
    
    def broadcast_transformer(self, callback):
        self.transformer = callback

        def wrapper(*args, **kwargs):
            return callback(*args, **kwargs)
        return wrapper
    
    def on_broadcast(self, _type: BroadcastType):
        def wrapper(callback):
            self.listeners.append(BroadcastListener(
                callback=callback,
                type=_type
            ))
        return wrapper

    def __broadcast_loop(self):
        with Client(self.host, self.port, passwd=self.passwd) as client:
            self.client = client
            self.client.timeout = 1
            
            while True:
                
                broadcast_packet = None
                
                try:
                    broadcast_packet = client.read()
                except:
                    pass
                
                while len(self.async_execution) > 0:
                    client.run(*self.async_execution.pop())
                
                if broadcast_packet is None:
                    continue
                
                broadcast_type, *data = self.transformer(broadcast_packet)
                
                for listener in self.listeners:
                    if listener.type == broadcast_type:
                        listener.callback(*data)
    
    async def listen_async(self, command: str, *args: list[str]):
        self.async_execution.append((command, *args))
        
        await rcon(
            command, 
            *args, 
            host=self.host, 
            port=self.port, 
            passwd=self.passwd
        )
    
    def __command_watchdog(self):
        pass

    def start(self):
        run(self.__broadcast_loop())
        self.__command_watchdog()
        
        
        
        