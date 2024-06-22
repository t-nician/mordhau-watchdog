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
    callback: () = field(default=lambda _: (_))
    type: BroadcastType = field(default=BroadcastType.UNKNOWN)


@dataclass
class Watchdog:
    host: str = field(default="")
    port: int = field(default=0)
    passwd: str = field(default="")
    
    listeners: list[BroadcastListener] = field(default_factory=list)
    transformer: () = field(default=lambda _: (_))

    client: None | Client = field(default=None)
    
    def broadcast_transformer(self, callback):
        self.transformer = callback
        def wrapper(*args, **kwargs):
            return callback(*args, **kwargs)
        return wrapper
    
    
    def on_broadcast(self, type: BroadcastType):
        def wrapper(callback):
            self.listeners.append(BroadcastListener(
                callback=callback,
                type=type
            ))
        return wrapper
    
    
    def __broadcast_loop(self):
        with Client(self.host, self.port, passwd=self.passwd) as client:
            self.client = client
            
            while True:
                broadcast_packet = client.run("listen", "chat") # TODO mordhau quirk stuff. shouldn't be here once this is "done"
                broadcast_type, *data = self.transformer(broadcast_packet)
                
                for listener in self.listeners:
                    if listener.type == broadcast_type:
                        listener.callback(*data)
                
                
        """print(await rcon(
            "listen", "chat", 
            host=self.host, port=self.port, passwd=self.passwd
        ))
        
        while True:
            broadcast_packet = await rcon(
                "alive",
                host=self.host, port=self.port, passwd=self.passwd
            )
            
            print(broadcast_packet)"""

    
    def __command_watchdog(self):
        #self.__
        pass
    
    
    def start(self):
        run(self.__broadcast_loop())
        self.__command_watchdog()
        
        
        
        