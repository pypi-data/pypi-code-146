"""Level 1 - Context."""

from dataclasses import dataclass, field

from ..base import BaseContext


@dataclass(frozen=True)
class Person(BaseContext):
    """Level 1 - Context (Person)."""

    class_name_str: str = field(init=False, default="Person")


@dataclass(frozen=True)
class PersonExt(BaseContext):
    """Level 1 - Context (Person_Ext)."""

    class_name_str: str = field(init=False, default="Person_Ext")


@dataclass(frozen=True)
class System(BaseContext):
    """Level 1 - Context (System)."""

    class_name_str: str = field(init=False, default="System")


@dataclass(frozen=True)
class SystemDb(BaseContext):
    """Level 1 - Context (SystemDb)."""

    class_name_str: str = field(init=False, default="SystemDb")


@dataclass(frozen=True)
class SystemDbExt(BaseContext):
    """Level 1 - Context (SystemDb_Ext)."""

    class_name_str: str = field(init=False, default="SystemDb_Ext")


@dataclass(frozen=True)
class SystemExt(BaseContext):
    """Level 1 - Context (System_Ext)."""

    class_name_str: str = field(init=False, default="System_Ext")


@dataclass(frozen=True)
class SystemQueueExt(BaseContext):
    """Level 1 - Context (SystemQueue_Ext)."""

    class_name_str: str = field(init=False, default="SystemQueue_Ext")


@dataclass(frozen=True)
class SystemQueue(BaseContext):
    """Level 1 - Context (SystemQueue)."""

    class_name_str: str = field(init=False, default="SystemQueue")


@dataclass(frozen=True)
class EnterpriseBoundary(BaseContext):
    """Level 1 - Context (Enterprise_Boundary)."""

    class_name_str: str = field(init=False, default="Enterprise_Boundary")
    descr: None = field(init=False)


@dataclass(frozen=True)
class SystemBoundary(BaseContext):
    """Level 1 - Context (System_Boundary)."""

    class_name_str: str = field(init=False, default="System_Boundary")
    descr: None = field(init=False)
