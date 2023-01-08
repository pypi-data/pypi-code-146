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
Luigi utilities
"""

from __future__ import unicode_literals, absolute_import

import os
import logging
import subprocess
import sys
import warnings

import sqlalchemy as sa
import six
from six.moves.xmlrpc_client import ProtocolError

from rattail.app import GenericHandler
from rattail.util import shlex_join


log = logging.getLogger(__name__)


class LuigiHandler(GenericHandler):
    """
    Base class and default implementation for Luigi handler.
    """

    def get_supervisor_process_name(self, require=False, **kwargs):
        getter = self.config.require if require else self.config.get
        return getter('rattail.luigi', 'scheduler.supervisor_process_name')

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
        cmd = self.config.get('rattail.luigi', 'scheduler.restart_command')
        if cmd:
            cmd = self.config.parse_list(cmd)
        elif name:
            cmd = ['supervisorctl', 'restart', name]

        log.debug("attempting luigi scheduler restart with command: %s", cmd)

        try:
            output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as error:
            log.warning("failed to restart luigi scheduler; output was:")
            log.warning(error.output)
            raise

    def get_all_overnight_tasks(self, **kwargs):
        tasks = []

        keys = self.config.getlist('rattail.luigi', 'overnight.tasks',
                                   default=[])
        if not keys:
            keys = self.config.getlist('rattail.luigi', 'overnight_tasks',
                                       default=[])
            if keys:
                warnings.warn("setting is deprecated: [rattail.luigi] overnight_tasks; "
                              "please use [rattail.luigi] overnight.tasks instead",
                              DeprecationWarning)

        for key in keys:
            if key.startswith('overnight-'):
                key = key[len('overnight-'):]
                warnings.warn("overnight task keys use deprecated 'overnight-' prefix",
                              DeprecationWarning)

            lastrun = self.get_overnight_task_setting(key, 'lastrun')
            lastrun = self.app.parse_utctime(lastrun, local=True)
            tasks.append({
                'key': key,
                'description': self.get_overnight_task_setting(key, 'description'),
                'module': self.get_overnight_task_setting(key, 'module'),
                'class_name': self.get_overnight_task_setting(key, 'class_name'),
                'script': self.get_overnight_task_setting(key, 'script'),
                'notes': self.get_overnight_task_setting(key, 'notes'),
                'lastrun': lastrun,
                'last_date': self.get_overnight_task_setting(key, 'last_date',
                                                             typ='date'),
            })
        tasks.sort(key=lambda t: t['description'])
        return tasks

    def get_overnight_task_setting(self, key, name, typ=None, **kwargs):
        getter = self.config.get
        if typ == 'date':
            getter = self.config.getdate
        value = getter('rattail.luigi',
                       'overnight.task.{}.{}'.format(key, name))
        if value is None:
            value = getter('rattail.luigi',
                           'overnight.overnight-{}.{}'.format(key, name))
            if value is not None:
                warnings.warn("[rattail.luigi] overnight.overnight-* settings are deprecated; "
                              "please use [rattail.luigi] overnight.task.* instead",
                              DeprecationWarning)
        return value

    def get_overnight_task(self, key, **kwargs):
        if key.startswith('overnight-'):
            key = key[len('overnight-'):]
            warnings.warn("overnight task keys use deprecated 'overnight-' prefix",
                          DeprecationWarning, stacklevel=2)

        for task in self.get_all_overnight_tasks():
            if task['key'] == key:
                return task

    def launch_overnight_task(self, task, date,
                              keep_config=True,
                              email_if_empty=True,
                              email_key=None,
                              wait=True,
                              dry_run=False,
                              **kwargs):
        """
        Launch the given overnight task, to run for the given date.

        :param task: An overnight task info dict, e.g. as obtained
           from :meth:`get_overnight_task()`.

        :param date: Date for which task should run.

        :param keep_config: If true (the default) then the ``rattail
           overnight`` command will be invoked with the same config
           file(s) which are effective in the current/parent process.
           If false, it will be invoked only with ``app/silent.conf``.

        :param email_if_empty: If true (the default), then email will
           be sent when the task command completes, even if it
           produces no output.  If false, then email is sent only if
           the command produces output.

        :param email_key: Optional config key for email settings to be
           used in determining recipients etc.

        :param wait: If true (the default), the task will run
           in-process, and so will begin immediately, but caller must
           wait for it to complete.  If false, the task will be
           scheduled via the ``at`` command, to begin within the next
           minute.  (This lets process control return immediately to
           the caller.)

        :param dry_run: If true, log the final command for the task
           but do not actually run it.
        """
        appdir = self.config.appdir()
        env = {'PYTHONPATH': appdir}
        if keep_config:
            env['RATTAIL_CONFIG_FILES'] = os.pathsep.join(self.config.files_read)
        else:
            env['RATTAIL_CONFIG_FILES'] = os.path.join(appdir, 'silent.conf')

        # build our command, which will vary per caller request.  by
        # default we do not use the shell to run command, but in some
        # cases must (e.g. when invoking `at`)
        shell = False

        # not waiting means schedule via `at`
        if not wait:

            # rattail overnight <task>
            cmd = [
                '{}/bin/rattail'.format(sys.prefix),
                '--no-versioning',
                'overnight', '-k', task['key'],
                '--date={}'.format(date),
                '--wait',
            ]
            if email_key:
                cmd.extend(['--email-key', email_key])
            if not email_if_empty:
                cmd.append('--no-email-if-empty')

            # echo 'rattail overnight <task>' | at now
            cmd = ['echo', shlex_join(cmd)]
            cmd = shlex_join(cmd)
            cmd = "{} | at 'now + 1 minute'".format(cmd)
            shell = True        # must run command via shell

        else:
            # run-n-mail task immediately

            if task['script']:
                # use whatever script is configured
                cmd = self.config.parse_list(task['script'])

            else:
                # invoke luigi directly
                cmd = [
                    '{}/bin/luigi'.format(sys.prefix),
                    '--module', task['module'],
                    task['class_name'],
                    '--date={}'.format(date),
                ]

            # rattail run-n-mail 'task command'
            cmd = [
                os.path.join(sys.prefix, 'bin', 'rattail'),
                '--no-versioning',
                'run-n-mail',
                '--keep-exit-code',
                '--subject', "Overnight for {}: {}".format(date, task['key']),
                shlex_join(cmd),
            ]
            if email_key:
                cmd.extend(['--key', email_key])
            if not email_if_empty:
                cmd.append('--skip-if-empty')

        # log final command
        log.debug("env is: %s", env)
        log.debug("launching command in subprocess: %s", cmd)
        if dry_run:
            log.debug("dry-run mode, so aborting")
            return

        # run command in subprocess
        curdir = os.getcwd()
        try:
            # nb. always chdir to luigi folder, even if not needed
            os.chdir(os.path.join(appdir, 'luigi'))
            subprocess.check_output(cmd, shell=shell, env=env,
                                    stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as error:
            log.warning("command failed with exit code %s!  output was:",
                        error.returncode)
            log.warning(error.output.decode('utf_8'))
            raise
        else:
            if wait and self.config.getbool('rattail.luigi',
                                            'auto_record_last_date',
                                            # TODO: default should be true
                                            default=False):
                self.record_overnight_last_date(task, date)
        finally:
            # nb. always change back to first dir, in case we're being
            # called by some long-running process, e.g. web app
            os.chdir(curdir)

    def record_overnight_last_date(self, task, date, session=None, **kwargs):
        name = 'rattail.luigi.overnight.task.{}.last_date'.format(task['key'])
        with self.app.short_session(session=session, commit=True) as s:
            self.app.save_setting(s, name, six.text_type(date))

    def get_all_backfill_tasks(self, **kwargs):
        tasks = []

        keys = self.config.getlist('rattail.luigi', 'backfill.tasks',
                                   default=[])
        if not keys:
            keys = self.config.getlist('rattail.luigi', 'backfill_tasks',
                                       default=[])
            if keys:
                warnings.warn("setting is deprecated: [rattail.luigi] backfill_tasks; "
                              "please use [rattail.luigi] backfill.tasks instead",
                              DeprecationWarning)

        for key in keys:
            if key.startswith('backfill-'):
                key = key[len('backfill-'):]
                warnings.warn("backfill task keys use deprecated 'backfill-' prefix",
                              DeprecationWarning)

            lastrun = self.get_backfill_task_setting(key, 'lastrun')
            lastrun = self.app.parse_utctime(lastrun, local=True)
            tasks.append({
                'key': key,
                'description': self.get_backfill_task_setting(key, 'description'),
                'script': self.get_backfill_task_setting(key, 'script'),
                'forward': self.get_backfill_task_setting(key, 'forward',
                                                          typ='bool') or False,
                'notes': self.get_backfill_task_setting(key, 'notes'),
                'lastrun': lastrun,
                'last_date': self.get_backfill_task_setting(key, 'last_date',
                                                            typ='date'),
                'target_date': self.get_backfill_task_setting(key, 'target_date',
                                                              typ='date'),
            })
        tasks.sort(key=lambda t: t['description'])
        return tasks

    def get_backfill_task_setting(self, key, name, typ=None, **kwargs):
        getter = self.config.get
        if typ == 'bool':
            getter = self.config.getbool
        elif typ == 'date':
            getter = self.config.getdate
        value = getter('rattail.luigi',
                       'backfill.task.{}.{}'.format(key, name))
        if value is None:
            value = getter('rattail.luigi',
                           'backfill.{}.{}'.format(key, name))
            if value is not None:
                warnings.warn("[rattail.luigi] backfill.* settings are deprecated; "
                              "please use [rattail.luigi] backfill.task.* instead",
                              DeprecationWarning)
        return value

    def get_backfill_task(self, key, **kwargs):
        if key.startswith('backfill-'):
            key = key[len('backfill-'):]
            warnings.warn("backfill task keys use deprecated 'backfill-' prefix",
                          DeprecationWarning, stacklevel=2)

        for task in self.get_all_backfill_tasks():
            if task['key'] == key:
                return task

    def launch_backfill_task(self, task, start_date, end_date, **kwargs):
        if not start_date or not end_date:
            raise ValueError("must specify both start_date and end_date")

        appdir = self.config.appdir()
        luigi = os.path.join(sys.prefix, 'bin', 'luigi')
        logging_conf = os.path.join(appdir, 'luigi', 'logging.conf')
        cmd = [luigi, '--logging-conf-file', logging_conf,
               '--module', 'rattail.luigi.backfill_runner']

        if task['forward']:
            cmd.append('ForwardBackfillRange')
        else:
            cmd.append('BackwardBackfillRange')

        if start_date > end_date:
            start_date, end_date = end_date, start_date

        cmd.extend([
            '--key', task['key'],
            '--start-date={}'.format(start_date),
            '--end-date={}'.format(end_date),
        ])

        env = {
            'RATTAIL_CONFIG_FILES': os.path.join(appdir, 'silent.conf'),
        }

        last_date = end_date if task['forward'] else start_date
        cmd = [os.path.join(sys.prefix, 'bin', 'rattail'),
               '--config', os.path.join(appdir, 'silent.conf'),
               '--no-versioning',
               'run-n-mail',
               '-S', 'Backfill thru {}: {}'.format(last_date, task['description']),
               shlex_join(cmd)]

        cmd = ['echo', shlex_join(cmd)]
        cmd = shlex_join(cmd)

        cmd = "{} | at 'now + 1 minute'".format(cmd)

        # run command in subprocess
        log.debug("launching command in subprocess: %s", cmd)
        try:
            subprocess.check_output(cmd, shell=True, env=env,
                                    stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as error:
            log.warning("command failed with exit code %s!  output was:",
                        error.returncode)
            log.warning(error.stderr.decode('utf_8'))
            raise

    def record_backfill_last_date(self, task, date, session=None, **kwargs):
        name = 'rattail.luigi.backfill.task.{}.last_date'.format(task['key'])
        with self.app.short_session(session=session, commit=True) as s:
            self.app.save_setting(s, name, six.text_type(date))

    def purge_overnight_settings(self, session):
        model = self.model
        to_delete = session.query(model.Setting)\
                           .filter(sa.or_(
                               model.Setting.name == 'rattail.luigi.overnight.tasks',
                               model.Setting.name.like('rattail.luigi.overnight.task.%.description'),
                               model.Setting.name.like('rattail.luigi.overnight.task.%.notes'),
                               model.Setting.name.like('rattail.luigi.overnight.task.%.module'),
                               model.Setting.name.like('rattail.luigi.overnight.task.%.class_name'),
                               model.Setting.name.like('rattail.luigi.overnight.task.%.script'),
                               # TODO: these should no longer be used
                               model.Setting.name == 'rattail.luigi.overnight_tasks',
                               model.Setting.name.like('rattail.luigi.overnight.%.description'),
                               model.Setting.name.like('rattail.luigi.overnight.%.notes'),
                               model.Setting.name.like('rattail.luigi.overnight.%.script')))\
                           .all()
        for setting in to_delete:
            self.app.delete_setting(session, setting.name)

    def purge_backfill_settings(self, session):
        model = self.model
        to_delete = session.query(model.Setting)\
                           .filter(sa.or_(
                               model.Setting.name == 'rattail.luigi.backfill.tasks',
                               model.Setting.name.like('rattail.luigi.backfill.task.%.description'),
                               model.Setting.name.like('rattail.luigi.backfill.task.%.forward'),
                               model.Setting.name.like('rattail.luigi.backfill.task.%.notes'),
                               model.Setting.name.like('rattail.luigi.backfill.task.%.script'),
                               model.Setting.name.like('rattail.luigi.backfill.task.%.target_date'),
                               # TODO: these should no longer be used
                               model.Setting.name == 'rattail.luigi.backfill_tasks',
                               model.Setting.name.like('rattail.luigi.backfill.%.description'),
                               model.Setting.name.like('rattail.luigi.backfill.%.forward'),
                               model.Setting.name.like('rattail.luigi.backfill.%.notes'),
                               model.Setting.name.like('rattail.luigi.backfill.%.script'),
                               model.Setting.name.like('rattail.luigi.backfill.%.target_date')))\
                           .all()
        for setting in to_delete:
            self.app.delete_setting(session, setting.name)
