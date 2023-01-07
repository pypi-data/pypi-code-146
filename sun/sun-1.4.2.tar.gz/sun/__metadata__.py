#!/usr/bin/python3
# -*- coding: utf-8 -*-

# __metadata__.py is a part of sun.

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
import shutil
import platform
import subprocess


__all__ = 'sun'
__author__ = 'dslackw'
__copyright__ = '2015-2022'
__version_info__ = (1, 4, 2)
__version__ = '{0}.{1}.{2}'.format(*__version_info__)
__license__ = 'GNU General Public License v3 (GPLv3)'
__email__ = 'd.zlatanidis@gmail.com'
__website__ = 'https://gitlab.com/dslackw/sun'


configs = {
    'updater': 'slackpkg',
    'daemon_tool': 'daemon',
    'changelog_txt': 'ChangeLog.txt',
    'bin_path': '/usr/bin/',
    'pkg_path': '/var/log/packages/',
    'icon_path': '/usr/share/pixmaps/',
    'desktop_path': '/usr/share/applications/',
    'xdg_autostart': '/etc/xdg/autostart/',
    'conf_path': f'/etc/{__all__}/',
    'etc_slackpkg': '/etc/slackpkg/',
    'var_lib_slackpkg': '/var/lib/slackpkg/',
    'arch': platform.machine(),
    'kernel': os.uname()[2],
    'cpu': platform.processor(),
    'mem': subprocess.getoutput('free -h').split(),
    'disk': shutil.disk_usage('/'),
    'uptime': subprocess.getoutput('uptime -p')
}
