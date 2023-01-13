#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
import shutil
import tarfile
from pathlib import Path

from slpkg.configs import Configs
from slpkg.blacklist import Blacklist


class Utilities:

    def __init__(self):
        self.configs = Configs
        self.colors = self.configs.colour
        self.color = self.colors()
        self.yellow = self.color['yellow']
        self.cyan = self.color['cyan']
        self.endc = self.color['endc']
        self.black = Blacklist()

    def is_installed(self, name: str) -> str:
        """ Returns the installed package name. """
        pattern = f'*{self.configs.sbo_repo_tag}'

        var_log_packages = Path(self.configs.log_packages)
        packages = [file.name for file in var_log_packages.glob(pattern)]

        for package in packages:
            pkg = self.split_installed_pkg(package)[0]

            if pkg == name and pkg not in self.black.get():
                return package
        return ''

    def all_installed(self):
        """ Return all installed SBo packages from /val/log/packages folder. """
        pattern = f'*{self.configs.sbo_repo_tag}'
        var_log_packages = Path(self.configs.log_packages)
        installed = [file.name for file in var_log_packages.glob(pattern)]

        return installed

    @staticmethod
    def untar_archive(path: str, archive: str, ext_path: str):
        """ Untar the file to the build folder. """
        tar_file = Path(path, archive)
        untar = tarfile.open(tar_file)
        untar.extractall(ext_path)
        untar.close()

    @staticmethod
    def remove_file_if_exists(path: str, file: str):
        """ Clean the old files. """
        archive = Path(path, file)
        if archive.is_file():
            archive.unlink()

    @staticmethod
    def remove_folder_if_exists(path: str, folder: str):
        """ Clean the old folders. """
        directory = Path(path, folder)
        if directory.exists():
            shutil.rmtree(directory)

    @staticmethod
    def create_folder(path: str, folder: str):
        """ Creates folder. """
        directory = Path(path, folder)
        if not directory.exists():
            directory.mkdir(parents=True, exist_ok=True)

    def split_installed_pkg(self, package: str) -> list:
        """ Split the package by the name, version, arch, build and tag. """
        name = '-'.join(package.split('-')[:-3])
        version = ''.join(package[len(name):].split('-')[:-2])
        arch = ''.join(package[len(name + version) + 2:].split('-')[:-1])
        build = ''.join(package[len(name + version + arch) + 3:].split('-')).replace(self.configs.sbo_repo_tag, '')
        tag = ''.join(package[len(name + version + arch + build) + 4:].split('-'))

        return [name, version, arch, build, tag]

    def finished_time(self, elapsed_time: float):
        """ Printing the elapsed time. """
        print(f'\n{self.yellow}Finished Successfully:{self.endc}',
              time.strftime(f'[{self.cyan}%H:%M:%S{self.endc}]',
                            time.gmtime(elapsed_time)))
