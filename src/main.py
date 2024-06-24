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
        playtime = time.time() - player_timestamps[mordhau_player.id]
        
        del player_timestamps[mordhau_player.id]
        
        player_str = player_str + f"is leaving!\nPlayed for {playtime} seconds..."
    
    print(player_str)


mordhau.listen(
    EventType.PLAYER_CHAT,
    EventType.PLAYER_PRESENCE
)