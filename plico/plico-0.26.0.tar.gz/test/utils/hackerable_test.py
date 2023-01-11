#!/usr/bin/env python
import unittest
from plico.utils.hackerable import Hackerable
from plico.utils.logger import Logger

__version__ = "$Id: hackerable_test.py 26 2018-01-26 19:06:25Z lbusoni $"


class MyHackerable(Hackerable):

    class GenericObject(object):

        def __init__(self):
            self._value= 0

        def setValue(self, value):
            self._value= value

        def getValue(self):
            return self._value


    def __init__(self):
        self._aMember= self.GenericObject()
        self._logger= Logger.of('MyLogger')
        Hackerable.__init__(self, self._logger)


class HackerableTest(unittest.TestCase):


    def setUp(self):
        self.hack= MyHackerable()


    def testEvalExecute(self):
        self.hack.execute("self._aMember.setValue(42.0)")
        self.assertEqual("42.0",
                         self.hack.eval("self._aMember.getValue()"))



if __name__ == "__main__":
    unittest.main()
