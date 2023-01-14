#!/usr/bin/python3
# -*- coding: utf-8 -*-

from pathlib import Path
from typing import Union

from slpkg.configs import Configs
from slpkg.models.models import SBoTable
from slpkg.models.models import session as Session


class CreateData:
    """ Reads the SLACKBUILDS.TXT file and inserts them into the database. """

    def __init__(self):
        self.configs = Configs
        self.session = Session

    def insert_sbo_table(self):
        """ Install the data. """
        sbo_tags = [
            'SLACKBUILD NAME:',
            'SLACKBUILD LOCATION:',
            'SLACKBUILD FILES:',
            'SLACKBUILD VERSION:',
            'SLACKBUILD DOWNLOAD:',
            'SLACKBUILD DOWNLOAD_x86_64:',
            'SLACKBUILD MD5SUM:',
            'SLACKBUILD MD5SUM_x86_64:',
            'SLACKBUILD REQUIRES:',
            'SLACKBUILD SHORT DESCRIPTION:'
        ]
        path = Path(self.configs.sbo_repo_path, self.configs.sbo_txt)
        sbo_file = self.read_file(path)

        cache = []  # init cache

        print('\nCreating the database... ', end='', flush=True)

        for i, line in enumerate(sbo_file, 1):

            for tag in sbo_tags:
                if line.startswith(tag):
                    line = line.replace(tag, '').strip()
                    cache.append(line)

            if (i % 11) == 0:
                data = SBoTable(name=cache[0], location=cache[1].split('/')[1],
                                files=cache[2], version=cache[3],
                                download=cache[4], download64=cache[5],
                                md5sum=cache[6], md5sum64=cache[7],
                                requires=cache[8], short_description=cache[9])
                self.session.add(data)

                cache = []  # reset cache after 11 lines

        print('Done')

        self.session.commit()

    @staticmethod
    def read_file(file: Union[str, Path]) -> list:
        """ Reads the text file. """
        with open(file, 'r', encoding='utf-8') as f:
            return f.readlines()
