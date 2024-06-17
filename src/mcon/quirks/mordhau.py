from dataclasses import dataclass, field

from mcon.command import Command
from mcon.quirks.playfab import PlayfabPlayer


@dataclass
class MordhauPlayer(PlayfabPlayer):
    team: str = field(default="")


@dataclass
class PlayerlistCommand(Command):
    name: str = field(default="playerlist")
    result: list[MordhauPlayer] = field(default_factory=list)
    
    def __player_str_to_mordhau_player(player_str: str) -> MordhauPlayer:
        player_str.removesuffix("\n")
        playfab, name, ping, team = player_str.split(",")
        return MordhauPlayer(
            name=name.removeprefix(" "),
            playfab_id=playfab,
            ping=ping.removeprefix(" "),
            team=team.removeprefix(" ")
        )
        
    
    def complete(self, data: str):
        playerlist = []
        
        if data == "There are currently no players present":
            return None
        
        if data.count("\n") > 1:
            split_data = data.split("\n")
            split_data.pop()
            
            for player_str in split_data:
                playerlist.append(
                    PlayerlistCommand.__player_str_to_mordhau_player(
                        player_str
                    )
                )
        else:
            playerlist.append(
                PlayerlistCommand.__player_str_to_mordhau_player(
                    data
                )
            )
        
        self.result = playerlist