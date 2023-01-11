#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
import subprocess
from multiprocessing import Process

from slpkg.configs import Configs
from slpkg.utilities import Utilities
from slpkg.views.views import ViewMessage
from slpkg.progress_bar import ProgressBar
from slpkg.models.models import LogsDependencies
from slpkg.models.models import session as Session


class RemovePackages:
    """ Removes installed packages. """

    def __init__(self, packages: list, flags: list):
        self.packages = packages
        self.flags = flags
        self.session = Session
        self.configs = Configs
        self.colors = self.configs.colour
        self.color = self.colors()
        self.bold = self.color['bold']
        self.yellow = self.color['yellow']
        self.red = self.color['red']
        self.endc = self.color['endc']
        self.byellow = f'{self.bold}{self.yellow}'
        self.bred = f'{self.bold}{self.red}'
        self.installed_packages = []
        self.dependencies = []
        self.utils = Utilities()
        self.progress = ProgressBar()
        self.output = 0
        self.remove_pkg = None
        self.stderr = None
        self.stdout = None

    def remove(self):
        """ Removes package with dependencies. """
        view = ViewMessage(self.flags)

        self.installed_packages, self.dependencies = view.remove_packages(
            self.packages)

        view.question()

        start = time.time()
        self.remove_packages()

        if self.dependencies and '--resolve-off' not in self.flags:
            self.delete_deps_logs()

        self.delete_main_logs()

        elapsed_time = time.time() - start

        self.utils.finished_time(elapsed_time)

    def remove_packages(self):
        """ Run Slackware command to remove the packages. """
        for package in self.installed_packages:
            self.remove_pkg = package
            command = f'{self.configs.removepkg} {package}'
            self.multi_process(command, package)

    def delete_main_logs(self):
        """ Deletes main packages from logs. """
        for pkg in self.packages:
            self.session.query(LogsDependencies).filter(
                LogsDependencies.name == pkg).delete()
        self.session.commit()

    def delete_deps_logs(self):
        """ Deletes depends packages from logs. """
        for pkg in self.dependencies:
            self.session.query(LogsDependencies).filter(
                LogsDependencies.name == pkg).delete()
        self.session.commit()

    def multi_process(self, command, package):
        """ Starting multiprocessing remove process. """
        if self.configs.view_mode == 'new':
            done = f' {self.byellow} Done{self.endc}'
            message = f'{self.red}Remove{self.endc}'
            self.stderr = subprocess.DEVNULL
            self.stdout = subprocess.DEVNULL

            # Starting multiprocessing
            p1 = Process(target=self.process, args=(command,))
            p2 = Process(target=self.progress.bar, args=(f'[{message}]', package))

            p1.start()
            p2.start()

            # Wait until process 1 finish
            p1.join()

            # Terminate process 2 if process 1 finished
            if not p1.is_alive():

                if p1.exitcode != 0:
                    done = f' {self.bred} Failed{self.endc}'
                    self.output = p1.exitcode

                print(f'{self.endc}{done}', end='')
                p2.terminate()

            # Wait until process 2 finish
            p2.join()

            # Restore the terminal cursor
            print('\x1b[?25h')
        else:
            self.process(command)

        self.print_error()

    def process(self, command):
        """ Processes execution. """
        self.output = subprocess.call(command, shell=True,
                                      stderr=self.stderr, stdout=self.stdout)
        if self.output != 0:
            raise SystemExit(self.output)

    def print_error(self):
        """ Stop the process and print the error message. """
        if self.output != 0:
            raise SystemExit(f"\n{self.red}FAILED {self.stderr}:{self.endc} package '{self.remove_pkg}' to remove.\n")
