#
#  Copyright (c) 2022 Russell Smiley
#
#  This file is part of click_logging_config.
#
#  You should have received a copy of the MIT License along with build_harness.
#  If not, see <https://opensource.org/licenses/MIT>.
#

import functools
import typing

DecoratorCallable = typing.TypeVar(
    "DecoratorCallable", bound=typing.Callable[..., typing.Any]
)


def f1(f: DecoratorCallable) -> DecoratorCallable:
    print("this is f1 decorator")

    def decorator(p1: str):
        print("this is f1 decorated")
        v = f(p1)

        return f"{v}, f1 decorated"

    return decorator


@f1
def func1(p1: str) -> str:
    v = f"this is func1, {p1}"
    return v


def test_1():
    r = func1("first")

    assert r == "this is func1, first, f1 decorated"


def f2(p2: str) -> DecoratorCallable:
    print(f"this is f2 decorator, {p2}")

    def decorator(f: DecoratorCallable) -> DecoratorCallable:
        print("this is f2 decorated")

        def wrapper(p1: str) -> str:
            print("this is f2 wrapped")
            v = f(p1)

            return f"{v}, f2 decorated, {p2}"

        return wrapper

    return decorator


@f2("f2 arg")
def func2(p1: str) -> str:
    v = f"this is func2, {p1}"
    return v


def test_2():
    r = func2("second")

    assert r == "this is func2, second, f2 decorated, f2 arg"


def f3(p2: str) -> DecoratorCallable:
    print(f"this is f3 decorator, {p2}")

    def decorator(f: DecoratorCallable) -> DecoratorCallable:
        print("this is f3 decorated")

        def wrapper(p3: str, *args) -> str:
            print("this is f3 wrapped")
            v = f(*args)

            return f"{v}, f3 decorated, {p2}, {p3}"

        return functools.update_wrapper(wrapper, f, assigned=("p3"))

    return decorator


@f3("f3p2 arg")
def func3(p1: str) -> str:
    v = f"this is func3, {p1}"
    return v


def test_3():
    r = func3("p3 arg", "p1 arg")

    assert r == "this is func3, p1 arg, f3 decorated, f3p2 arg, p3 arg"
