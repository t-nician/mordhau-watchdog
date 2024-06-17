from dataclasses import dataclass, field


@dataclass
class PlayfabPlayer:
    name: str
    playfab_id: str
    
    ping: str = field(default="")