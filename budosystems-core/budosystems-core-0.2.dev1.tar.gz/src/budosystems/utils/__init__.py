#
#  Copyright (c) 2021.  Budo Systems
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
#

"""General utility classes and functions."""

from __future__ import annotations

from typing import Any, Type, TypeVar
from .. import typehints as th

# S = TypeVar("S", bound="Singleton")
M = TypeVar("M", bound="SingletonMeta")
T = TypeVar("T")
# Intent: Type[T] == M  (Can't find a way to express this relationship in typing code.)

class SingletonMeta(type):
    """
    Metaclass for single value classes.

    :param name: Name of the new singleton class.
    :param bases: Base classes from which the new class will inherit.
    :param namespace: Namespace that will form the structure of the new class.
    :param kwargs: These parameters will be passed to the constructors of the bases to instantiate
        the singleton value.
    """
    def __new__(mcs: Type[M], cls_name: str, bases: th.Bases, namespace: th.DictStrAny,
                **_kwargs: Any) -> M:
        new_namespace = namespace.copy()

        if '__repr__' not in new_namespace:
            new_namespace['__repr__'] = lambda self: f"<singleton {type(self).__name__}>"

        new_cls: M = super().__new__(mcs, cls_name, bases, new_namespace)

        return new_cls

    def __init__(cls: Type[T], cls_name: str, bases: th.Bases, namespace: th.DictStrAny,
                 **kwargs: Any):
        super().__init__(cls_name, bases, namespace)    # type: ignore
        # ## Initialize the singleton instance
        it: T   # Intent: Type[T] == M and Type[M] == SingletonMeta

        try:
            # Pass the kwargs from the class declaration (excluding `metaclass`) to the constructor
            # of the new class.
            # Note: Calling __new__ and __init__ directly instead of cls(...) or __call__ because
            # we are overriding __call__ in this metaclass to not make these calls.
            it = cls.__new__(cls, **kwargs)
            it.__init__(**kwargs)   # type: ignore
        except TypeError:
            # Some constructors do not accept any arguments in their signatures.
            it = cls.__new__(cls)   # pylint: disable=no-value-for-parameter
            it.__init__()   # type: ignore

        cls.__it__ = it

    def __call__(cls) -> T:  # type: ignore[type-var]
        it: T = cls.__it__
        return it


# class Singleton(metaclass=SingletonMeta):
#     """Parent for single value classes."""
#
#     # def __new__(cls: Type[T]) -> T:
#     #     it: Optional[T] = cast(Optional[T], cls.__dict__.get("__it__"))
#     #     if it is not None:
#     #         return it
#     #     cls.__it__ = it = object.__new__(cls)
#     #     # assert it is not None
#     #     it._init()
#     #     return it
#     #
#     # def _init(self):
#     #     pass
#     #
#     # def __init__(self):
#     #     # Intentionally avoid calling super().__init__(), as it would be called everytime
#     #     # the constructor is called, but that's how we get the singleton instance.
#     #     pass
#     #
#     # def __repr__(self) -> str:
#     #     return f"<singleton {type(self).__name__}>"
