import unittest
import os

class HangmanTestCase(unittest.TestCase):
    def test_presence_milestone_2(self):
        self.assertIn('milestone_2.py', os.listdir('.'), 'You should have a file named milestone_2.py in your repository. If you created it, make sure it is in the root directory of your repository')

if __name__ == '__main__':

    unittest.main(verbosity=0)
    