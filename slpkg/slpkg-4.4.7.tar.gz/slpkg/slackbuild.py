#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import time
import subprocess

from pathlib import Path
from collections import OrderedDict
from distutils.version import LooseVersion
from multiprocessing import Process, cpu_count

from slpkg.checksum import Md5sum
from slpkg.configs import Configs
from slpkg.queries import SBoQueries
from slpkg.utilities import Utilities
from slpkg.dialog_box import DialogBox
from slpkg.dependencies import Requires
from slpkg.downloader import Downloader
from slpkg.views.views import ViewMessage
from slpkg.progress_bar import ProgressBar
from slpkg.models.models import LogsDependencies
from slpkg.models.models import session as Session


class Slackbuilds:
    """ Download build and install the SlackBuilds. """

    def __init__(self, slackbuilds: list, flags: list, mode: str):
        self.slackbuilds = slackbuilds
        self.flags = flags
        self.mode = mode
        self.session = Session
        self.utils = Utilities()
        self.dialog = DialogBox()
        self.view_message = ViewMessage(self.flags)
        self.configs = Configs
        self.colors = self.configs.colour
        self.color = self.colors()
        self.bold = self.color['bold']
        self.cyan = self.color['cyan']
        self.red = self.color['red']
        self.yellow = self.color['yellow']
        self.endc = self.color['endc']
        self.byellow = f'{self.bold}{self.yellow}'
        self.bred = f'{self.bold}{self.red}'
        self.install_order = []
        self.dependencies = []
        self.sbos = {}
        self.progress = ProgressBar()
        self.process_message = None
        self.output = 0
        self.stderr = None
        self.stdout = None

    def execute(self):
        """ Starting build or install the slackbuilds. """
        self.creating_dictionary()

        if '--resolve-off' not in self.flags:
            self.creating_dependencies_for_build()

        self.creating_main_for_build()

        self.view_before_build()

        start = time.time()
        self.download_slackbuilds_and_build()
        elapsed_time = time.time() - start

        self.utils.finished_time(elapsed_time)

    def creating_dictionary(self):
        """ Dictionary with the main slackbuilds and dependencies. """
        for sbo in self.slackbuilds:
            self.sbos[sbo] = Requires(sbo).resolve()

    def creating_dependencies_for_build(self):
        """ List with the dependencies. """
        for deps in self.sbos.values():
            for dep in deps:

                # Checks if the package was installed and skipped.
                if ('--skip-installed' in self.flags and
                        self.utils.is_installed(dep)):
                    continue

                if dep in self.slackbuilds:
                    self.slackbuilds.remove(dep)

                self.dependencies.append(dep)

        # Remove duplicate packages and keeps the order.
        dependencies = list(OrderedDict.fromkeys(self.dependencies))

        if dependencies:
            self.dependencies = self.choose_dependencies(dependencies)

        self.install_order.extend(self.dependencies)

    def choose_dependencies(self, dependencies: list):
        """ Choose packages for install. """
        height = 10
        width = 70
        list_height = 0
        choices = []
        title = ' Choose dependencies you want to install '

        for package in dependencies:
            status = True
            repo_ver = SBoQueries(package).version()
            installed = self.utils.is_installed(package)

            if installed:
                status = False

            choices += [(package, repo_ver, status)]

        text = f'There are {len(choices)} dependencies:'

        code, tags = self.dialog.checklist(text, title, height, width,
                                           list_height, choices, dependencies)

        if not code:
            return dependencies

        os.system('clear')

        return tags

    def creating_main_for_build(self):
        """ List with the main slackbuilds. """
        [self.install_order.append(main) for main in self.sbos.keys()]

    def view_before_build(self):
        """ View slackbuilds before proceed. """
        if not self.mode == 'build':
            self.view_message.install_packages(self.slackbuilds, self.dependencies, self.mode)
        else:
            self.view_message.build_packages(self.slackbuilds, self.dependencies)

        del self.dependencies  # no more needed

        self.view_message.question()

    def download_slackbuilds_and_build(self):
        """ Downloads files and sources and starting the build. """
        inst_ver = '0'

        for sbo in self.install_order:

            package = self.utils.is_installed(sbo)

            if package:
                inst_ver = self.utils.split_installed_pkg(package)[1]

            repo_ver = SBoQueries(sbo).version()

            if (self.mode == 'install' and LooseVersion(repo_ver) > LooseVersion(inst_ver) or
                    self.mode == 'upgrade' and package and LooseVersion(repo_ver) > LooseVersion(inst_ver) or
                    package and '--reinstall' in self.flags and self.mode == 'install' or self.mode == 'build'):

                file = f'{sbo}{self.configs.sbo_tar_suffix}'

                self.utils.remove_file_if_exists(self.configs.tmp_slpkg, file)
                self.utils.remove_folder_if_exists(self.configs.build_path, sbo)

                location = SBoQueries(sbo).location()
                url = f'{self.configs.sbo_repo_url}/{location}/{file}'

                down_sbo = Downloader(self.configs.tmp_slpkg, url)
                down_sbo.download()

                self.utils.untar_archive(self.configs.tmp_slpkg, file, self.configs.build_path)

                self.patch_sbo_tag(sbo)

                sources = SBoQueries(sbo).sources()
                self.download_sources(sbo, sources)

                self.build_the_script(self.configs.build_path, sbo)

                if not self.mode == 'build':

                    pkg = self.creating_package_for_install(sbo)
                    self.install_package(pkg)

                    if '--resolve-off' not in self.flags:
                        self.logging_installed_dependencies(sbo)
            else:
                version = self.utils.split_installed_pkg(package)[1]
                self.view_message.view_skipping_packages(sbo, version)

    def patch_sbo_tag(self, sbo):
        """ Patching SBo TAG from the configuration file. """
        sbo_script = Path(self.configs.build_path, sbo, f'{sbo}.SlackBuild')

        if sbo_script.is_file():
            with open(sbo_script, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            with open(sbo_script, 'w') as script:
                for line in lines:
                    if line.startswith('TAG=$'):
                        line = f'TAG=${{TAG:-{self.configs.sbo_repo_tag}}}\n'
                    script.write(line)

    def logging_installed_dependencies(self, name: str):
        """ Logging installed dependencies and used for remove. """
        exist = self.session.query(LogsDependencies.name).filter(
            LogsDependencies.name == name).first()

        requires = Requires(name).resolve()

        # Update the dependencies if exist else create it.
        if exist:
            self.session.query(
                LogsDependencies).filter(
                    LogsDependencies.name == name).update(
                        {LogsDependencies.requires: ' '.join(requires)})

        elif requires:
            deps = LogsDependencies(name=name, requires=' '.join(requires))
            self.session.add(deps)
        self.session.commit()

    def install_package(self, package: str):
        """ Install the packages that before created in the tmp directory. """
        pkg = self.utils.split_installed_pkg(package)[0]

        execute = self.configs.installpkg
        if ('--reinstall' in self.flags and
                self.utils.is_installed(pkg)):
            execute = self.configs.reinstall

        message = f'{self.cyan}Installing{self.endc}'
        self.process_message = f"'{pkg}' to install"

        if self.mode == 'upgrade':
            self.process_message = f"package '{pkg}' to upgrade"
            message = f'{self.cyan}Upgrade{self.endc}'

        command = f'{execute} {self.configs.tmp_path}/{package}'

        self.multi_process(command, package, message)

    def creating_package_for_install(self, name: str):
        """ Creating a list with all the finished packages for
            installation. """
        version = SBoQueries(name).version()

        pattern = f'{name}-{version}-*{self.configs.sbo_repo_tag}*'

        tmp = Path(self.configs.tmp_path)
        packages = [file.name for file in tmp.glob(pattern)]

        return max(packages)

    def build_the_script(self, path: str, name: str):
        """ Run the .SlackBuild script. """
        folder = f'{Path(path, name)}/'
        execute = f'{folder}./{name}.SlackBuild'

        # Change to root privileges
        os.chown(folder, 0, 0)
        for file in os.listdir(folder):
            os.chown(f'{folder}{file}', 0, 0)

        if '--jobs' in self.flags:
            self.set_makeflags()

        message = f'{self.red}Build{self.endc}'
        self.process_message = f"package '{name}' to build"

        self.multi_process(execute, name, message)

    @staticmethod
    def set_makeflags():
        """ Set number of processors. """
        os.environ['MAKEFLAGS'] = f'-j {cpu_count()}'

    def download_sources(self, name: str, sources: list):
        """ Download the sources. """
        path = Path(self.configs.build_path, name)
        checksums = SBoQueries(name).checksum()

        for source, checksum in zip(sources, checksums):
            down_source = Downloader(path, source)
            down_source.download()

            md5sum = Md5sum(self.flags)
            md5sum.check(path, source, checksum, name)

    def multi_process(self, command, filename, message):
        """ Starting multiprocessing install/upgrade process. """
        if self.configs.view_mode == 'new':
            done = f' {self.byellow} Done{self.endc}'
            self.stderr = subprocess.DEVNULL
            self.stdout = subprocess.DEVNULL

            # Starting multiprocessing
            p1 = Process(target=self.process, args=(command,))
            p2 = Process(target=self.progress.bar, args=(f'[{message}]', filename))

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
            raise SystemExit(f"\n{self.red}FAILED {self.output}:{self.endc} {self.process_message}.\n")
