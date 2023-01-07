#!/usr/bin/python3
# -*- coding: utf-8 -*-

# licenses.py is a part of sun.

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


from sun.__metadata__ import __copyright__


ABOUT = ('SUN (Slackware Update Notifier)\n\n'
         'Tray notification applet for informing '
         'about package updates in Slackware.\n\n'
         'Copyright {0} © Dimitris Zlatanidis\n'
         'Slackware® is a Registered Trademark of '
         'Patrick Volkerding.\n'
         'Linux® is a Registered Trademark of Linus '
         'Torvalds.'.format(__copyright__))


LICENSE = ('This program is free software: you can redistribute it and/or modify',
           'it under the terms of the GNU General Public License as published by',
           'the Free Software Foundation, either version 3 of the License, or',
           '(at your option) any later version.\n',
           'This program is distributed in the hope that it will be useful',
           'but WITHOUT ANY WARRANTY; without even the implied warranty of',
           'MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the',
           'GNU General Public License for more details.\n',
           'You should have received a copy of the GNU General Public License',
           'along with this program.  If not, see <http://www.gnu.org/licenses/>.')
