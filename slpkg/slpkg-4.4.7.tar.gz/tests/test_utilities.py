import unittest
from slpkg.utilities import Utilities
from slpkg.configs import Configs


class TestUtilities(unittest.TestCase):

    def setUp(self):
        self.utils = Utilities()
        self.build_path = Configs.build_path
        self.package = 'fish-3.4.0-x86_64-2_SBo'

    def test_ins_installed(self):
        self.assertEqual(self.package, self.utils.is_installed('fish'))

    def test_split_name(self):
        self.assertEqual('fish', self.utils.split_installed_pkg(self.package)[0])

    def test_split_version(self):
        self.assertEqual('3.4.0', self.utils.split_installed_pkg(self.package)[1])

    def test_split_arch(self):
        self.assertEqual('x86_64', self.utils.split_installed_pkg(self.package)[2])

    def test_split_build(self):
        self.assertEqual('2', self.utils.split_installed_pkg(self.package)[3])

    def test_split_tag(self):
        self.assertEqual('SBo', self.utils.split_installed_pkg(self.package)[4])


if __name__ == '__main__':
    unittest.main()
