import time

import database

from mcon import from_config

from mcon.watchdog import Watchdog, BroadcastType
from mcon.quirks.mordhau import MordhauSession, EventType, MordhauPlayer

from datetime import datetime, timedelta

mordhau = MordhauSession(
    watchdog=from_config("./config.jsonc")
)

mongo = database.from_config("./config.jsonc")


def format_time(seconds) -> tuple[int, int, int, int]:
    result =  (datetime(1, 1, 1) + timedelta(seconds=seconds))
    return result.day - 1, result.hour, result.minute, result.second


player_timestamps: dict[str, int] = {}

@mordhau.watchdog.on_broadcast(EventType.PLAYER_CHAT)
def chat(mordhau_player: MordhauPlayer, channel, message):
    if message.startswith(".playtime"):
        global player_timestamps
        
        playtime_model = mongo.get_playtime_data(mordhau_player.id) or mongo.create_playtime_data(mordhau_player.id)
        
        timestamp = player_timestamps.get(mordhau_player.id)
        session_seconds = timestamp and time.time() - timestamp or 0

        total_time = "Total: %dd %dh %dm %ds" % format_time(
            playtime_model.total_playtime + session_seconds
        )
        
        mordhau.watchdog.run(
            "say", 
            f"[{mordhau_player.id} - {mordhau_player.name}]\nTotal Playtime: "
            + total_time
        )


@mordhau.watchdog.on_broadcast(EventType.PLAYER_PRESENCE)
def presence(mordhau_player: MordhauPlayer, is_joining):
    global player_timestamps
    
    player_str = f"{mordhau_player.id} {mordhau_player.name} "
    
    timestamp = player_timestamps.get(mordhau_player.id)
    playtime = int(timestamp and time.time() - timestamp or 0)
    
    if is_joining:
        player_str = player_str + "is joining!"
        player_timestamps[mordhau_player.id] = time.time()
    else:
        if timestamp:
            del player_timestamps[mordhau_player.id]
        
        player_str = player_str + f"is leaving! Session {int(playtime)} seconds..."
    
    print(player_str)
    
    playtime_model = mongo.get_playtime_data(
        mordhau_player.id
    ) or mongo.create_playtime_data(mordhau_player.id)
    
    playtime_model.total_playtime += playtime
    
    playtime_model.one_week += playtime
    playtime_model.two_weeks += playtime
    
    playtime_model.one_month += playtime
    
    mongo.save_playtime_player(playtime_model)


mordhau.listen(
    EventType.PLAYER_CHAT,
    EventType.PLAYER_PRESENCE
)