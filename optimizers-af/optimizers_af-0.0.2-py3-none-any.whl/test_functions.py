import numpy as np


def test_func_1(point):
    return np.absolute(point - np.arange(point.size)).sum()


def de_jong_1(point):
    return (point ** 2).sum()


def rastrigin(point):
    factor = 10
    return (
            (point ** 2 - factor * np.cos(2 * np.pi * point)).sum()
            + factor * point.size
    )
