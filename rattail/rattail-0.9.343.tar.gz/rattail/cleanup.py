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
Cleanup Handler

See also :doc:`rattail-manual:base/handlers/other/cleanup`.
"""

from __future__ import unicode_literals, absolute_import

import logging

from rattail.app import GenericHandler
from rattail.util import load_entry_points


log = logging.getLogger(__name__)


class CleanupHandler(GenericHandler):
    """
    Base class and default implementation for the "cleanup" handler,
    responsible for removing old unwanted files etc.
    """

    def cleanup_everything(self, session, dry_run=False, progress=None, **kwargs):
        """
        Invoke cleanup logic for all enabled cleaners.
        """
        cleaners = self.get_all_cleaners()
        for key in sorted(cleaners):
            cleaner = cleaners[key]
            log.debug("running cleanup for: %s", key)
            cleaner.cleanup(session, dry_run=dry_run, progress=progress)

    def get_all_cleaners(self, **kwargs):
        """
        Return a dictionary containing all registered cleaner objects.
        """
        cleaners = load_entry_points('rattail.cleaners')
        for key in list(cleaners):
            cleaner = cleaners[key](self.config)
            cleaner.key = key
            cleaners[key] = cleaner
        return cleaners

    def get_cleaner(self, key):
        """
        Retrieve a specific cleaner object.
        """
        cleaners = self.get_all_cleaners()
        return cleaners.get(key)


class Cleaner(object):
    """
    Base class for cleaners.
    """

    def __init__(self, config, **kwargs):
        self.config = config
        self.app = config.get_app()
        self.model = self.app.model

    def cleanup(self, session, dry_run=False, progress=None, **kwargs):
        """
        Perform actual cleanup steps as needed.
        """
