import time

from enum import Enum
from dataclasses import dataclass, field

from mcon.session import Session
from mcon.watchdog import Command

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


previous_playerlist: list[MordhauPlayer] = []
chat_history: list[Chatlog] = []


def player_is_in_list(list, player):
    for other in list:
        if other.id == player.id:
            return True


@dataclass
class MordhauSession(Session):
    playerlist: list[MordhauPlayer] = field(default_factory=list)
    chatlogs: list[Chatlog] = field(default_factory=list)
    
    chat_commands: dict[str, tuple[(tuple[MordhauPlayer, str]), int]] = field(default_factory=dict)
    event_listeners: list[tuple[EventType, (MordhauPlayer)]] = field(default_factory=list)
    
    def chat_command(self, command: str, args: int = 0):
        def wrapper(callback: (tuple[MordhauPlayer, str])):
            if self.chat_commands.get(command) is None:
                self.chat_commands[command] = (callback, args)
        return wrapper
    
    
    def on_event(self, event_type: EventType):
        def wrapper(callback: (MordhauPlayer)):
            self.event_listeners.append((event_type, callback))
        return wrapper
    
    
    def prestart(self):
        @self.watchdog.command(Command("chatlog", args=["5"]), interval_seconds=1)
        def chatlog(command: Command):
            global chat_history
            # WAHH
            difference = len(chat_history) - len(command.result)
            
            
                
                
            
        
        @self.watchdog.command(Command("playerlist"), interval_seconds=1)
        def playerlist(command: Command):
            global previous_playerlist
            
            if command.result == "There are currently no players present":
                for player in previous_playerlist: 
                    self.__fire_event(EventType.PLAYER_LEAVE, player)
                previous_playerlist = []
                return None
            
            player_str_list = command.result.split("\n")
            player_str_list.pop()
            
            current_playerlist = []
            
            for player_str in player_str_list:
                playfab, name, ping, team = player_str.split(", ")

                current_playerlist.append(
                    MordhauPlayer(
                        name,
                        playfab,
                        team,
                        ping,
                        PlayerType.PLAYER
                    )
                )

            for player in current_playerlist:
                if not player_is_in_list(previous_playerlist, player):
                    self.__fire_event(EventType.PLAYER_JOIN, player)
            
            for player in previous_playerlist: 
                if not player_is_in_list(current_playerlist, player):
                    self.__fire_event(EventType.PLAYER_LEAVE, player)
            
            previous_playerlist = current_playerlist
            
    
    def __fire_event(self, event_type: EventType, *args):
        for event_listener in self.event_listeners:
            if event_listener[0] == event_type:
                event_listener[1](*args)