"""Testing assertion helpers."""
import re
from collections.abc import Callable
from functools import singledispatch

__all__ = ["assert_like"]


@singledispatch
def assert_like(  # pylint: disable=unused-argument
    expected, got, allow_extra=True, loc=""
) -> None:
    """Check whether an object is like the expected.

    Supported values:
    * dict: see 'assert_like_dict'
    * list: see 'assert_like_list'
    * regex pattern: see 'assert_like_pattern'
    * callable: see 'assert_like_function'
    * everything else: simply compared using '=='
    """
    __tracebackhide__ = True  # pylint: disable=unused-variable
    assert expected == got, f"{loc}: {got!r} != {expected!r}"


@assert_like.register
def assert_like_dict(expected: dict, got, allow_extra=True, loc="") -> None:
    """Check whether a dictionary is like the expected.

    'allow_extra': enable extra keys in the dictionary or not
    """
    __tracebackhide__ = True  # pylint: disable=unused-variable
    assert isinstance(got, dict), f"{loc} {got.__class__.__name__} != dict"
    expected_keys = set(expected)
    got_keys = set(got)
    missing_keys = expected_keys - got_keys
    assert not missing_keys, f"{loc}: missing_keys={missing_keys}"
    if not allow_extra:
        extra_keys = got_keys - expected_keys
        assert not extra_keys, f"{loc}: extra_keys={extra_keys}"
    for key, value in sorted(expected.items()):
        assert_like(value, got[key], allow_extra=allow_extra, loc=f"{loc}.{key}")


@assert_like.register
def assert_like_list(expected: list, got, loc="", **kwargs) -> None:
    """Check whether a list is like the expected.

    Ellipsis can be used for partial matching ([..., 2] == [1, 2]).
    """
    __tracebackhide__ = True  # pylint: disable=unused-variable
    assert isinstance(got, list), f"{loc} {got.__class__.__name__} != list"
    got_iter = iter(got)
    ellipsis = False
    for index, value in enumerate(expected):
        loc_ = f"{loc}[{index}]"
        if value is Ellipsis:
            ellipsis = True
            continue
        for got_ in got_iter:
            try:
                assert_like(value, got_, loc=loc_, **kwargs)
            except AssertionError:
                if not ellipsis:
                    raise
            else:
                ellipsis = False
                break
        else:
            raise AssertionError(f"{loc_}: unexpected end of list")
    if not ellipsis:
        extra = list(got_iter)
        assert not extra, f"{loc}: unexpected items: extra_items={extra}"


@assert_like.register
def assert_like_pattern(expected: re.Pattern, got, loc="", **_) -> None:
    """Check whether a string matches the given pattern."""
    __tracebackhide__ = True  # pylint: disable=unused-variable
    assert expected.search(got), f"{loc}: {got} !~ {expected.pattern}"


@assert_like.register
def assert_like_function(expected: Callable, got, loc="", **_) -> None:
    """Check whether an object is the expected using the callback function."""
    __tracebackhide__ = True  # pylint: disable=unused-variable
    try:
        assert expected(got)
    except Exception as exc:
        ctx = None if isinstance(exc, AssertionError) else exc
        raise AssertionError(f"{loc}: {got} validation failed ({exc})") from ctx
