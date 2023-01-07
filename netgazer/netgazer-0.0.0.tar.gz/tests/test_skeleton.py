#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from netgazer.skeleton import fib

__author__ = "Tim Armstrong"
__copyright__ = "Tim Armstrong"
__license__ = "mit"


def test_fib():
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(7) == 13
    with pytest.raises(AssertionError):
        fib(-10)
