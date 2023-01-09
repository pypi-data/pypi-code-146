from enum import Enum


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    END = 4
    START = 5
    BREAK = 6

    def get_x(self) -> int:
        match self:
            case self.UP:
                return 0
            case self.RIGHT:
                return 1
            case self.DOWN:
                return 0
            case self.LEFT:
                return -1
        return 0

    def get_y(self) -> int:
        match self:
            case self.UP:
                return -1
            case self.RIGHT:
                return 0
            case self.DOWN:
                return 1
            case self.LEFT:
                return 0
        return 0
