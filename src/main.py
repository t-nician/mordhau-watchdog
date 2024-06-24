import time

from mcon import from_config

from mcon.watchdog import Watchdog, BroadcastType
from mcon.quirks.mordhau import MordhauSession, EventType, MordhauPlayer

mordhau = MordhauSession(
    watchdog=from_config("./config.jsonc")
)


@mordhau.watchdog.on_broadcast(EventType.PLAYER_CHAT)
def chat(mordhau_player: MordhauPlayer, channel, message):
    print(f"{mordhau_player.id} {mordhau_player.name} said '{message}'")


player_timestamps: dict[str, int] = {}
@mordhau.watchdog.on_broadcast(EventType.PLAYER_PRESENCE)
def presence(mordhau_player: MordhauPlayer, is_joining):
    global player_timestamps
    
    player_str = f"{mordhau_player.id} {mordhau_player.name} "
    
    if is_joining:
        player_str = player_str + "is joining!"
        player_timestamps[mordhau_player.id] = time.time()
    else:
        
        playtime = 0
        timestamp = player_timestamps.get(mordhau_player.id)
        
        if timestamp is not None:
            playtime = time.time() - timestamp
            del player_timestamps[mordhau_player.id]
        else:
            playtime = 0
        
        player_str = player_str + f"is leaving! Session {int(playtime)} seconds..."
    
    print(player_str)


mordhau.listen(
    EventType.PLAYER_CHAT,
    EventType.PLAYER_PRESENCE
)