from mcon import from_config

from mcon.watchdog import Watchdog, BroadcastType
from mcon.quirks.mordhau import MordhauSession, EventType, MordhauPlayer

mordhau = MordhauSession(
    watchdog=from_config("./config.jsonc")
)


@mordhau.watchdog.on_broadcast(EventType.PLAYER_CHAT)
def chat(mordhau_player: MordhauPlayer, channel, message):
    print(f"{mordhau_player.id} {mordhau_player.name} said '{message}'")


@mordhau.watchdog.on_broadcast(EventType.PLAYER_PRESENCE)
def presence(mordhau_player: MordhauPlayer, is_joining):
    player_str = f"{mordhau_player.id} {mordhau_player.name} "
    
    if is_joining:
        player_str = player_str + "is joining!"
    else:
        player_str = player_str + "is leaving!"
    
    print(player_str)


mordhau.listen(
    EventType.PLAYER_CHAT,
    EventType.PLAYER_PRESENCE
)