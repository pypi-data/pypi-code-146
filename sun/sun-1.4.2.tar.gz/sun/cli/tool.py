#!/usr/bin/python3
# -*- coding: utf-8 -*-

# sun is a part of sun.

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


import sys
import getpass
import subprocess
from sun.utils import Utilities
from sun.__metadata__ import __version__, configs


def su():
    """ Display message when sun execute as root. """
    if getpass.getuser() == 'root':
        raise SystemExit('sun: Error: It should not be run as root')


def usage():
    """ SUN arguments. """
    args = (f'SUN (Slackware Update Notifier) - Version: {__version__}\n'
            '\nUsage: sun [OPTIONS]\n'
            '\nOptional arguments:\n'
            '  help       Display this help and exit.\n'
            '  start      Start sun daemon.\n'
            '  stop       Stop sun daemon.\n'
            '  restart    Restart sun daemon.\n'
            '  check      Check for software updates.\n'
            '  status     Sun daemon status.\n'
            '  info       Os and machine information.\n'
            '\nStart GTK icon from the terminal: sun start --gtk')
    print(args)


def check_updates():
    """ Check and display upgraded packages. """
    message, packages = 'No news is good news!', ''

    if not daemon_status():
        message = 'SUN is not running'
    else:
        packages = Utilities().fetch()
        count = len(packages)

        if count > 0:
            message = f'{count} software updates are available\n'

    return message, packages


def daemon_status():
    """ Display sun daemon status. """
    output = subprocess.getoutput('ps -af')
    status = False

    if 'sun_daemon' in output:
        status = True

    return status


def _init_check_updates():
    """ Sub function for init. """
    message, packages = check_updates()
    count = len(packages)

    if count > 0:
        print(message)
        for pkg in packages:
            print(pkg)
    else:
        print(message)


def process(cmd, message):
    """ Check subprocess output status. """

    start = (f'{configs["bin_path"]}{configs["daemon_tool"]} -frB --pidfiles=~/.run '
             f'--name=sun_daemon {configs["bin_path"]}python3 '
             f'{configs["bin_path"]}sun_daemon &')

    stop = (f'{configs["bin_path"]}{configs["daemon_tool"]} '
            '--pidfiles=~/.run --name=sun_daemon --stop')

    restart = (f'{configs["bin_path"]}{configs["daemon_tool"]} '
               '--pidfiles=~/.run --name=sun_daemon --restart')

    status = {
        'start': start,
        'stop': stop,
        'restart': restart
    }

    if daemon_status() and cmd == 'start':
        output = 1
        message = 'SUN is already running'

    elif not daemon_status() and cmd == 'stop':
        output = 1
        message = 'SUN is not running'

    elif not daemon_status() and cmd == 'restart':
        output = 1
        message = 'SUN is not running'

    else:
        output = subprocess.call(status[cmd], shell=True)

    if output > 0:
        message = f'FAILED [{output}]: {message}'

    return message


def cli():
    """ Initialization, all begins from here. """
    su()
    args = sys.argv
    args.pop(0)

    if len(args) == 1:
        if args[0] == 'start':
            message = f'Starting SUN daemon:  {configs["daemon_tool"]} &'
            print(process(args[0], message))

        elif args[0] == 'stop':
            message = f'Stopping SUN daemon:  {configs["daemon_tool"]}'
            print(process(args[0], message))

        elif args[0] == 'restart':
            message = f'Restarting SUN daemon:  {configs["daemon_tool"]}'
            print(process(args[0], message))

        elif args[0] == 'check':
            _init_check_updates()

        elif args[0] == 'status':
            status = 'SUN is not running'
            if daemon_status():
                status = 'SUN is running...'
            print(status)

        elif args[0] == 'help':
            usage()

        elif args[0] == 'info':
            print(Utilities().os_info())

        else:
            print("try: 'sun help'")

    elif len(args) == 2 and args[0] == 'start' and args[1] == '--gtk':
        subprocess.call('sun_gtk &', shell=True)

    else:
        raise SystemExit("try: 'sun help'")
