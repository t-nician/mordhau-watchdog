from dataclasses import dataclass, field

from mcon.command import Command
from mcon.quirks.playfab import PlayfabPlayer


@dataclass
class MordhauPlayer(PlayfabPlayer):
    team: str = field(default="")
    message: str = field(default="")


def is_mordhau_player_in_list(playfab: str, list: list[MordhauPlayer]) -> bool:
    for player in list:
        if player.playfab_id == playfab:
            return True
    return False


@dataclass
class ChatlogCommand(Command):
    args: list[str] = field(default_factory=lambda: list["18"])
    result: list[MordhauPlayer] = field(default_factory=list)
    
    def complete(self, data: str):
        self.result = data


@dataclass
class PlayerlistCommand(Command):
    name: str = field(default="playerlist")
    result: list[MordhauPlayer] = field(default_factory=list)
    
    def string_to_mordhau_player(player_str: str) -> MordhauPlayer:
        """
        player_str example: "000000000000000, t-nician, 1 ms, team 0\n"
        """
        player_str.removesuffix("\n")
        playfab, name, ping, team = player_str.split(",")
        return MordhauPlayer(
            name=name.removeprefix(" "),
            playfab_id=playfab,
            ping=ping.removeprefix(" "),
            team=team.removeprefix(" ")
        )
        
    
    def complete(self, data: str):
        if len(data) < 38 or data == "There are currently no players present":
            return None
        
        playerlist = []
        
        data = data.split("\n")
        data.pop()
            
        for player_str in data:
            playerlist.append(
                PlayerlistCommand.string_to_mordhau_player(
                    player_str
                )
            )

        self.result = playerlist
        
        
    def get_difference(
        self, 
        playerlist: list[MordhauPlayer]
    ) -> tuple[list[MordhauPlayer], list[MordhauPlayer]]:
        """
        returns two lists.
        
        first list are people that joined.
        second list are people that left.
        """

        joiners, leavers = [], []
        
        for player in self.result:
            if not is_mordhau_player_in_list(player.playfab_id, playerlist):
                joiners.append(player)
        
        for player in playerlist:
            if not is_mordhau_player_in_list(player.playfab_id, self.result):
                leavers.append(player)
        
        return joiners, leavers