#!/usr/bin/python3
# -*- coding: utf-8 -*-

from slpkg.queries import SBoQueries
from slpkg.configs import Configs


class SearchPackage:
    """ Search slackbuilds from the repository. """

    def __init__(self):
        self.colors = Configs.colour
        self.color = self.colors()
        self.yellow = self.color['yellow']
        self.cyan = self.color['cyan']
        self.endc = self.color['endc']
        self.green = self.color['green']
        self.grey = self.color['grey']

    def package(self, packages: list):
        """ Searching and print the matched slackbuilds. """
        matching = 0

        names = SBoQueries('').sbos()

        print(f'The list below shows the repo '
              f'packages that contains \'{", ".join([p for p in packages])}\':\n')

        for name in names:
            for package in packages:
                if package in name:
                    matching += 1
                    desc = SBoQueries(name).description().replace(name, '')
                    print(f'{self.cyan}{name}{self.endc}-{self.yellow}{SBoQueries(name).version()}{self.endc}'
                          f'{self.green}{desc}{self.endc}')

        if not matching:
            print('\nDoes not match any package.\n')
        else:
            print(f'\n{self.grey}Total found {matching} packages.{self.endc}')
