# This file is placed in the Public Domain.
# pylint: disable=C0113,C0114,C0115,C0116


"scan tests"


import inspect
import unittest


from opr.handler import Command
from operbot import irc


def scan(mod):
    for key, cmd in inspect.getmembers(mod, inspect.isfunction):
        if key.startswith("cb"):
            continue
        names = cmd.__code__.co_varnames
        if "event" in names:
            Command.add(cmd)


class TestScan(unittest.TestCase):

    def test_scan(self):
        scan(irc)
        self.assertTrue("icfg" in Command.cmd)
