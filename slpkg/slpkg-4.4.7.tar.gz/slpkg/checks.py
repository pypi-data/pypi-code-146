#!/usr/bin/python3
# -*- coding: utf-8 -*-

from pathlib import Path

from slpkg.configs import Configs
from slpkg.queries import SBoQueries
from slpkg.blacklist import Blacklist
from slpkg.utilities import Utilities


class Check:
    """ Some checks before proceed. """

    def __init__(self):
        self.configs = Configs
        self.utils = Utilities()

    @staticmethod
    def exists(slackbuilds: list):
        """ Checking if the slackbuild exists in the repository. """
        not_packages = []

        for sbo in slackbuilds:
            if not SBoQueries(sbo).slackbuild():
                not_packages.append(sbo)

        if not_packages:
            raise SystemExit(f'\nPackages \'{", ".join(not_packages)}\' '
                             'does not exists.\n')

    @staticmethod
    def unsupported(slackbuilds: list):
        """ Checking for unsupported slackbuilds. """
        for sbo in slackbuilds:
            sources = SBoQueries(sbo).sources()

            if 'UNSUPPORTED' in sources:
                raise SystemExit(f"\nPackage '{sbo}' unsupported by arch.\n")

    def installed(self, slackbuilds: list) -> list:
        """ Checking for installed packages. """
        found, not_found = [], []

        for sbo in slackbuilds:
            package = self.utils.is_installed(sbo)
            if package:
                pkg = self.utils.split_installed_pkg(package)[0]
                found.append(pkg)
            else:
                not_found.append(sbo)

        if not_found:
            raise SystemExit(f'\nNot found \'{", ".join(not_found)}\' '
                             'installed packages.\n')

        return found

    def blacklist(self, slackbuilds: list):
        """ Checking if the packages are blacklisted. """
        packages = []
        black = Blacklist()

        for package in black.get():
            if package in slackbuilds:
                packages.append(package)

        if packages:
            raise SystemExit(
                f'\nThe packages \'{", ".join(packages)}\' is blacklisted.\n'
                f'Please edit the blacklist.toml file in '
                f'{self.configs.etc_path} folder.\n')

    def database(self):
        """ Checking for empty table """
        db = Path(self.configs.db_path, self.configs.database)
        if not SBoQueries('').sbos() or not db.is_file():
            raise SystemExit('\nYou need to update the package lists first.\n'
                             'Please run slpkg update.\n')
