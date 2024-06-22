import time

from enum import Enum
from dataclasses import dataclass, field

from mcon.quirks.playfab import PlayfabPlayer

class EventType(Enum):
    PLAYER_LEAVE = "player_left"
    PLAYER_JOIN = "player_join"
    

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


