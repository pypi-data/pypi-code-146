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
Luigi Tasks
"""

from __future__ import unicode_literals, absolute_import

import os
import datetime
import subprocess
import sys

import luigi
import six

from rattail.time import date_range

# TODO: deprecate / remove this
from rattail.luigi.logging import WarnSummaryIfProblems


class OvernightTask(luigi.Task):
    """
    Base class for overnight automation tasks.
    """
    date = luigi.DateParameter()

    # TODO: subclass must define this
    filename = None

    # how long should we wait after task completes, for datasync to catch up?
    datasync_wait_minutes = None

    def output(self):
        return luigi.LocalTarget('{}/{}'.format(self.date.strftime('%Y/%m/%d'), self.filename))

    def run_command(self):
        raise NotImplementedError

    def touch_output(self):
        with self.output().open('w') as f:
            pass

    def datasync_wait(self, minutes=None, initial_delay=10):
        """
        :param int initial_delay: Number of seconds for the initial delay,
           before we actually start to wait on the queue to clear out.
        """
        if minutes is None:
            minutes = self.datasync_wait_minutes or 10

        # sometimes the datasync queue can take a moment to actually "fill up"
        # initially, so we wait a full minute to ensure that happens before we
        # start actually waiting for it to empty out again
        if initial_delay:
            subprocess.check_call(['sleep', six.text_type(initial_delay)])

        subprocess.check_call([
            'bin/rattail',
            '--config=app/cron.conf',
            'datasync',
            '--timeout={}'.format(minutes),
            'wait',
        ])

    def run(self):
        workdir = os.getcwd()
        os.chdir(sys.prefix)
        self.date_plus = self.date + datetime.timedelta(days=1)
        self.run_command()
        if self.datasync_wait_minutes:
            self.datasync_wait(initial_delay=60)
        os.chdir(workdir)
        self.touch_output()


class OvernightTaskWrapper(luigi.WrapperTask):
    """
    Wrapper task for overnight automation
    """
    date = luigi.DateParameter()


class BackfillTask(luigi.Task):
    """
    Base class for backfill "single date" automation tasks.
    """
    key = luigi.Parameter()
    date = luigi.DateParameter()

    def output(self):
        return luigi.LocalTarget('backfill/{}/{}'.format(
            self.key,
            self.date.strftime('%Y-%m-%d')))

    @property
    def rattail_task(self):
        if not hasattr(self, '_rattail_task'):
            app = self.config.get_app()
            luigi_handler = app.get_luigi_handler()
            self._rattail_task = luigi_handler.get_backfill_task(self.key)
        return self._rattail_task

    def get_script(self):
        if not hasattr(self, 'script'):
            self.script = self.rattail_task['script']
        return self.script

    def run(self):
        cmd = "{} {}".format(self.get_script(), self.date)
        subprocess.check_call(cmd, shell=True)
        self.touch_output()

        # record last date for which this backfill task was ran
        app = self.config.get_app()
        luigi_handler = app.get_luigi_handler()
        luigi_handler.record_backfill_last_date(self.rattail_task, self.date)

    def touch_output(self):
        with self.output().open('w') as f:
            pass


class BackwardBackfillRange(luigi.WrapperTask):
    key = luigi.Parameter()
    start_date = luigi.DateParameter()
    end_date = luigi.DateParameter()

    def requires(self):

        # make sure start date comes before end date
        if self.start_date > self.end_date:
            start_date = self.end_date
            end_date = self.start_date
        else:
            start_date = self.start_date
            end_date = self.end_date

        # get full list of dates for range (inclusive!)
        dates = list(date_range(start_date, end_date))
        # nb. also reverse the list
        dates.sort(reverse=True)

        # require task for each date in range
        # nb. must declare oldest date to prevent infinite loop
        BackwardBackfillTask.newest_date = end_date
        return [BackwardBackfillTask(self.key, date)
                for date in dates]


class BackwardBackfillTask(BackfillTask):

    # nb. caller must explicitly set `newest_date` attribute on the
    # class before using - otherwise an infinite loop is likely

    def requires(self):
        if self.date < self.newest_date:
            return BackwardBackfillTask(self.key,
                                        self.date + datetime.timedelta(days=1))


class ForwardBackfillRange(luigi.WrapperTask):
    key = luigi.Parameter()
    start_date = luigi.DateParameter()
    end_date = luigi.DateParameter()

    def requires(self):

        # make sure start date comes before end date
        if self.start_date > self.end_date:
            start_date = self.end_date
            end_date = self.start_date
        else:
            start_date = self.start_date
            end_date = self.end_date

        # get full list of dates for range (inclusive!)
        dates = list(date_range(start_date, end_date))

        # require task for each date in range
        # nb. must declare oldest date to prevent infinite loop
        ForwardBackfillTask.oldest_date = start_date
        return [ForwardBackfillTask(self.key, date)
                for date in dates]


class ForwardBackfillTask(BackfillTask):

    # nb. caller must explicitly set `oldest_date` attribute on the
    # class before using - otherwise an infinite loop is likely

    def requires(self):
        if self.date > self.oldest_date:
            return ForwardBackfillTask(self.key,
                                       self.date - datetime.timedelta(days=1))
