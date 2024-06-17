import mcon
import time

watchdog = mcon.from_config("./config.jsonc")


playerlist_stamps: [str, int] = {}

def __log_time(playfab, join_time, leave_time):
    print(playfab, "played for", leave_time - join_time, "seconds")

@watchdog.command("playerlist")
def _(rcon_string: str):
    global playerlist_stamps
    
    if rcon_string == "There are currently no players present":
        for playfab, join_time in playerlist_stamps.items():
            __log_time(playfab, join_time, time.time())
            print(playfab, "left the server!")
        
        playerlist_stamps = {}
            
        return None

    
    playerlist = [] 
    
    if rcon_string.count("\n") > 1:
        playerlist = rcon_string.split("\n")
        playerlist.pop()
    else:
        playerlist.append(rcon_string)
        
    player_playfab_list = []
    
    for player_str in playerlist:
        playfab, name, ping, team = player_str.split(",")
        
        player_playfab_list.append(playfab)
        
        if not playerlist_stamps.get(playfab):
            print(playfab, name, "joined the server!")
            playerlist_stamps[playfab] = time.time()   
    
    leavers = []
    
    for playfab, join_stamp in playerlist_stamps.items():
        if player_playfab_list.count(playfab) == 0:
            leavers.append(playfab)
            __log_time(playfab, join_stamp, time.time())
            print(playfab, "left the server!")
    
    for playfab in leavers:
        del playerlist_stamps[playfab]
    


watchdog.start()