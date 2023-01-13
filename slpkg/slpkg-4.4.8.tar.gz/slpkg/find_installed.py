#!/usr/bin/python3
# -*- coding: utf-8 -*-

from slpkg.configs import Configs
from slpkg.utilities import Utilities


class FindInstalled:
    """ Find installed packages. """

    def __init__(self):
        self.configs = Configs
        self.colors = self.configs.colour
        self.color = self.colors()
        self.yellow = self.color['yellow']
        self.cyan = self.color['cyan']
        self.green = self.color['green']
        self.blue = self.color['blue']
        self.endc = self.color['endc']
        self.grey = self.color['grey']
        self.utils = Utilities()

    def find(self, packages: list):
        """ Find the packages. """
        matching = []
        installed = self.utils.all_installed()

        print(f'The list below shows the installed packages '
              f'that contains \'{", ".join([p for p in packages])}\' files:\n')

        for pkg in packages:
            for package in installed:
                if pkg in package:
                    matching.append(package)
        self.matched(matching)

    def matched(self, matching: list):
        """ Print the matched packages. """
        if matching:
            for package in matching:
                pkg = self.utils.split_installed_pkg(package)
                print(f'{self.cyan}{pkg[0]}{self.endc}-{self.yellow}{pkg[1]}{self.endc}-{pkg[2]}-'
                      f'{self.blue}{pkg[3]}{self.endc}_{pkg[4]}')
            print(f'\n{self.grey}Total found {len(matching)} packages.{self.endc}')
        else:
            print('\nDoes not match any package.\n')
