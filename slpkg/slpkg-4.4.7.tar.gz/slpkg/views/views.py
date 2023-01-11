#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import shutil
from typing import Any
from distutils.version import LooseVersion

from slpkg.configs import Configs
from slpkg.views.ascii import Ascii
from slpkg.queries import SBoQueries
from slpkg.utilities import Utilities
from slpkg.blacklist import Blacklist
from slpkg.dialog_box import DialogBox
from slpkg.models.models import LogsDependencies
from slpkg.models.models import session as Session


class ViewMessage:
    """ Print some messages before. """

    def __init__(self, flags: list):
        self.flags = flags
        self.session = Session
        self.utils = Utilities()
        self.black = Blacklist()
        self.dialog = DialogBox()
        self.configs = Configs
        self.colors = self.configs.colour
        self.color = self.colors()
        self.bold = self.color['bold']
        self.green = self.color['green']
        self.bgreen = f'{self.bold}{self.green}'
        self.yellow = self.color['yellow']
        self.cyan = self.color['cyan']
        self.bcyan = f'{self.bold}{self.cyan}'
        self.red = self.color['red']
        self.grey = self.color['grey']
        self.violet = self.color['violet']
        self.blue = self.color['blue']
        self.endc = self.color['endc']
        self.installed_packages = []
        self.columns, self.rows = shutil.get_terminal_size()
        self.ascii = Ascii()
        self.ulc = self.ascii.upper_left_corner
        self.hl = self.ascii.horizontal_line
        self.urc = self.ascii.upper_right_corner
        self.vl = self.ascii.vertical_line
        self.var = self.ascii.vertical_and_right
        self.val = self.ascii.vertical_and_left
        self.llc = self.ascii.lower_left_corner
        self.lrc = self.ascii.lower_right_corner

    def draw_title_box(self, message, title):
        """ Drawing title message. """
        middle_title = int((self.columns / 2) - len(title) + 2)
        print(f'{self.bgreen}{self.ulc}' + f'{self.hl}' * (self.columns - 2) + f'{self.urc}')
        print(f'{self.vl}' + ' ' * middle_title + f'{title}' + ' ' * (self.columns - middle_title - len(title) - 2) +
              f'{self.vl}')
        self.draw_middle_line()
        print(f'{self.vl}{self.endc} {message}' + ' ' * (self.columns - len(message) - 3) + f'{self.bgreen}{self.vl}')
        self.draw_middle_line()
        print(f'{self.bgreen}{self.vl}{self.endc} Package:' + ' ' * 27 + 'Version:' + ' ' * (self.columns - 51) +
              f'Size{self.bgreen} {self.vl}{self.endc}')

    def draw_middle_line(self):
        """ Drawing a middle line. """
        print(f'{self.bgreen}{self.var}' + f'{self.hl}' * (self.columns - 2) + f'{self.val}')

    def draw_dependency_line(self):
        """ Drawing  the dependencies line. """
        print(f'{self.bgreen}{self.vl}{self.endc} Dependencies:' + ' ' * (self.columns - 16) +
              f'{self.bgreen}{self.vl}{self.endc}')

    def view_packages(self, package, version, mode):
        """ Printing the main packages. """
        color = self.cyan
        if mode == 'remove':
            color = self.red
        if mode == 'build':
            color = self.yellow
        if mode == 'upgrade':
            color = self.violet

        print(f'{self.bgreen}{self.vl} {self.bold}{color}{package}{self.endc}' + ' ' * (35 - len(package)) +
              f'{self.blue}{version}' + ' ' * ((self.columns - 37) - len(version) - 1) +
              f'{self.bgreen}{self.vl}{self.endc}')

    def draw_bottom_line(self):
        """ Drawing the bottom line. """
        print(f'{self.bold}{self.green}{self.llc}' + f'{self.hl}' * (self.columns - 2) + f'{self.lrc}{self.endc}')

    def view_skipping_packages(self, sbo, version):
        """ Print the skipping packages. """
        print(f'[{self.yellow}Skipping{self.endc}] {sbo}-{version} {self.red}(already installed){self.endc}')

    def build_packages(self, slackbuilds: list, dependencies: list):
        """ View packages for build only. """
        self.draw_title_box('The following packages will be build:', 'Build Packages')

        for sbo in slackbuilds:
            version = SBoQueries(sbo).version()
            self.view_packages(sbo, version, mode='build')

        if dependencies:
            self.draw_middle_line()
            self.draw_dependency_line()

            for sbo in dependencies:
                version = SBoQueries(sbo).version()
                self.view_packages(sbo, version, mode='build')

        self.summary(slackbuilds, dependencies, option='build')

    def install_packages(self, slackbuilds: list, dependencies: list, mode: str):
        """ View packages for install. """
        title = 'Install Packages'
        if mode == 'upgrade':
            title = 'Upgrade Packages'

        self.draw_title_box('The following packages will be installed or upgraded:', title)

        for sbo in slackbuilds:
            version = SBoQueries(sbo).version()
            self.view_packages(sbo, version, mode=mode)

        if dependencies:
            self.draw_middle_line()
            self.draw_dependency_line()

            for sbo in dependencies:
                version = SBoQueries(sbo).version()
                self.view_packages(sbo, version, mode=mode)

        self.summary(slackbuilds, dependencies, option=mode)

    def download_packages(self, slackbuilds: list):
        """ View downloaded packages. """
        self.draw_title_box('The following packages will be downloaded:', 'Download Packages')

        for sbo in slackbuilds:
            version = SBoQueries(sbo).version()
            self.view_packages(sbo, version, mode='download')

        self.summary(slackbuilds, dependencies=[], option='download')

    def remove_packages(self, packages: list) -> Any:
        """ View remove packages. """
        slackbuilds, dependencies = [], []
        for pkg in packages:
            slackbuilds.append(pkg)

            requires = self.session.query(
                LogsDependencies.requires).filter(
                    LogsDependencies.name == pkg).first()

            if requires:
                dependencies += requires[0].split()

        if dependencies and '--resolve-off' not in self.flags:
            dependencies = self.choose_dependencies_for_remove(dependencies)

        self.draw_title_box('The following packages will be removed:', 'Remove Packages')

        for pkg in slackbuilds:
            self._view_removed(pkg)

        if dependencies and '--resolve-off' not in self.flags:
            self.draw_middle_line()
            self.draw_dependency_line()

            for pkg in dependencies:
                self._view_removed(pkg)
        else:
            dependencies = []

        self.summary(slackbuilds, dependencies, option='remove')

        return self.installed_packages, dependencies

    def _view_removed(self, name: str):
        """ View and creates list with packages for remove. """
        installed = self.utils.all_installed()

        if self.utils.is_installed(name):
            for package in installed:
                pkg = self.utils.split_installed_pkg(package)[0]
                if pkg == name:
                    self.installed_packages.append(package)
                    version = self.utils.split_installed_pkg(package)[1]
                    self.view_packages(pkg, version, mode='remove')

    def choose_dependencies_for_remove(self, dependencies: list) -> list:
        """ Choose packages for remove using the dialog box. """
        height = 10
        width = 70
        list_height = 0
        choices = []
        title = " Choose dependencies you want to remove "

        for package in dependencies:
            repo_ver = SBoQueries(package).version()
            choices += [(package, repo_ver, True)]

        text = f'There are {len(choices)} dependencies:'

        code, tags = self.dialog.checklist(text, title, height, width, list_height, choices, dependencies)

        if not code:
            return dependencies

        os.system('clear')
        return tags

    def summary(self, slackbuilds: list, dependencies: list, option: str):
        """ View the status of the packages action. """
        slackbuilds.extend(dependencies)
        install = upgrade = remove = 0

        for sbo in slackbuilds:
            inst_ver = repo_ver = 0
            installed = self.utils.is_installed(sbo)
            if installed:
                inst_ver = self.utils.split_installed_pkg(installed)[1]
                repo_ver = SBoQueries(sbo).version()

            if not installed:
                install += 1
            elif installed and '--reinstall' in self.flags:
                upgrade += 1
            elif installed and LooseVersion(repo_ver) > LooseVersion(inst_ver) and '--reinstall' not in self.flags:
                upgrade += 1
            elif installed and option == 'remove':
                remove += 1

        self.draw_bottom_line()

        if option in ['install', 'upgrade']:
            print(f'{self.grey}Total {install} packages will be '
                  f'installed and {upgrade} will be upgraded.{self.endc}')

        elif option == 'build':
            print(f'{self.grey}Total {len(slackbuilds)} packages '
                  f'will be build in {self.configs.tmp_path} folder.{self.endc}')

        elif option == 'remove':
            print(f'{self.grey}Total {remove} packages '
                  f'will be removed.{self.endc}')

        elif option == 'download':
            print(f'{self.grey}{len(slackbuilds)} packages '
                  f'will be downloaded in {self.configs.download_only} folder.{self.endc}')

    def logs_packages(self, dependencies: list):
        """ View the logging packages. """
        print('The following logs will be removed:\n')

        for dep in dependencies:
            print(f'{self.cyan}{dep[0]}{self.endc}')
            print(f'  {self.llc}{self.hl}{self.cyan} {dep[1]}{self.endc}\n')
        print('Note: After cleaning you should remove them one by one.')

    def question(self):
        """ Manage to proceed. """
        if '--yes' not in self.flags:
            answer = input('\nDo you want to continue? [y/N] ')
            if answer not in ['Y', 'y']:
                raise SystemExit()
        print()
