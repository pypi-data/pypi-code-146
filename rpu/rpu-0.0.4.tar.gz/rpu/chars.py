"""
.. include:: ../extras/chars.md
"""

import random

__all__ = (
    "INVISIBLE_CHARACTERS",
    "INVISIBLE_CHARACTER",
    "ARROW_LEFT",
    "ARROW_RIGHT",
    "ARROW_UP",
    "ARROW_DOWN",
    "BULLET_POINT",
)

ZERO_WIDTH_CHARACTERS = ["\uFEFF", "\u200d", "\u2060", "\u200b", "\u200c"]
INVISIBLE_CHARACTERS = ZERO_WIDTH_CHARACTERS + ["\u2800"]
INVISIBLE_CHARACTER = random.choice(INVISIBLE_CHARACTERS)

ARROW_LEFT = "←"
ARROW_RIGHT = "→"
ARROW_UP = "↑"
ARROW_DOWN = "↓"

BULLET_POINT = "•"
