import unittest
import os

class HangmanTestCase(unittest.TestCase):
    def test_presence_milestone_3(self):
        self.assertIn('milestone_3.py', os.listdir('.'), 'You should have a file named milestone_3.py in your repository. If you created it, make sure it is in the root directory of your repository')

if __name__ == '__main__':

    unittest.main(verbosity=0)
    