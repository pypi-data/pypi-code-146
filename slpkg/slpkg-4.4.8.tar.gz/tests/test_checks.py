import unittest
from slpkg.checks import Check


class TestPkgInstalled(unittest.TestCase):

    def setUp(self):
        self.check = Check()
        self.packages = ['fish', 'ranger', 'pycharm']

    def test_check_exists(self):
        self.assertIsNone(self.check.exists(self.packages))

    def test_check_unsupported(self):
        self.assertIsNone(self.check.unsupported(self.packages))

    def test_check_installed(self):
        self.assertListEqual(self.packages, self.check.installed(self.packages))

    def test_check_blacklist(self):
        self.assertIsNone(self.check.blacklist(self.packages))


if __name__ == "__main__":
    unittest.main()
