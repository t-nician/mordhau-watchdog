import time

from dataclasses import replace

from mcon import from_config
from mcon.watchdog import Watchdog, Command

from mcon.quirks.mordhau import MordhauSession, MordhauPlayer, EventType

watchdog: Watchdog = from_config("./config.jsonc")
mordhau: MordhauSession = MordhauSession(watchdog=watchdog)


@mordhau.chat_command(".playtime")
def playtime_command(player):
    print(player)


@mordhau.on_event(EventType.PLAYER_JOIN)
def player_joined(player: MordhauPlayer):
    print(player.id, player.name, "has joined!")


@mordhau.on_event(EventType.PLAYER_LEAVE)
def player_leave(player: MordhauPlayer):
    print(player.id, player.name, "has left!")
    

mordhau.start()