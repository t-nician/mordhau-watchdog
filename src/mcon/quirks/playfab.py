from dataclasses import dataclass, field


@dataclass
class PlayfabPlayer:
    name: str = field(default="")
    id: str = field(default="")
    
    def __eq__(self, other) -> bool:
        assert type(other) == PlayfabPlayer, f"expected a PlayfabPlayer! Got {other}"
        return self.id == other.id