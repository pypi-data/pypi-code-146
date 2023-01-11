import unittest
from slpkg.configs import Configs


class TestConfigs(unittest.TestCase):

    def setUp(self):
        self.sbo_txt = Configs.sbo_txt
        self.sbo_tar_suffix = Configs.sbo_tar_suffix
        self.sbo_repo_tag = Configs.sbo_repo_tag
        self.os_arch = Configs.os_arch

    def test_sbo_txt(self):
        self.assertEqual('SLACKBUILDS.TXT', self.sbo_txt)

    def test_tar_suffix(self):
        self.assertEqual('.tar.gz', self.sbo_tar_suffix)

    def test_repo_tag(self):
        self.assertEqual('_SBo', self.sbo_repo_tag)

    def test_os_arch(self):
        self.assertEqual('x86_64', self.os_arch)


if __name__ == '__main__':
    unittest.main()
