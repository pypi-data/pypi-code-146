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
Commands relating to Postfix
"""

from __future__ import unicode_literals, absolute_import

import re
import sys
import subprocess
import logging

import six

from rattail.commands.core import Subcommand


log = logging.getLogger(__name__)


class PostfixSummary(Subcommand):
    """
    Generate (and maybe email) a Postfix log summary
    """
    name = 'postfix-summary'
    description = __doc__.strip()

    def add_parser_args(self, parser):

        parser.add_argument('--email', action='store_true', default=False,
                            help="Email the summary instead of displaying it.")

        parser.add_argument('--problems-only', action='store_true',
                            help="Only show summary if it contains problems.")

        parser.add_argument('--yesterday', action='store_true',
                            help="Show summary for previous day only.")

        parser.add_argument('file', nargs='*', default=['/var/log/mail.log'],
                            help="Path(s) to mail log file(s)")

    def run(self, args):

        # TODO: any way to get around using 'sudo' here?
        cmd = ['sudo', 'pflogsumm', '--problems-first']
        if args.yesterday:
            cmd.extend(['-d', 'yesterday'])
        cmd.extend(args.file)

        # run cmd
        output = subprocess.check_output(cmd).decode('utf_8')

        # parse problem counts
        problems = {}
        pattern = re.compile(r'^ +(\d)   (deferred|bounced|rejected|reject warnings|held|discarded)\b')
        for line in output.split('\n'):
            match = pattern.match(line)
            if match:
                problem = match.group(2)
                if problem in problems:
                    log.warning("extra line matches '%s' pattern: %s", problem, line)
                problems[problem] = int(match.group(1))

        log.info("postfix summary contained %s problems",
                 sum(six.itervalues(problems)))

        # bail if caller only wants to see problems and we have none
        if args.problems_only:
            if not any(six.itervalues(problems)):
                return

        # just display the summary unless we're to email it
        if args.email:
            self.app.send_email('postfix_summary', {
                'output': output,
                'problems': problems,
            })
        else:
            self.stdout.write(output)
