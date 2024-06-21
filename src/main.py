import time

from dataclasses import replace

from mcon import from_config
from mcon.watchdog import Watchdog, Command

from mcon.quirks.mordhau import MordhauSession, MordhauPlayer

watchdog: Watchdog = from_config("./config.jsonc")
mordhau: MordhauSession = MordhauSession(watchdog=watchdog)


@mordhau.chat_command(".playtime")
def playtime_command(player):
    print(player)


mordhau.start()