from dataclasses import dataclass, field

from ..base import BaseContainer


@dataclass(frozen=True)
class Container(BaseContainer):
    class_name_str: str = field(init=False, default="Container")


@dataclass(frozen=True)
class ContainerDb(BaseContainer):
    class_name_str: str = field(init=False, default="ContainerDb")


@dataclass(frozen=True)
class ContainerQueue(BaseContainer):
    class_name_str: str = field(init=False, default="ContainerQueue")


@dataclass(frozen=True)
class ContainerExt(BaseContainer):
    class_name_str: str = field(init=False, default="Container_Ext")


@dataclass(frozen=True)
class ContainerDbExt(BaseContainer):
    class_name_str: str = field(init=False, default="ContainerDb_Ext")


@dataclass(frozen=True)
class ContainerQueueExt(BaseContainer):
    class_name_str: str = field(init=False, default="ContainerQueue_Ext")


@dataclass(frozen=True)
class ContainerBoundary(BaseContainer):
    class_name_str: str = field(init=False, default="Container_Boundary")
    techn: None = field(init=False, default=None)
