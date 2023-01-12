# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2022 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#
#  You should have received a copy of the GNU General Public License along with
#  Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Cleanup logic
"""

from __future__ import unicode_literals, absolute_import

import os
import logging
import time

from rattail.cleanup import Cleaner


log = logging.getLogger(__name__)


class BeakerCleaner(Cleaner):
    """
    Cleanup logic for old Beaker session files.
    """

    def get_session_dir(self):
        session_dir = self.config.get('rattail.cleanup', 'beaker.session_dir')
        if session_dir and os.path.isdir(session_dir):
            return session_dir

        session_dir = os.path.join(self.config.appdir(), 'sessions')
        if os.path.isdir(session_dir):
            return session_dir

    def cleanup(self, session, dry_run=False, progress=None, **kwargs):
        session_dir = self.get_session_dir()
        if not session_dir:
            return

        data_dir = os.path.join(session_dir, 'data')
        lock_dir = os.path.join(session_dir, 'lock')

        # looking for files older than X days
        days = self.config.getint('rattail.cleanup',
                                  'beaker.session_cutoff_days',
                                  default=30)
        cutoff = time.time() - 3600 * 24 * days

        for topdir in (data_dir, lock_dir):
            if not os.path.isdir(topdir):
                continue

            for dirpath, dirnames, filenames in os.walk(topdir):
                for fname in filenames:
                    path = os.path.join(dirpath, fname)
                    ts = os.path.getmtime(path)
                    if ts <= cutoff:
                        if dry_run:
                            log.debug("would delete file: %s", path)
                        else:
                            os.remove(path)
                            log.debug("deleted file: %s", path)
