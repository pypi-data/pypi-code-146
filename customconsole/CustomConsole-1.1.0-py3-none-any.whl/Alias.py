from dataclasses import dataclass
from CustomConsole.Color import Colors as Color

@dataclass
class Alias:

    """
    This Class Creates Aliases ( Badges ) for console object or for general purpose
    """

    # Nessesary things
    text        : str
    foreground  : Color
    background  : Color
    # Advanced
    size        : int = 15
    adjust      : str = "Auto"
    l_wrap      : str = "["
    r_wrap      : str = "]"

    @property
    def colored(self):
        text_spaces = self.size - ( 2 + len( self.l_wrap ) + len( self.r_wrap ))
        if len(self.text) > text_spaces:
            self.text = self.text[:(text_spaces + 1)].title()
        __colored = Color.Colored.console(f"{self.l_wrap} { self.text.center( text_spaces ) } {self.r_wrap}", self.foreground, self.background)
        return __colored

    @property
    def uncolored(self):
        text_spaces = self.size - ( 2 + len( self.l_wrap ) + len( self.r_wrap ))
        if len(self.text) > text_spaces:
            self.text = self.text[:(text_spaces + 1)].title()
        __un_colored = f"{self.l_wrap} { self.text.center( text_spaces ) } {self.r_wrap}"
        return __un_colored

    def __str__(self) -> str:
        return self.colored
