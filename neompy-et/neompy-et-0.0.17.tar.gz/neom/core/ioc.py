# Copyright 2022 neomadas-dev
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#   1. Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#
#   2. Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#
#   3. Neither the name of the copyright holder nor the names of its
#      contributors may be used to endorse or promote products derived from
#      this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
# IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
# TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from typing import get_type_hints


def AutoWire(cls):
    def new_decoration(new_method, type_hints):
        def wrapper(cls, *args, **kwargs):
            self = new_method(cls)
            for name, key in type_hints.items():
                call = manager.pairs[key]
                setattr(self, name, call())
            self.__init__(*args, **kwargs)
            return self

        return wrapper

    type_hints = get_type_hints(cls)
    cls.__new__ = new_decoration(cls.__new__, type_hints)
    return cls


class Manager:
    def __init__(self):
        self.pairs = {}

    def wire(self, interface, concrete):
        self.pairs[interface] = concrete


manager = Manager()

# new api


def wire(f):
    def wrap(f, type_hints):
        def wrapper(*args, **kwargs):
            for name, key in type_hints.items():
                if isinstance(key, Provide):
                    kwargs[name] = manager.pairs[key.it]()
            return f(*args, **kwargs)

        return wrapper

    type_hints = get_type_hints(f)
    return wrap(f, type_hints)


def Wireable(tg):
    def new_decoration(new_method, type_hints):
        def wrapper(tg, *args, **kwargs):
            self = new_method(tg)
            for name, key in type_hints.items():
                if isinstance(key, Provide):
                    call = manager.pairs[key.it]
                    setattr(self, name, call())
            self.__init__(*args, **kwargs)
            return self

        return wrapper

    type_hints = get_type_hints(tg)
    tg.__new__ = new_decoration(tg.__new__, type_hints)
    return tg


class Provide:
    __slots__ = ("it",)

    def __init__(self, it):
        self.it = it


class Provider:

    __slots__ = ("_name", "_doc", "__weakref__")

    def __init__(self, name, doc):
        self._name = name
        self._doc = doc

    def __new__(cls, *args, **_):
        if (
            len(args) == 3
            and isinstance(args[0], str)
            and isinstance(args[1], tuple)
        ):
            raise TypeError(f"Cannot subclass {cls!r}")
        return super().__new__(cls)

    def __init_subclass__(self, /, *_, **ks):
        if "_root" not in ks:
            raise TypeError("Cannot subclass provider classes")

    def __copy__(self):
        return self

    def __deepcopy__(self, _):
        return self

    def __eq__(self, other):
        return self._name == other._name  # TODO: no impl

    def __hash__(self):
        return hash((self._name,))

    def __repr__(self):
        return "ioc." + self._name

    def __reduce__(self):
        return self._name

    def __call__(self, *_, **__):
        raise TypeError(f"Cannot instantiate {self!r}")

    def __instancecheck__(self, _):
        raise TypeError(f"{self} cannot be used with isinstance()")

    def __subclasscheck__(self, _):
        raise TypeError(f"{self} cannot be used with issubclass()")

    def __getitem__(self, provider):
        return Provide(provider)


Wired = Provider(
    "Wired",
    doc="""Declare a dependency wireable class.

  @Wireable
  class Service:
    member: Wired[Member]

  @wire
  def process(argument, another: Wired[Another]):
    return None

  @wire
  def process(argument, extra: Wired[Extra]):
    return None
  """,
)
