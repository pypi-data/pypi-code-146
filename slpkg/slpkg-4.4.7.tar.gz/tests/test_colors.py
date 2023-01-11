import unittest
from slpkg.configs import Configs


class TestColors(unittest.TestCase):

    def setUp(self):
        colors = Configs.colour
        self.color = colors()

    def test_colors(self):
        self.assertIn('bold', self.color)
        self.assertIn('red', self.color)
        self.assertIn('yellow', self.color)
        self.assertIn('cyan', self.color)
        self.assertIn('green', self.color)
        self.assertIn('blue', self.color)
        self.assertIn('grey', self.color)
        self.assertIn('endc', self.color)


if __name__ == '__main__':
    unittest.main()
