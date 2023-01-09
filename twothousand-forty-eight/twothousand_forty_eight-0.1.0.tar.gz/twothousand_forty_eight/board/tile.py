from typing import Optional


class Tile:
    x: int
    y: int
    value: int
    id: int
    merged_from: Optional[tuple[int, int]]

    def __init__(self, x: int, y: int, value: int, id: Optional[int]) -> None:
        self.x = x
        self.y = y
        self.value = value
        if id:
            self.id = id
        else:
            self.id = get_new_id()
        self.merged_from = None


_counter = 0


def get_new_id() -> int:
    global _counter
    id = _counter
    _counter += 1
    return id
