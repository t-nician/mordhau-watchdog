import time

from mcon.command import Command
from mcon.watchdog import Watchdog

from mcon.quirks.mordhau import MordhauPlayer, PlayerlistCommand, ChatlogCommand


watchdog = Watchdog()


@watchdog.command(ChatlogCommand, interval_seconds=1)
def chatlog_monitor(command: ChatlogCommand):
    print(command.result)


@watchdog.command(PlayerlistCommand, interval_seconds=5)
def playerlist_monitor(command: PlayerlistCommand):
    print(command.result)
    

@watchdog.command(Command("stats"), interval_seconds=10)
def stats_monitor(command: Command):
    print(command.result)
    
    
watchdog.start()