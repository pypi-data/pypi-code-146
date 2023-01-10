from dataclasses import dataclass
from i2.wrapper import Wrap
from i2 import Sig
import typing


def foo(self, y):
    return self.x + y


@dataclass
class A:
    x: int
    bar = Wrap(foo)


# want this to be equivalent to:
@dataclass
class B:
    x: int

    def bar(self, y):
        return self.x + y


@dataclass
class B2:
    x: int

    def bar(self, y):
        return self.x + y

    bar2 = bar


def post(wrapper, klass):
    return wrapper.__get__(klass, None)


"""@dataclass
class AA:
    x: int
    bar = post(Wrap(foo), AA)
"""


@dataclass
class AAA:
    x: int
    bar: typing.Callable[..., typing.Any] = foo


class C:
    def __init__(self, x):
        self.x = x
        self.bar = foo


class D:
    def __init__(self, x):
        self.x = x

    bar = foo

    def g(self):
        return 'hello world'

    h = g


if __name__ == '__main__':
    a = A(x=1)
    b = B(x=1)
    c = C(x=1)
    d = D(x=1)
    # aa = AA(x=1)
    aaa = AAA(x=1)
    aaa.bar(3)
    d.bar(3)
    print(type(a.bar))
    print(D(x=1).bar(3))
    # A.bar
    # B.bar
    # b.bar()
    # (method) bar:(y)-> Any
    a.bar(3)
    b2 = B2(x=1)
    b2.bar(3)
    b2.bar2(3)
    # (variable) bar: MethodType
    a.bar.func
    c.bar()
