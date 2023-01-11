#!/usr/bin/python3
# -*- coding: utf-8 -*-

class Version:
    """ Print the version. """

    def __init__(self):
        self.version_info = (4, 4, 7)
        self.version = '{0}.{1}.{2}'.format(*self.version_info)
        self.license = 'MIT License'
        self.author = 'Dimitris Zlatanidis (dslackw)'
        self.homepage = 'https://dslackw.gitlab.io/slpkg'

    def view(self):
        """ Prints the version. """
        print(f'Version: {self.version}\n'
              f'Author: {self.author}\n'
              f'License: {self.license}\n'
              f'Homepage: {self.homepage}')
