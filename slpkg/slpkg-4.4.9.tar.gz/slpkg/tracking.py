#!/usr/bin/python3
# -*- coding: utf-8 -*-

from slpkg.configs import Configs
from slpkg.views.ascii import Ascii
from slpkg.dependencies import Requires


class Tracking:
    """ Tracking of the package dependencies. """

    def __init__(self):
        self.configs = Configs
        self.ascii = Ascii()
        self.llc = self.ascii.lower_left_corner
        self.hl = self.ascii.horizontal_line
        self.colors = self.configs.colour
        self.color = self.colors()
        self.cyan = self.color['cyan']
        self.grey = self.color['grey']
        self.yellow = self.color['yellow']
        self.endc = self.color['endc']

    def packages(self, packages: list):
        """ Prints the packages dependencies. """
        print(f"The list below shows the packages with dependencies:\n")

        char = f' {self.llc}{self.hl}'
        for i, package in enumerate(packages):
            requires = Requires(package).resolve()
            how_many = len(requires)

            if not requires:
                requires = ['No dependencies']

            print(f'{self.yellow}{package}{self.endc}')
            print(f'{char} {self.cyan}{" ".join([req for req in requires])}{self.endc}')
            print(f'\n{self.grey}{how_many} dependencies for {package}{self.endc}\n')
