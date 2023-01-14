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
DataSync Handler
"""

from __future__ import unicode_literals, absolute_import

import datetime
import logging
import subprocess

from six.moves.xmlrpc_client import ProtocolError

from rattail.app import GenericHandler
from rattail.datasync.config import load_profiles


log = logging.getLogger(__name__)


class DatasyncHandler(GenericHandler):

    def should_use_profile_settings(self):
        """
        This declares whether datasync profiles should be read from
        config file only (the default) or from settings in the DB.

        :returns: True if settings in the DB should be used; False if not.
        """
        return self.config.getbool('rattail.datasync', 'use_profile_settings',
                                   default=False)

    def get_supervisor_process_name(self, require=False, **kwargs):
        getter = self.config.require if require else self.config.get
        return getter('rattail.datasync', 'supervisor_process_name')

    def get_supervisor_process_info(self, name=None, **kwargs):
        if not name:
            name = self.get_supervisor_process_name(require=True)

        proxy = self.app.make_supervisorctl_proxy()

        try:
            return proxy.supervisor.getProcessInfo(name)
        except ProtocolError as error:
            raise self.app.safe_supervisor_protocol_error(error)

    def restart_supervisor_process(self, name=None, **kwargs):
        if not name:
            name = self.get_supervisor_process_name()

        try:
            proxy = self.app.make_supervisorctl_proxy()
        except:
            log.warning("failed to make supervisorctl proxy", exc_info=True)

        else:
            # we have our proxy, so use that, then return
            try:
                info = proxy.supervisor.getProcessInfo(name)
                if info['state'] != 0:
                    proxy.supervisor.stopProcess(name)
                proxy.supervisor.startProcess(name)
            except ProtocolError as error:
                raise self.app.safe_supervisor_protocol_error(error)
            return

        # no proxy, but we can still try command line
        # TODO: should rename this setting at some point?
        cmd = self.config.get('tailbone', 'datasync.restart')
        if cmd:
            cmd = self.config.parse_list(cmd)
        elif name:
            cmd = ['supervisorctl', 'restart', name]

        log.debug("attempting datasync restart with command: %s", cmd)

        try:
            output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as error:
            log.warning("failed to restart datasync; output was:")
            log.warning(error.output)
            raise

    def get_configured_profiles(self, **kwargs):
        return load_profiles(self.config, **kwargs)

    def get_watcher_lastrun(self, watcher_key, local=False, tzinfo=True,
                            session=None):
        """
        Retrieve the "last run" time for the datasync watcher thread
        identifed by ``watcher_key``.
        """
        # the 'last run' value is maintained as UTC
        lastrun_setting = self.get_watcher_lastrun_setting(watcher_key)
        timefmt = self.get_lastrun_timefmt()

        close = False
        if not session:
            session = self.app.make_session()
            close = True
        lastrun = self.app.get_setting(session, lastrun_setting)
        if close:
            session.close()

        if lastrun:
            lastrun = datetime.datetime.strptime(lastrun, timefmt)
            if local:
                return self.app.localtime(lastrun, from_utc=True, tzinfo=tzinfo)
            else:
                return self.app.make_utc(lastrun, tzinfo=tzinfo)

    def get_lastrun_timefmt(self):
        """
        Retrieve the "last run" time format.
        """
        return '%Y-%m-%d %H:%M:%S'

    def get_watcher_lastrun_setting(self, watcher_key):
        """
        Retrieve the "last run" setting name for the given watcher.
        """
        return 'rattail.datasync.{}.watcher.lastrun'.format(watcher_key)
