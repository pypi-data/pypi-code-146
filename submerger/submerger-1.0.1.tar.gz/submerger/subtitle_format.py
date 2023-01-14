from enum import Enum


class SubtitleFormat:
    class Position(Enum):
        BOTTOM_LEFT = '1'
        BOTTOM_CENTER = '2'
        BOTTOM_RIGHT = '3'
        MIDDLE_LEFT = '4'
        MIDDLE_CENTER = '5'
        MIDDLE_RIGHT = '6'
        TOP_LEFT = '7'
        TOP_CENTER = '8'
        TOP_RIGHT = '9'

    def __init__(self) -> None:
        self.position: SubtitleFormat.Position | None = None
        self.color: str | None = None
        self.italic: bool = False

    def set_position(self, position: Position) -> 'SubtitleFormat':
        self.position = position
        return self

    def set_color(self, color: str) -> 'SubtitleFormat':
        self.color = color
        return self

    def set_italic(self) -> 'SubtitleFormat':
        self.italic = True
        return self

    def format(self, text: str) -> str:
        if self.position is not None:
            text = rf'{{\an{self.position.value}}}{text}'

        if self.italic:
            text = f'<i>{text}</i>'

        if self.color is not None:
            text = f'<font color={self.color}>{text}</font>'

        return text
