
"""
    FreeClimb API

    This is a manually implemented test to validate the 
    contents of https://github.com/FreeClimbAPI/Python-Getting-Started-Tutorial/blob/master/python-getting-started.py
    are functioning as expected
"""

import unittest

import freeclimb
import json

class TestQuickStart(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testQuickStart(self):
        message = "Hello, World!"
        say = freeclimb.Say(text=message)
        script = freeclimb.PerclScript(commands=[say])
        data = script.to_json()
        self.assertEqual(data, '[{"Say": {"text": "Hello, World!"}}]')


if __name__ == '__main__':
    unittest.main()
