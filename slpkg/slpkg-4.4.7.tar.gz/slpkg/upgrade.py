#!/usr/bin/python3
# -*- coding: utf-8 -*-


from distutils.version import LooseVersion

from slpkg.configs import Configs
from slpkg.queries import SBoQueries
from slpkg.utilities import Utilities
from slpkg.blacklist import Blacklist
from slpkg.dialog_box import DialogBox
from slpkg.dependencies import Requires


class Upgrade:
    """ Upgrade the installed packages. """

    def __init__(self):
        self.configs = Configs
        self.utils = Utilities()
        self.dialog = DialogBox()

    def packages(self):
        """ Compares version of packages and returns the maximum. """
        repo_packages = SBoQueries('').sbos()
        black = Blacklist().get()
        upgrade, requires = [], []

        installed = self.utils.all_installed()

        for pkg in installed:
            inst_pkg_name = self.utils.split_installed_pkg(pkg)[0]

            if (pkg.endswith(self.configs.sbo_repo_tag)
                    and inst_pkg_name not in black):

                if inst_pkg_name in repo_packages:
                    inst_ver = self.utils.split_installed_pkg(pkg)[1]
                    repo_ver = SBoQueries(inst_pkg_name).version()

                    if LooseVersion(repo_ver) > LooseVersion(inst_ver):
                        requires += Requires(inst_pkg_name).resolve()
                        upgrade.append(inst_pkg_name)

        # Clean the packages if they are dependencies
        for pkg in upgrade:
            if pkg not in requires:
                yield pkg
