from mcon import from_config

from mcon.watchdog import Watchdog, BroadcastType
from mcon.quirks.mordhau import MordhauSession, EventType, MordhauPlayer

mordhau = MordhauSession(
    watchdog=from_config("./config.jsonc")
)


@mordhau.watchdog.on_broadcast(EventType.PLAYER_CHAT)
def chat(mordhau_player, channel, message):
    print("player", mordhau_player)
    print("channel", channel)
    print("message", message)


@mordhau.watchdog.on_broadcast(EventType.PLAYER_PRESENCE)
def presence(mordhau_player, is_joining):
    print("player", mordhau_player)
    print("is_joining", is_joining)


mordhau.listen(
    EventType.PLAYER_CHAT,
    EventType.PLAYER_PRESENCE
)