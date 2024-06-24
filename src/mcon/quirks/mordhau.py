import time

from enum import Enum

from asyncio import run
from dataclasses import dataclass, field

from mcon.watchdog import Watchdog, BroadcastType
from mcon.quirks.playfab import PlayfabPlayer


class EventType(Enum):
    PLAYER_PRESENCE = "login"
    PLAYER_CHAT = "chat"
    

class PlayerType(Enum):
    ADMIN = "admin"
    PLAYER = "player"


@dataclass
class MordhauPlayer(PlayfabPlayer):
    team: str = field(default="")
    ping: str = field(default="")
    
    type: PlayerType = field(default=PlayerType.PLAYER)
    

@dataclass
class Chatlog(PlayfabPlayer):
    player: MordhauPlayer = field(default_factory=MordhauPlayer)
    
    message: str = field(default="")
    timestamp: int = field(default=0)


@dataclass
class MordhauSession:
    watchdog: Watchdog = field(default_factory=Watchdog)
    
    def listen(self, *types: list[EventType]):
        @self.watchdog.broadcast_transformer
        def transformer(packet):
            payload_str = packet.payload.decode()
            
            if payload_str.startswith("Login:"):
                print(payload_str)
                return EventType.PLAYER_PRESENCE, payload_str[len("Login:")::]

            if payload_str.startswith("Chat:"):
                split = payload_str[len("Chat: ")::].split(",")          

                playfab, name = split[0], split[1]
                mordhau_player = MordhauPlayer(name=name, id=playfab)
                
                raw_message = "".join(split[2::]).removeprefix(" ")
                target_end = raw_message.find(")")

                channel = raw_message[0:target_end + 1]
                processed_message = raw_message[target_end + 2::]
                
                return EventType.PLAYER_CHAT, mordhau_player, channel, processed_message
        
        
        #@self.watchdog.on_broadcast(EventType.PLAYER_CHAT)
        #def chat(playfab, name, channel, message):
        #    print("chat payload", payload)
            
        
        for type in types:
            run(self.watchdog.listen_async("listen", type.value))
        
        self.watchdog.start()