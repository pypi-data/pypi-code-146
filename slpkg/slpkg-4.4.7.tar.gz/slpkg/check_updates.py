#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import urllib3
from pathlib import Path
from multiprocessing import Process

from slpkg.configs import Configs
from slpkg.progress_bar import ProgressBar


class CheckUpdates:
    """ Check for changes in the ChangeLog file. """

    def __init__(self):
        self.configs = Configs
        self.colors = self.configs.colour
        self.color = self.colors()
        self.green = self.color['green']
        self.yellow = self.color['yellow']
        self.endc = self.color['endc']
        self.progress = ProgressBar()

    def check(self) -> bool:
        """ Checks the ChangeLogs and returns True or False. """
        local_date = 0

        local_chg_txt = Path(self.configs.sbo_repo_path,
                             self.configs.sbo_chglog_txt)

        http = urllib3.PoolManager()
        repo = http.request(
            'GET', f'{self.configs.sbo_repo_url}/{self.configs.sbo_chglog_txt}')

        if local_chg_txt.is_file():
            local_date = int(os.stat(local_chg_txt).st_size)

        repo_date = int(repo.headers['Content-Length'])

        return repo_date != local_date

    def view_message(self):
        if self.check():
            print(f'\n\n{self.endc}There are new updates available!')
        else:
            print(f'\n\n{self.endc}No updated packages since the last check.')

    def updates(self):
        """ Starting multiprocessing download process. """
        message = f'Checking for news in the Changelog.txt file...'

        # Starting multiprocessing
        p1 = Process(target=self.view_message)
        p2 = Process(target=self.progress.bar, args=(message, ''))

        p1.start()
        p2.start()

        # Wait until process 1 finish
        p1.join()

        # Terminate process 2 if process 1 finished
        if not p1.is_alive():
            p2.terminate()

        # Wait until process 2 finish
        p2.join()

        # Restore the terminal cursor
        print('\x1b[?25h')
