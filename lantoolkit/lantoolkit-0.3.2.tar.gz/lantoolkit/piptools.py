# -*- coding: utf-8 -*-
"""
Created on Fri Jan 13 19:03:14 2023

@author: Administrator
"""
import pip
import subprocess
from rich.progress import track as tqdm


def install(pkg):
    for _ in tqdm(subprocess.call('pip install ' + pkg + ' --use-pep517', shell=True), description='install'):
        pass


def upgrade(pkg):
    pip(['install', '-U', pkg])


def uninstall(pkg):
    pip.main(['uninstall', pkg])


def download(pkg):
    pip.main(['download', pkg])


def reinstall(pkg):
    uninstall(pkg)
    install(pkg)

# noinspection PyTypeChecker


class config:
    def set(*value):
        pip.main(['config', 'set', value])

    def edit(edor):
        if edor == '':
            pip.main(['config', 'edit'])
        else:
            pip.main(['config', '--editor=' + edor, 'edit'])

    def debug():
        pip.main(['config', 'debug'])

    def unset(cfg):
        pip.main(['config', 'unset', cfg])
