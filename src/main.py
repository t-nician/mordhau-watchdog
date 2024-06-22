from mcon import from_config

from mcon.watchdog import Watchdog, BroadcastType


watchdog: Watchdog = from_config("./config.jsonc")


@watchdog.broadcast_transformer
def transformer(packet):
    return BroadcastType.UNKNOWN, "Hello there!"


@watchdog.on_broadcast(BroadcastType.UNKNOWN)
def on_chat(data):
    print("on_chat", data)


watchdog.start()