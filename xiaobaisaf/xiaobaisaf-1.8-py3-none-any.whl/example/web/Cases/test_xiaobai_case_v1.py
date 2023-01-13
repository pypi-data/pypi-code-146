#! /usr/bin/env python
'''
@Author: xiaobaiTser
@Time  : 2022/8/21 0:25
@File  : test_xiaobai_shop_v1.py
'''
import pytest

def test_xiaobai_coupon():
    assert 1 == 1

def test_xiaobai_collection():
    assert 1 == 2


if __name__ == '__main__':
    pytest.main(['-s', '-v', 'test_xiaobai_case_v1.py'])