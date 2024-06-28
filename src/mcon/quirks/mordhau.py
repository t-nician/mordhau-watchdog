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
            if packet is None:
                return BroadcastType.UNKNOWN, ""
            
            payload_str = packet.payload.decode()
            
            if payload_str.startswith("Login:"):
                split = payload_str[len("Login:")::].split(": ")
                
                raw_str = split[1].removeprefix(" ")
                
                name = raw_str.removesuffix(") logged out").removesuffix(") logged in")[0:len(raw_str) - 29].removesuffix(" ")
                playfab = raw_str[len(raw_str) - 28::].removeprefix("(").removesuffix(") logged out").removesuffix(") logged in")

                mordhau_player = MordhauPlayer(
                    name=name,
                    id=playfab.removeprefix("(").removesuffix(")")
                )
                             
                return EventType.PLAYER_PRESENCE, mordhau_player, raw_str.endswith("logged in")

            
            if payload_str.startswith("Chat:"):
                split = payload_str[len("Chat:")::].split(",")          

                playfab, name = split[0].removeprefix(" "), split[1].removeprefix(" ")
                mordhau_player = MordhauPlayer(name=name, id=playfab)
                
                raw_message = ",".join(split[2::]).removeprefix(" ")
                target_end = raw_message.find(")")

                channel = raw_message[0:target_end + 1]
                processed_message = raw_message[target_end + 2::].removesuffix("\n")
                
                return EventType.PLAYER_CHAT, mordhau_player, channel, processed_message
            
            return BroadcastType.UNKNOWN, ""
        
        for type in types:
            self.watchdog.queued_commands.append(("listen", type.value))
        
        self.watchdog.start()