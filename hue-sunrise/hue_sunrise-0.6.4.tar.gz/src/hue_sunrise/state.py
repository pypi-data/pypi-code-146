from __future__ import annotations

from dataclasses import dataclass

from .colors import XY


@dataclass
class State:
    xy: XY | None = None  # color
    bri: int | None = None  # brightness
    sat: int | None = None  # saturation
    ct: int | None = None  # color temperature
    on: bool | None = None
