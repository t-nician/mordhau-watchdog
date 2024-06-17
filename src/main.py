import time

from dataclasses import replace

from mcon.command import Command
from mcon.watchdog import Watchdog

from mcon.quirks.mordhau import MordhauPlayer, PlayerlistCommand, ChatlogCommand


watchdog = Watchdog()

#@watchdog.command(ChatlogCommand(), interval_seconds=1)
#def chatlog_monitor(command: ChatlogCommand):
#    print("chatlog", command.result)


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
    

#@watchdog.command(Command("stats"), interval_seconds=10)
#def stats_monitor(command: Command):
#    print("stats", command.result)
    
    
watchdog.start()