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
Upgrade handlers
"""

from __future__ import unicode_literals, absolute_import

import os
import shutil
import subprocess
import logging
import warnings

from rattail.app import GenericHandler


log = logging.getLogger(__name__)


class UpgradeHandler(GenericHandler):
    """
    Base class and default implementation for upgrade handlers.
    """

    def get_all_systems(self, **kwargs):
        """
        Returns a list of all "systems" available for upgrade.
        """
        systems = []
        keys = self.config.getlist('rattail.upgrades', 'systems',
                                   default=[])
        for key in keys:
            label = self.config.get('rattail.upgrades',
                                    'system.{}.label'.format(key))
            command = self.config.get('rattail.upgrades',
                                      'system.{}.command'.format(key))
            systems.append({'key': key,
                            'label': label,
                            'command': command})

        systems.sort(key=lambda s: s['label'])

        systems.insert(0, {
            'key': 'rattail',
            'label': self.config.app_title(),
            'command': self.config.require('rattail.upgrades', 'command'),
        })

        return systems

    def get_system(self, key, require=False, **kwargs):
        """
        Returns the "system" record for the given key.
        """
        systems = self.get_all_systems(**kwargs)
        for system in systems:
            if system['key'] == key:
                return system
        if require:
            raise KeyError("No system info found for key: {}".format(key))

    def executable(self, upgrade):
        """
        This method should return a boolean indicating whether or not execution
        should be allowed for the upgrade, given its current condition.  The
        default simply returns ``True`` unless the upgrade has already been
        executed.
        """
        if upgrade is None:
            return True
        return not bool(upgrade.executed)

    def mark_executing(self, upgrade):
        upgrade.executing = True
        upgrade.status_code = self.enum.UPGRADE_STATUS_EXECUTING

    def do_execute(self, upgrade, user, **kwargs):
        """
        Perform all steps needed to fully execute the given upgrade.

        Callers should use this method; you can override
        :meth:`execute()` to customize execution logic.
        """
        # execute proper
        success = self.execute(upgrade, user, **kwargs)

        # declare the upgrade no longer executing
        upgrade.executing = False
        upgrade.executed = self.app.make_utc()
        upgrade.executed_by = user

        # set upgrade status, email key
        if success:
            upgrade.status_code = self.enum.UPGRADE_STATUS_SUCCEEDED
            email_key = 'upgrade_success'
        else:
            upgrade.status_code = self.enum.UPGRADE_STATUS_FAILED
            email_key = 'upgrade_failure'

        # figure out url to the upgrade, if we can
        url = self.config.get('tailbone', 'url.upgrade')
        if not url:
            url = self.config.base_url()
            if url:
                url = '{}/upgrades/{{uuid}}'.format(url)
        if not url:
            url = '#'

        # send appropriate email
        system = self.get_system(upgrade.system or 'rattail')
        self.app.send_email(email_key, {
            'upgrade': upgrade,
            'system_title': system['label'],
            'upgrade_url': url.format(uuid=upgrade.uuid),
        })

    def execute(self, upgrade, user, progress=None, **kwargs):
        """
        Execute the given upgrade, as the given user.
        """
        # record pre-upgrade status
        before_path = self.config.upgrade_filepath(upgrade.uuid,
                                                   filename='requirements.before.txt',
                                                   makedirs=True)
        self.record_requirements_snapshot(before_path)

        # get stdout/stderr file paths
        stdout_path = self.config.upgrade_filepath(upgrade.uuid,
                                                   filename='stdout.log')
        stderr_path = self.config.upgrade_filepath(upgrade.uuid,
                                                   filename='stderr.log')

        # figure out the upgrade command
        if upgrade.system:
            system = self.get_system(upgrade.system, require=True)
            cmd = system['command']
            if not cmd:
                raise ValueError("No command defined for system: {}".format(upgrade.system))
        else:
            cmd = self.get_system('rattail')['command']
        cmd = self.config.parse_list(cmd)

        # run the upgrade command
        log.debug("will run upgrade command: %s", cmd)
        with open(stdout_path, 'wb') as stdout:
            with open(stderr_path, 'wb') as stderr:
                upgrade.exit_code = subprocess.call(cmd, stdout=stdout, stderr=stderr)
        logger = log.warning if upgrade.exit_code != 0 else log.debug
        logger("upgrade command exit code was: %s", upgrade.exit_code)

        # record post-upgrade status
        after_path = self.config.upgrade_filepath(upgrade.uuid, filename='requirements.after.txt')
        self.record_requirements_snapshot(after_path)

        # success as boolean
        return upgrade.exit_code == 0

    def record_requirements_snapshot(self, path):
        pip = self.get_pip_path()
        logpath = os.path.join(self.config.workdir(), 'pip.log')

        kwargs = {}
        suppress_stderr = self.config.getbool('rattail.upgrades', 'suppress_pip_freeze_stderr',
                                              default=False, usedb=False)
        if suppress_stderr:
            stderr = open('/dev/null', 'w')
            kwargs['stderr'] = stderr

        with open(path, 'wb') as stdout:
            subprocess.call([pip, '--log', logpath, 'freeze'], stdout=stdout, **kwargs)

        if suppress_stderr:
            stderr.close()

    def get_pip_path(self):
        path = os.path.join(self.config.appdir(), os.pardir, 'bin', 'pip')
        return os.path.abspath(path)

    def delete_files(self, upgrade):
        """
        Delete all data files for the given upgrade.
        """
        path = self.config.upgrade_filepath(upgrade.uuid)
        if os.path.exists(path):
            shutil.rmtree(path)


def get_upgrade_handler(config, default=None):
    """
    Returns an upgrade handler object.
    """
    warnings.warn("get_upgrade_handler() function is deprecated; please "
                  "use AppHandler.get_upgrade_handler() instead",
                  DeprecationWarning, stacklevel=2)

    app = config.get_app()
    return app.get_upgrade_handler(default=default)
