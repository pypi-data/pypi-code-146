from typing import Union, Sequence, Tuple
from pathlib import Path
from solid2.core.object_base import OpenSCADObject

PathStr = Union[Path, str]

P2 = Tuple[float, float]
P3 = Tuple[float, float, float]
P4 = Tuple[float, float, float, float]
Vec3 = P3
Vec4 = P4
Vec34 = Union[Vec3, Vec4]
P3s = Sequence[P3]
P23 = Union[P2, P3]
Points = Sequence[P23]
Indexes = Union[Sequence[int], Sequence[Sequence[int]]]
ScadSize = Union[int, Sequence[float]]
OpenSCADObjectPlus = Union[OpenSCADObject, Sequence[OpenSCADObject]]

