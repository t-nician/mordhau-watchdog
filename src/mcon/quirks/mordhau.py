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
            
            #print(payload_str)
            
            if payload_str.startswith("Login:"):
                #Login: 2024.06.28-15.04.09: Edentage (8A0461F1C969789C) logged out
                split = payload_str[len("Login:")::].split(":")#.split(":")[0].removesuffix(":")
                stamp = split[0].removesuffix(":")
                
                name = split[1][len(stamp)::len(split[1]) - 29]
                playfab = split[1][len(split[1]) - 29::]
                
                print("test", split)
                
                result = payload_str[len("Login:") + len(stamp) + 2::].split(" ")

                mordhau_player = MordhauPlayer(
                    name=name,
                    id=playfab.removeprefix("(").removesuffix(")")
                )
                             
                return EventType.PLAYER_PRESENCE, mordhau_player, "".join(result[2::]) == "loggedin"

            
            if payload_str.startswith("Chat:"):
                split = payload_str[len("Chat:")::].split(",")          

                playfab, name = split[0].removeprefix(" "), split[1].removeprefix(" ")
                mordhau_player = MordhauPlayer(name=name, id=playfab)
                
                raw_message = ",".join(split[2::]).removeprefix(" ")
                target_end = raw_message.find(")")

                channel = raw_message[0:target_end + 1]
                processed_message = raw_message[target_end + 2::].removesuffix("\n")
                
                return EventType.PLAYER_CHAT, mordhau_player, channel, processed_message
        
        for type in types:
            self.watchdog.queued_commands.append(("listen", type.value))
        
        self.watchdog.start()