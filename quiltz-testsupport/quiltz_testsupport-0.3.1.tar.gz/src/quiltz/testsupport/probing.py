from time import sleep
from typing import Callable
from hamcrest import assert_that
from hamcrest.core.matcher import Matcher


def probe_that(assertion_or_delayed_result_function: Callable, matcher: Matcher = None, timeout: int = 1000):
    """probes the delayed_result_function until it matches the hamcrest matcher given.
    if it matches the matcher within the timeout the probe passes. It if does not it fails 
    with an AssertionError, just like assert_that would.

    probe_that can be called in two ways: 
    1: with a delayed result function (callable) and a matcher
    example:
        probe_that(lambda: result, equal_to(5))

    2: with a delayed assertion
    examples:
        probe_that(lambda: assert result == 5)
        probe_that(lambda: assert_that(result, equal_to(5)))

    :param assertion_or_delayed_result_function:  a callable executing the assertion or returning actual result
    :param matcher:   matcher to be used in mode 1
    :param timeout:   timeout (default one second)
    """
    assertion = assertion_or_delayed_result_function
    if matcher is not None:
        if not isinstance(matcher, Matcher):
            raise (ValueError("matcher is not a matcher"))
        assertion = lambda: assert_that(assertion_or_delayed_result_function(), matcher)
    t = 0
    success = False
    while not success:
        try:
            assertion()
            success = True
        except AssertionError as e:
            sleep(50.0 / 1000.0)
            t += 50
            if t >= timeout:
                raise e
