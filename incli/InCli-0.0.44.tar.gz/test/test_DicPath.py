import unittest
from InCli.SFAPI import DicPath

class Test_DicPatj(unittest.TestCase):
    def test_simple(self):
        obj = {
            "a":1,
            "b":2,
            "c":3
        }
        res = DicPath.find(obj,"c")
        self.assertTrue(res==obj['c'])

        res = DicPath.find(obj,"c")

        print()


    def test_simple2(self):
        obj = {
            "a":1,
            "b":2,
            "c":{
                "a":1,
                "b":2,
                "c":3
            }
        }
        res = DicPath.find(obj,"c.c")
        self.assertTrue(res==obj['c']['c'])

        print()

        

