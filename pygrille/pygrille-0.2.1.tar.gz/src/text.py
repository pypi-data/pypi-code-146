import pygame
import os.path


class Text:
    def __init__(self, font: str = None, size: int = None, text: str = None, pos: tuple = None, colour: tuple = None):
        if font is None:
            font = "Arial"
        if size is None:
            size = 30
        if text is None:
            text = ""
        if pos is None:
            pos = (0,0)
        if colour is None:
            colour = (0,0,0)
        self.fontstr = font
        self.font = None
        self.size = size
        self.text = text
        self.pos = pos
        self.colour = colour
        self.render = None
        self.makefont()
        self.rendertext()

    def makefont(self):
        if os.path.exists(self.fontstr):
            self.font = pygame.font.Font(self.font, self.size)
        else:
            self.font = pygame.font.SysFont(self.fontstr, self.size)

    def rendertext(self):
        self.render = self.font.render(self.text, False, self.colour)

    def draw(self, screen: pygame.Surface):
        screen.blit(self.render, (self.pos[0], self.pos[1]))

    def get_text(self):
        return self.text

    def set_text(self, text: str):
        self.text = text
        self.rendertext()

    def change_font(self, font: str):
        self.font = font
        self.makefont()
        self.rendertext()

    def change_size(self, size: int):
        self.size = size
        self.makefont()
        self.rendertext()

    def move(self, newpos: tuple):
        self.pos = newpos

    def change_colour(self, colour: tuple):
        self.colour = colour
