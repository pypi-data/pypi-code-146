#! /usr/bin/env python
'''
@Author: xiaobaiTser
@Time  : 2022/9/2 1:12
@File  : test_case.py
'''

import pytest

@pytest.mark.parametrize('a', [1])
@pytest.mark.parametrize('b', [1])
def test_a(a, b):
    print(a, b)