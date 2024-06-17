import time
import copy

from rcon.source import Client

from uuid import uuid4
from dataclasses import dataclass, field, fields, asdict, replace

from mcon.command import Command

@dataclass
class CommandAssignment:
    callback: (Command) = field(default=lambda: ())
    command: Command = field(default_factory=Command)
    threshold: int = field(default=0)
    interval: int = field(default=0)


@dataclass
class Watchdog:
    host: str = field(default="")
    port: int = field(default=0)
    
    password: str = field(default="")
    commands: list[CommandAssignment] = field(default_factory=list)
    
    def command(self, command: Command, interval_seconds: int = 5):
        print(command)
        def wrapper(callback: (Command)):
            self.commands.append(
                CommandAssignment(
                    callback=callback, 
                    command=command, 
                    threshold=interval_seconds
                )
            )
        return wrapper
    
    
    def execute_rcon(self, command: str, args: list[str]) -> str:
        return "000000000000002, t-nician, 1 ms, team 0\n"
    
    
    def start(self):
        while True:
            for command_assignment in self.commands:
                if command_assignment.interval >= command_assignment.threshold:
                    command_assignment.interval = 0
                    
                    complmete_command = replace(command_assignment.command)
                    complmete_command.complete(
                        self.execute_rcon(
                            command_assignment.command.name, 
                            command_assignment.command.args
                        )
                    )
                    
                    command_assignment.callback(complmete_command)                    
                else:
                    command_assignment.interval += 1
            
            time.sleep(0.5)