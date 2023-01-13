#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
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
        self.flag_resolve_off = '--resolve-off'
        self.flag_reinstall = '--reinstall'
        self.flag_yes = '--yes'
        self.session = Session
        self.utils = Utilities()
        self.black = Blacklist()
        self.dialog = DialogBox()
        self.configs = Configs
        self.colors = self.configs.colour
        self.color = self.colors()
        self.yellow = self.color['yellow']
        self.cyan = self.color['cyan']
        self.red = self.color['red']
        self.grey = self.color['grey']
        self.violet = self.color['violet']
        self.endc = self.color['endc']
        self.installed_packages = []
        self.ascii = Ascii()

    def view_packages(self, package, version, mode):
        """ Printing the main packages. """
        color = self.cyan
        if mode == 'remove':
            color = self.red
        if mode == 'build':
            color = self.yellow
        if mode == 'upgrade':
            color = self.violet

        self.ascii.draw_view_package(package, version, color)

    def view_skipping_packages(self, sbo, version):
        """ Print the skipping packages. """
        print(f'[{self.yellow}Skipping{self.endc}] {sbo}-{version} {self.red}(already installed){self.endc}')

    def build_packages(self, slackbuilds: list, dependencies: list):
        """ View packages for build only. """
        self.ascii.draw_package_title_box('The following packages will be build:', 'Build Packages')

        for sbo in slackbuilds:
            version = SBoQueries(sbo).version()
            self.view_packages(sbo, version, mode='build')

        if dependencies:
            self.ascii.draw_middle_line()
            self.ascii.draw_dependency_line()

            for sbo in dependencies:
                version = SBoQueries(sbo).version()
                self.view_packages(sbo, version, mode='build')

        self.summary(slackbuilds, dependencies, option='build')

    def install_packages(self, slackbuilds: list, dependencies: list, mode: str):
        """ View packages for install. """
        title = 'Install Packages'
        if mode == 'upgrade':
            title = 'Upgrade Packages'

        self.ascii.draw_package_title_box('The following packages will be installed or upgraded:', title)

        for sbo in slackbuilds:
            version = SBoQueries(sbo).version()
            self.view_packages(sbo, version, mode=mode)

        if dependencies:
            self.ascii.draw_middle_line()
            self.ascii.draw_dependency_line()

            for sbo in dependencies:
                version = SBoQueries(sbo).version()
                self.view_packages(sbo, version, mode=mode)

        self.summary(slackbuilds, dependencies, option=mode)

    def download_packages(self, slackbuilds: list):
        """ View downloaded packages. """
        self.ascii.draw_package_title_box('The following packages will be downloaded:', 'Download Packages')

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

        if dependencies and self.flag_resolve_off not in self.flags:
            dependencies = self.choose_dependencies_for_remove(dependencies)

        self.ascii.draw_package_title_box('The following packages will be removed:', 'Remove Packages')

        for pkg in slackbuilds:
            self._view_removed(pkg)

        if dependencies and self.flag_resolve_off not in self.flags:
            self.ascii.draw_middle_line()
            self.ascii.draw_dependency_line()

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
            elif installed and self.flag_reinstall in self.flags:
                upgrade += 1
            elif (installed and LooseVersion(repo_ver) > LooseVersion(inst_ver) and
                    self.flag_reinstall not in self.flags):
                upgrade += 1
            elif installed and option == 'remove':
                remove += 1

        self.ascii.draw_bottom_line()

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
            print(f'{self.yellow}{dep[0]}{self.endc}')
            self.ascii.draw_log_package(dep[1])

        print('Note: After cleaning you should remove them one by one.')

    def question(self):
        """ Manage to proceed. """
        if self.flag_yes not in self.flags:
            answer = input('\nDo you want to continue? [y/N] ')
            if answer not in ['Y', 'y']:
                raise SystemExit()
        print()
