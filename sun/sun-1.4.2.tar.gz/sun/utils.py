#!/usr/bin/python3
# -*- coding: utf-8 -*-

# utils.py is a part of sun.

# Copyright 2015-2023 Dimitris Zlatanidis <d.zlatanidis@gmail.com>
# All rights reserved.

# sun is a tray notification applet for informing about
# package updates in Slackware.

# https://gitlab.com/dslackw/sun

# sun is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


import os
import re
import tomli
import getpass
import urllib3
from sun.__metadata__ import configs


class Utilities:

    def __init__(self):
        self.configs = configs

    @staticmethod
    def url_open(link):
        """ Return urllib urlopen. """
        r = ''
        try:
            http = urllib3.PoolManager()
            con = http.request('GET', link)
            r = con.data.decode()
        except KeyError:
            print('SUN: error: ftp mirror not supported')

        return r

    @staticmethod
    def read_file(registry):
        """ Return reading file. """
        with open(registry, 'r', encoding='utf-8', errors='ignore') as file_txt:
            read_file = file_txt.read()
            return read_file

    def slack_ver(self):
        """ Open a file and read the Slackware version. """
        dist = self.read_file('/etc/slackware-version')
        sv = re.findall(r'\d+', dist)

        if len(sv) > 2:
            version = ('.'.join(sv[:2]))
        else:
            version = ('.'.join(sv))

        return dist.split()[0], version

    def installed_packages(self):
        """ Count installed Slackware packages. """
        for pkg in os.listdir(self.configs['pkg_path']):
            if not pkg.startswith('.'):
                yield pkg

    @staticmethod
    def read_mirrors(mirrors):
        """ Read the config file and return an uncomment line. """
        for line in mirrors.splitlines():
            line = line.lstrip()

            if line and not line.startswith('#'):
                return line

        return ''

    def mirrors(self):
        """ Get mirror from slackpkg mirrors file. """
        slack_mirror = self.read_mirrors(self.read_file(f'{self.configs["etc_slackpkg"]}mirrors'))

        if slack_mirror.startswith('ftp'):
            print('Please select an http/s mirror not ftp.')
            return ''

        if slack_mirror:
            return f'{slack_mirror}{self.configs["changelog_txt"]}'

        else:
            print('You do not have any http/s mirror selected in /etc/slackpkg/'
                  'mirrors.\nPlease edit that file and uncomment ONE http/s mirror.\n')
            return ''

    def fetch(self):
        """ Get the ChangeLog.txt file size and counts
        the upgraded packages.
        """
        mirrors = self.mirrors()
        r, slackpkg_last_date = '', ''
        upgraded = []

        if mirrors:
            mirror = self.url_open(mirrors)

            path = f'{self.configs["var_lib_slackpkg"]}{self.configs["changelog_txt"]}'

            if os.path.isfile(path):
                slackpkg_last_date = self.read_file(path).split('\n', 1)[0].strip()

            for line in mirror.splitlines():
                if slackpkg_last_date == line.strip():
                    break

                # This condition checks the packages
                if (line.endswith('z:  Upgraded.') or line.endswith('z:  Rebuilt.') or
                        line.endswith('z:  Added.') or line.endswith('z:  Removed.')):
                    upgraded.append(line.split('/')[-1])

                # This condition checks the kernel
                if line.endswith('*:  Upgraded.') or line.endswith('*:  Rebuilt.'):
                    upgraded.append(line)

        return upgraded

    def config(self):
        """ Return sun configuration values. """
        conf_args = {
            'self.configs':
            {'INTERVAL': 60,
             'STANDBY': 3}
        }

        config_file = f'{self.configs["conf_path"]}sun.toml'

        if os.path.isfile(config_file):
            with open(config_file, 'rb') as self.configs:
                conf_args = tomli.load(self.configs)

        return conf_args['configs']

    def os_info(self):
        """ Get the OS info. """
        stype = 'Stable'
        mir = self.mirrors()

        if mir and 'current' in mir:
            stype = 'Current'

        info = (
            f'User: {getpass.getuser()}\n'
            f'OS: {self.slack_ver()[0]}\n'
            f'Version: {self.slack_ver()[1]}\n'
            f'Type: {stype}\n'
            f'Arch: {self.configs["arch"]}\n'
            f'Packages: {len(list(self.installed_packages()))}\n'
            f'Kernel: {self.configs["kernel"]}\n'
            f'Uptime: {self.configs["uptime"]}\n'
            '[Memory]\n'
            f'Free: {self.configs["mem"][9]}, Used: {self.configs["mem"][8]}, '
            f'Total: {self.configs["mem"][7]}\n'
            '[Disk]\n'
            f'Free: {self.configs["disk"][2] // (2**30)}Gi, Used: '
            f'{self.configs["disk"][1] // (2**30)}Gi, '
            f'Total: {self.configs["disk"][0] // (2**30)}Gi\n'
            f'[Processor]\n'
            f'CPU: {self.configs["cpu"]}'
            )

        return info
