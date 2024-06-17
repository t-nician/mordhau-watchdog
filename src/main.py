import time

from dataclasses import replace

from mcon.command import Command
from mcon.watchdog import Watchdog

from mcon.quirks.mordhau import MordhauPlayer, PlayerlistCommand, ChatlogCommand


watchdog = Watchdog()


__last_player_list: list[MordhauPlayer] = []
@watchdog.command(PlayerlistCommand(), interval_seconds=5)
def playerlist_monitor(command: PlayerlistCommand):
    global __last_player_list
    
    joiners, leavers = command.get_difference(
        __last_player_list
    )
    
    for player in joiners:
        print(player.playfab_id, player.name, "has joined!")
        
    for player in leavers:
        print(player.playfab_id, player.name, "has left!")
    
    __last_player_list = command.result
    
    
watchdog.start()