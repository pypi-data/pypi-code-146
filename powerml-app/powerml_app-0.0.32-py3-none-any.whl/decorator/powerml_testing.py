import functools


def powerml_unit_test_suite(func):
    @functools.wraps(func)
    def wrapper():
        metric_result, num_tests = func()
        return (metric_result, num_tests)
    return wrapper


def powerml_unit_test(func):
    @functools.wraps(func)
    def wrapper():
        test_result = func()
        return test_result
    return wrapper


def powerml_metric(func):
    @functools.wraps(func)
    def wrapper():
        metric_result = func()
        # Expect information about the metric to be non-boolean.
        return metric_result
    return wrapper
