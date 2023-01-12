# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116


"test persistence"


import unittest


from opr.objects import Object


class TestPersist(unittest.TestCase):


    def test_methodoverwrite(self):
        obj = Object()
        obj.a = "b"
        obj.get = ""
        self.assertTrue(getattr(obj, "a"), "b")
        