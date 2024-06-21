import time

from enum import Enum
from dataclasses import dataclass, field

from mcon.session import Session
from mcon.watchdog import Command

from mcon.quirks.playfab import PlayfabPlayer



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
class MordhauSession(Session):
    playerlist: list[MordhauPlayer] = field(default_factory=list)
    chatlogs: list[Chatlog] = field(default_factory=list)
    
    chat_commands: dict[str, (tuple[MordhauPlayer, str])] = field(default_factory=list)
    
    def chat_command(self, command: str, args: int = 0):
        def wrapper(callback: (tuple[MordhauPlayer, str])):
            print(callback)
        return wrapper
    
    
    def prestart(self):
        @self.watchdog.command(Command("playerlist"), interval_seconds=1)
        def playerlist(command: Command):
            print(command.result)
    