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
    client: None | Client = field(default=None)
    
    def command(self, command: Command, interval_seconds: int = 5):
        def wrapper(callback: (Command)):
            self.commands.append(
                CommandAssignment(
                    callback=callback, 
                    command=command, 
                    threshold=interval_seconds
                )
            )
        return wrapper
    
    
    def start(self):
        with Client(self.host, self.port, passwd=self.password) as client:
            self.client = client
            
            print(self.client.run("listen", "chat"))
            print(self.client.read())
            
            while True:
                for command_assignment in self.commands:
                    if command_assignment.interval >= command_assignment.threshold:
                        command_assignment.interval = 0
                        
                        executed_command = replace(command_assignment.command)
                        executed_command.complete(
                            client.run(
                                command_assignment.command.name, 
                                *command_assignment.command.args
                            )
                        )
                        
                        command_assignment.callback(executed_command)                    
                    else:
                        command_assignment.interval += 1
                
                time.sleep(0.5)