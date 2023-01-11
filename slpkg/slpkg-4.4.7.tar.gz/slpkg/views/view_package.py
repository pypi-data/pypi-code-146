#!/usr/bin/python3
# -*- coding: utf-8 -*-

import urllib3

from slpkg.configs import Configs
from slpkg.queries import SBoQueries
from slpkg.models.models import SBoTable
from slpkg.models.models import session as Session


class ViewPackage:
    """ View the repository packages. """

    def __init__(self):
        self.session = Session
        self.configs = Configs
        self.colors = self.configs.colour

    def package(self, packages: list):
        """ View the packages from the repository. """
        color = self.colors()
        green = color['green']
        blue = color['blue']
        yellow = color['yellow']
        cyan = color['cyan']
        red = color['red']
        endc = color['endc']

        for package in packages:

            info = self.session.query(
                SBoTable.name,
                SBoTable.version,
                SBoTable.requires,
                SBoTable.download,
                SBoTable.download64,
                SBoTable.md5sum,
                SBoTable.md5sum64,
                SBoTable.files,
                SBoTable.short_description,
                SBoTable.location
            ).filter(SBoTable.name == package).first()

            readme = self.http_request(f'{self.configs.sbo_repo_url}/{info[9]}/{info[0]}/README')

            info_file = self.http_request(f'{self.configs.sbo_repo_url}/{info[9]}/{info[0]}/{info[0]}.info')

            maintainer, email, homepage = '', '', ''
            for line in info_file.data.decode().splitlines():
                if line.startswith('HOMEPAGE'):
                    homepage = line[10:-1].strip()
                if line.startswith('MAINTAINER'):
                    maintainer = line[12:-1].strip()
                if line.startswith('EMAIL'):
                    email = line[7:-1].strip()

            deps = (', '.join([f'{pkg} ({SBoQueries(pkg).version()})' for pkg in info[2].split()]))

            print(f'Name: {green}{info[0]}{endc}\n'
                  f'Version: {green}{info[1]}{endc}\n'
                  f'Requires: {green}{deps}{endc}\n'
                  f'Homepage: {blue}{homepage}{endc}\n'
                  f'Download SlackBuild: {blue}{self.configs.sbo_repo_url}/{info[9]}/{info[0]}'
                  f'{self.configs.sbo_tar_suffix}{endc}\n'
                  f'Download sources: {blue}{info[3]}{endc}\n'
                  f'Download_x86_64 sources: {blue}{info[4]}{endc}\n'
                  f'Md5sum: {yellow}{info[5]}{endc}\n'
                  f'Md5sum_x86_64: {yellow}{info[6]}{endc}\n'
                  f'Files: {green}{info[7]}{endc}\n'
                  f'Description: {green}{info[8]}{endc}\n'
                  f'Slackware: {cyan}{self.configs.sbo_repo_url.split("/")[-1]}{endc}\n'
                  f'Category: {red}{info[9]}{endc}\n'
                  f'SBo url: {blue}{self.configs.sbo_repo_url}/{info[9]}/{info[0]}{endc}\n'
                  f'Maintainer: {yellow}{maintainer}{endc}\n'
                  f'Email: {yellow}{email}{endc}\n'
                  f'\nREADME: {cyan}{readme.data.decode()}{endc}')

    @staticmethod
    def http_request(link: str) -> str:
        """ Http get request. """
        http = urllib3.PoolManager()
        return http.request('GET', link)
