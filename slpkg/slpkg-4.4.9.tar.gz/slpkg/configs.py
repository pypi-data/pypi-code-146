#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import tomli
import platform

from pathlib import Path
from dataclasses import dataclass


class LoadConfigs:
    @staticmethod
    def file(path: str, file: str) -> dict:
        try:
            """ Load the configs from the file. """
            config_path_file = Path(path, f'{file}.toml')
            if config_path_file.exists():
                with open(config_path_file, 'rb') as conf:
                    return tomli.load(conf)
        except tomli.TOMLDecodeError as error:
            raise SystemExit(f"\nValueError: {error}: in the configuration file "
                  "'/etc/slpkg/slpkg.toml'\n")


@dataclass
class Configs:
    """ Default configurations. """

    # Programme name
    prog_name: str = 'slpkg'

    # OS architecture by default
    os_arch: str = platform.machine()

    # All necessary paths
    tmp_path: str = '/tmp'
    tmp_slpkg: str = Path(tmp_path, prog_name)
    build_path: str = Path('tmp', prog_name, 'build')
    download_only: str = Path(tmp_slpkg, '')
    lib_path: str = Path('/var/lib/', prog_name)
    etc_path: str = Path('/etc/', prog_name)
    db_path: str = Path(lib_path, 'database')
    sbo_repo_path: str = Path(lib_path, 'repository')
    log_packages: str = Path('/var', 'log', 'packages')

    # Database name
    database: str = f'database.{prog_name}'

    # SBo repository configs
    sbo_repo_url: str = 'http://slackbuilds.org/slackbuilds/15.0'
    sbo_txt: str = 'SLACKBUILDS.TXT'
    sbo_chglog_txt: str = 'ChangeLog.txt'
    sbo_tar_suffix: str = '.tar.gz'
    sbo_repo_tag: str = '_SBo'

    # Slackware commands
    installpkg: str = 'upgradepkg --install-new'
    reinstall: str = 'upgradepkg --reinstall'
    removepkg: str = 'removepkg'

    # Cli menu colors configs
    colors: str = True

    # Dialog utility
    dialog: str = True

    # Wget options
    wget_options = '-c -N'

    # Choose the view mode
    view_mode: str = 'new'

    load = LoadConfigs()
    configs = load.file(etc_path, prog_name)
    config = configs['configs']

    if config:
        try:
            # OS architecture by default
            os_arch: str = config['os_arch']

            # All necessary paths
            tmp_slpkg: str = config['tmp_slpkg']
            build_path: str = config['build_path']
            download_only: str = config['download_only']
            sbo_repo_path: str = config['sbo_repo_path']

            # Database name
            database: str = config['database']

            # SBo repository details
            sbo_repo_url: str = config['sbo_repo_url']
            sbo_txt: str = config['sbo_txt']
            sbo_chglog_txt: str = config['sbo_chglog_txt']
            sbo_tar_suffix: str = config['sbo_tar_suffix']
            sbo_repo_tag: str = config['sbo_repo_tag']

            # Slackware commands
            installpkg: str = config['installpkg']
            reinstall: str = config['reinstall']
            removepkg: str = config['removepkg']

            # Cli menu colors configs
            colors: str = config['colors']

            # Dialog utility
            dialog: str = config['dialog']

            # Wget options
            wget_options: str = config['wget_options']

            # Choose the view mode
            view_mode: str = config['view_mode']
        except KeyError as error:
            raise SystemExit(f"\nKeyError: {error}: in the configuration file "
                  "'/etc/slpkg/slpkg.toml'\n")

    # Creating the paths if not exists
    paths = [tmp_slpkg,
             build_path,
             download_only,
             sbo_repo_path,
             lib_path,
             etc_path,
             db_path]

    for path in paths:
        if not os.path.isdir(path):
            os.makedirs(path)

    @classmethod
    def colour(cls):
        color = {
            'bold': '',
            'red': '',
            'green': '',
            'yellow': '',
            'cyan': '',
            'blue': '',
            'grey': '',
            'violet': '',
            'endc': ''
        }

        if cls.colors:
            color = {
                'bold': '\033[1m',
                'red': '\x1b[91m',
                'green': '\x1b[32m',
                'yellow': '\x1b[93m',
                'cyan': '\x1b[96m',
                'blue': '\x1b[94m',
                'grey': '\x1b[38;5;247m',
                'violet': '\x1b[35m',
                'endc': '\x1b[0m'
            }

        return color
