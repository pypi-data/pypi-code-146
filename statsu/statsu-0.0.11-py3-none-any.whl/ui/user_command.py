from collections import deque
from typing import Deque


class UserCommand:
    def __init__(self, desc: str) -> None:
        self.description = desc
        
    def execute(self) -> None:
        pass

    def undo(self) -> None:
        pass
    
class UserCommandManager:
    def __init__(self) -> None:
        self.executed_commands: Deque[UserCommand] = deque(maxlen=5)
        self.undone_commands: Deque[UserCommand] = deque(maxlen=5)
    
    def execute_command(self, command: UserCommand) -> None:
        command.execute()
        self.executed_commands.append(command)
        self.undone_commands.clear()

    def undo_command(self) -> None:
        if len(self.executed_commands) > 0:
            target = self.executed_commands.pop()
            target.undo()
            self.undone_commands.append(target)
    
    def redo_command(self) -> None:
        if len(self.undone_commands) > 0:
            target = self.undone_commands.pop()
            target.execute()
            self.executed_commands.append(target)