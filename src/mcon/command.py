from dataclasses import dataclass, field, asdict


@dataclass
class Command:
    name: str = field(default="")
    result: any = field(default=None)
    
    args: list[str] = field(default_factory=list)
    
    def complete(self, data: str):
        self.result = data