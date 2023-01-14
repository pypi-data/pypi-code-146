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
Luigi task commands
"""

from __future__ import unicode_literals, absolute_import

import sys

from rattail.commands import Subcommand, date_argument


class Overnight(Subcommand):
    """
    Launch an overnight task for Luigi
    """
    name = 'overnight'
    description = __doc__.strip()

    def add_parser_args(self, parser):

        parser.add_argument('--task_key', '-k',
                            help="Config key for the overnight task to be launched.")

        parser.add_argument('--date', type=date_argument,
                            help="Date for which overnight task should be "
                            "launched.  Defaults to yesterday.")

        parser.add_argument('--email-if-empty', action='store_true', default=True,
                            help="Send email even if task produces no output.")
        parser.add_argument('--no-email-if-empty', action='store_false', dest='email_if_empty',
                            help="Send email only if task produces output.")

        parser.add_argument('--email-key',
                            help="Config key for email settings, to be used in "
                            "determining recipients etc.")

        parser.add_argument('--wait', action='store_true', default=True,
                            help="Run the task in-process, and wait for it to "
                            "finish.  This is the default behavior.")
        parser.add_argument('--no-wait', action='store_false', dest='wait',
                            help="Do not wait for the task to finish.  This will "
                            "cause the command to run via the `at` utility, i.e. "
                            "scheduled to start within the next minute.")

        parser.add_argument('--purge-settings', action='store_true',
                            help="Instead of running a task, remove all settings "
                            "from the DB, for all overnight tasks.")

        parser.add_argument('--dry-run', action='store_true',
                            help="Log the final command for the task, but do not "
                            "actually run it.")

    def run(self, args):
        self.luigi_handler = self.app.get_luigi_handler()
        if args.purge_settings:
            self.purge_settings(args)
        else:
            self.launch_task(args)

    def purge_settings(self, args):
        session = self.make_session()
        self.luigi_handler.purge_overnight_settings(session)
        self.finalize_session(session, dry_run=args.dry_run)

    def launch_task(self, args):
        key = args.task_key
        task = self.luigi_handler.get_overnight_task(key)
        if not task:
            self.stderr.write("overnight task not found for key: {}\n".format(key))
            sys.exit(1)

        date = args.date or self.app.yesterday()
        self.luigi_handler.launch_overnight_task(task, date,
                                                 email_if_empty=args.email_if_empty,
                                                 email_key=args.email_key,
                                                 wait=args.wait,
                                                 dry_run=args.dry_run)
