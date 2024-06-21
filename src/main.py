import time

from dataclasses import replace

from mcon import from_config

from mcon.command import Command
from mcon.watchdog import Watchdog

from mcon.quirks.mordhau import MordhauPlayer, PlayerlistCommand, ChatlogCommand, ChatCommandHandler


watchdog: Watchdog = from_config("./config.jsonc")


__last_player_list: list[MordhauPlayer] = []
__timestamp_list: dict[str, float] = {}

@watchdog.command(PlayerlistCommand(), interval_seconds=1)
def playerlist_monitor(command: PlayerlistCommand):
    global __last_player_list, __timestamp_list
    
    joiners, leavers = command.get_difference(
        __last_player_list
    )
    
    for player in joiners:
        __timestamp_list[player.playfab_id] = time.time()
        print(player.playfab_id, player.name, "has joined!")
        
    for player in leavers:
        session_time = time.time() - __timestamp_list[player.playfab_id]
        
        del __timestamp_list[player.playfab_id]
        
        print(
            player.playfab_id, player.name, f"has left!\nSession Playtime: {session_time}"
        )
    
    __last_player_list = command.result


"""__last_player_playtime: MordhauPlayer = None
@watchdog.command(ChatlogCommand(args=["5"]), interval_seconds=1)
def chatlog_monitor(command: ChatlogCommand):
    global __last_player_playtime, __timestamp_list
    for chatlog in command.result:
        if chatlog.message == ".playtime":
            if __last_player_playtime is None or __last_player_playtime.playfab_id != chatlog.player.playfab_id:
                if __timestamp_list.get(chatlog.player.playfab_id) is None:
                    __timestamp_list[chatlog.player.playfab_id] = time.time()
                    
                session_time = time.time() - __timestamp_list.get(chatlog.player.playfab_id)
                
                watchdog.client.run("say", f"{chatlog.player.name} {chatlog.player.playfab_id} session time: {session_time}")
                
                __last_player_playtime = chatlog.player"""



# INGAME CHAT COMMANDS
chatcommand_handler = ChatCommandHandler()

@chatcommand_handler.command("playtime")
def chatcommand_playtime(player: MordhauPlayer):
    pass


@watchdog.command(ChatlogCommand(), interval_seconds=2)
def chatcommand_monitor(command: ChatlogCommand):
    global chatcommand_handler
    
    chatcommand_handler.process(command.result)
    print(len(chatcommand_handler.history))
    

watchdog.start()