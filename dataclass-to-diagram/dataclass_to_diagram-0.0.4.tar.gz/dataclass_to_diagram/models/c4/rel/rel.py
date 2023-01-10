from dataclasses import dataclass, field


from ..base import BaseRel


@dataclass(frozen=True)
class Rel(BaseRel):
    class_name_str: str = field(init=False, default="Rel")


@dataclass(frozen=True)
class RelUp(BaseRel):
    class_name_str: str = field(init=False, default="Rel_Up")


@dataclass(frozen=True)
class RelDown(BaseRel):
    class_name_str: str = field(init=False, default="Rel_Down")


@dataclass(frozen=True)
class RelLeft(BaseRel):
    class_name_str: str = field(init=False, default="Rel_Left")


@dataclass(frozen=True)
class RelRight(BaseRel):
    class_name_str: str = field(init=False, default="Rel_Right")


@dataclass(frozen=True)
class RelBack(BaseRel):
    class_name_str: str = field(init=False, default="Rel_Back")


@dataclass(frozen=True)
class RelNeighbor(BaseRel):
    class_name_str: str = field(init=False, default="Rel_Neighbor")


@dataclass(frozen=True)
class BiRel(BaseRel):
    class_name_str: str = field(init=False, default="BiRel")


@dataclass(frozen=True)
class BiRelUp(BaseRel):
    class_name_str: str = field(init=False, default="BiRel_Up")


@dataclass(frozen=True)
class BiRelDown(BaseRel):
    class_name_str: str = field(init=False, default="BiRel_Down")


@dataclass(frozen=True)
class BiRelLeft(BaseRel):
    class_name_str: str = field(init=False, default="BiRel_Left")


@dataclass(frozen=True)
class BiRelRight(BaseRel):
    class_name_str: str = field(init=False, default="BiRel_Right")
