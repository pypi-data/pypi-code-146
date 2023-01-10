from dataclasses import dataclass, field

from ..base import BaseComponent


@dataclass(frozen=True)
class Component(BaseComponent):
    class_name_str: str = field(init=False, default="Component")


@dataclass(frozen=True)
class ComponentDb(BaseComponent):
    class_name_str: str = field(init=False, default="ComponentDb")


@dataclass(frozen=True)
class ComponentQueue(BaseComponent):
    class_name_str: str = field(init=False, default="ComponentQueue")


@dataclass(frozen=True)
class ComponentExt(BaseComponent):
    class_name_str: str = field(init=False, default="Component_Ext")


@dataclass(frozen=True)
class ComponentDbExt(BaseComponent):
    class_name_str: str = field(init=False, default="ComponentDb_Ext")


@dataclass(frozen=True)
class ComponentQueueExt(BaseComponent):
    class_name_str: str = field(init=False, default="ComponentQueue_Ext")
