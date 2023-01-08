"""
Unit tests for `dh.log`.
"""

import unittest

import dh.log


class MyTestException(Exception):
    pass


class MyTestWarning(UserWarning):
    pass


class Test(unittest.TestCase):
    def setUp(self):
        self.logger = dh.log.Logger()

    def test_raises_none_implicit(self):
        self.logger.info(text="Test")

    def test_raises_none_explicit(self):
        self.logger.info(text="Test", exception=None)

    def test_raises_exception_instance(self):
        self.assertRaises(MyTestException, lambda: self.logger.info(text="Test", exception=MyTestException("Test")))

    def test_raises_exception_class(self):
        self.assertRaises(MyTestException, lambda: self.logger.info(text="Test", exception=MyTestException))

    def test_raises_warning_instance(self):
        self.assertWarns(MyTestWarning, lambda: self.logger.info(text="Test", exception=MyTestWarning("Test")))

    def test_raises_warning_class(self):
        self.assertWarns(MyTestWarning, lambda: self.logger.info(text="Test", exception=MyTestWarning))
