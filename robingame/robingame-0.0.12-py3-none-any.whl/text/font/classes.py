from pathlib import Path

from pygame.color import Color
from pygame.surface import Surface

from robingame.image import load_spritesheet, scale_image, empty_image
from robingame.text.exceptions import TextError


class Font:
    letters: dict[str:Surface]
    image_size: tuple[int, int]
    xpad: int
    ypad: int

    def __init__(
        self,
        filename: str | Path,
        image_size: tuple[int, int],
        letters: str,
        xpad=0,
        ypad=0,
        trim=False,
        space_width=None,
        **kwargs,
    ):
        """`letters` is the letters in the spritesheet, in the same order."""
        self.image_size = width, height = image_size
        self.xpad = xpad
        self.ypad = ypad
        self.letters = dict()
        self.letters[" "] = empty_image((space_width or width, height))
        self.not_found = Surface(image_size)
        self.not_found.fill(Color("red"))
        images = load_spritesheet(filename, image_size=image_size, **kwargs)
        if trim:
            images = self.trim_images(images)
        self.letters.update({letter: image for letter, image in zip(letters, images)})

    def render(
        self,
        surf: Surface,
        text: str,
        x: int = 0,
        y: int = 0,
        scale: int = 1,
        wrap: int = 0,
        align: int = None,
    ) -> int:
        """
        align: -1=left, 0=center, 1=right
        wrap: x width at which to wrap text
        """
        _, ysize = self.image_size
        cursor = x
        for line in text.splitlines():
            wrapped_lines = self.wrap_words(line, wrap, x, scale) if wrap else [line]
            for line in wrapped_lines:
                cursor = self.align_cursor(line, x, align, scale, wrap)
                for letter in line:
                    image = self.get(letter)
                    image = scale_image(image, scale)
                    surf.blit(image, (cursor, y))
                    w = image.get_width()
                    cursor += w + self.xpad * scale
                y += (ysize + self.ypad) * scale
        return cursor

    def align_cursor(self, line: str, x: int, align: int, scale: int, wrap: int) -> int:
        """Used for left/right/centered text alignmnent"""
        match align:
            case -1 | None:
                cursor = x
            case 0:
                if not wrap:
                    raise TextError("Can't center text without specifying a wrap width.")
                line_width = self.printed_width(line, scale)
                slack = wrap - line_width
                cursor = x + slack // 2
            case 1:
                line_width = self.printed_width(line, scale)
                cursor = x + wrap - line_width
            case _:
                raise TextError(f"Bad alignment value: {align}")
        return cursor

    def wrap_words(self, text: str, wrap: int, x: int = 0, scale: int = 1) -> list[str]:
        """Break one long line into multiple lines based on the wrap width."""
        lines = []
        line = ""
        for word in text.split(" "):
            new_line = f"{line} {word}" if line else word
            if self.printed_width(new_line, scale) <= wrap:
                line = new_line
            else:
                lines.append(line)
                line = word
        lines.append(line)  # last line
        return lines

    def printed_width(self, text: str, scale: int) -> int:
        return sum((self.get(letter).get_width() + self.xpad) * scale for letter in text)

    def trim_images(self, images: list[Surface]) -> list[Surface]:
        """Make a monospaced font non-monospaced"""
        trimmed = []
        for image in images:
            x, _, w, _ = image.get_bounding_rect()  # trim x to bounding rect
            _, y, _, h = image.get_rect()  # maintain original y position of character
            new = image.subsurface((x, y, w, h))
            trimmed.append(new)
        return trimmed

    def get(self, letter: str) -> Surface:
        try:
            return self.letters[letter]
        except KeyError:
            return self.not_found
