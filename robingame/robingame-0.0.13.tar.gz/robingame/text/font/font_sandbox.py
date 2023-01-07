import pygame.draw
from pygame.color import Color
from pygame.surface import Surface

from robingame.objects import Game
from robingame.text.font import fonts

snippet = """
 1space
  2space
Ook    in 
de     spelling 
van    sommige andere talen wordt de umlaut gebruikt, bijvoorbeeld in verwante 
talen als het IJslands en het Zweeds, om een soortgelijk 

klankverschijnsel
weer
te;;;'''

geven, of in niet-verwante talen als het Fins, het Hongaars of het Turks, om dezelfde e-, eu- en u-klank weer te geven, die echter niet het resultaat van hetzelfde klankverschijnsel zijn.
"""


class FontTest(Game):
    window_width = 1500
    screen_color = (150, 150, 150)

    def draw(self, surface: Surface, debug: bool = False):
        super().draw(surface, debug)
        X = 500
        Y = 30
        WRAP = 500
        fonts.cellphone_white.render(
            surface,
            snippet,
            scale=2,
            wrap=WRAP,
            x=X,
            y=Y,
            align=-1,
        )
        pygame.draw.rect(surface, color=Color("red"), rect=(X, Y, WRAP, WRAP), width=1)


if __name__ == "__main__":
    FontTest().main()
