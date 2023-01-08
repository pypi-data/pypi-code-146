# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2023 Lance Edgar
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
Problem Reports for Trainwreck
"""

from __future__ import unicode_literals, absolute_import

import datetime

import six

from rattail.problems import ProblemReport


class MissingDatabases(ProblemReport):
    """
    Looks for missing Trainwreck databases, with the assumption that
    there should be one DB per year archived.
    """
    system_key = 'trainwreck'
    problem_key = 'missing_dbs'
    problem_title = "Missing Databases"

    def find_problems(self, **kwargs):
        trainwreck_handler = self.app.get_trainwreck_handler()
        problems = []

        # this check only makes sense when using rotation
        if trainwreck_handler.use_rotation():

            # so far we are just looking for next year's db.  this
            # "problem" is hardly urgent since we have a whole year to
            # create the db, but still need the reminder.
            next_year = six.text_type(self.app.today().year + 1)
            if next_year not in self.config.trainwreck_engines:
                problems.append(next_year)

        return problems


class CurrentNeedsPruning(ProblemReport):
    """
    Looks for "old" transactions which need to be purged from the
    "current" Trainwreck DB.
    """
    system_key = 'trainwreck'
    problem_key = 'current_needs_pruning'
    problem_title = "Current DB Needs Pruning"

    def find_problems(self, **kwargs):
        trainwreck_handler = self.app.get_trainwreck_handler()
        problems = []

        # this check only makes sense when using rotation
        if trainwreck_handler.use_rotation():

            # cutoff is 1 Jan on oldest "current" year
            current_years = trainwreck_handler.current_years()
            cutoff_year = self.app.today().year - current_years + 1
            cutoff = datetime.datetime(cutoff_year, 1, 1)
            cutoff = self.app.localtime(cutoff)

            # just count txns older than cutoff
            trainwreck_session = trainwreck_handler.make_session()
            trainwreck = trainwreck_handler.get_model()
            count = trainwreck_session.query(trainwreck.Transaction)\
                                      .filter(trainwreck.Transaction.end_time < self.app.make_utc(cutoff))\
                                      .count()
            if count:
                problems.append((count, cutoff))

        return problems
