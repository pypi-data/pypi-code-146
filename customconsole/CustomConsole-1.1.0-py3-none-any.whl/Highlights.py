from CustomConsole.Color import Colors as Color, Colored
from CustomConsole.Alias import Alias
from dataclasses import dataclass

@dataclass
class Highlights:

    foreground:Color

    @staticmethod
    def match_alias( alias:Alias ):
        if isinstance( alias, Alias):
            return Highlights( alias.foreground )
    
    def __call__(self, text):
        return Colored.text( text, color = self.foreground )

