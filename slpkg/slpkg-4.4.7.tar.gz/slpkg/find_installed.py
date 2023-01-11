#!/usr/bin/python3
# -*- coding: utf-8 -*-

from slpkg.configs import Configs
from slpkg.utilities import Utilities


class FindInstalled:
    """ Find installed packages. """

    def __init__(self):
        self.configs = Configs
        colors = self.configs.colour
        self.color = colors()
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
                print(f'{self.color["cyan"]}{package}{self.color["endc"]}')
        else:
            print('\nDoes not match any package.\n')
