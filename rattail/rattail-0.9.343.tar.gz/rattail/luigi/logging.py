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
Luigi Logging
"""

from __future__ import unicode_literals, absolute_import

import sys
import logging


class WarnSummaryAlways(logging.Filter):
    """
    Custom logging filter, to elevate the Luigi "execution summary"
    message to WARNING level, so that it shows up even when we ignore
    INFO logging.
    """

    def filter(self, record):
        if record.name == 'luigi-interface' and record.levelno == logging.INFO:
            if "===== Luigi Execution Summary =====" in record.msg:

                # looks like a summary, raise to WARNING
                record.levelno = logging.WARNING
                record.levelname = 'WARNING'

                # nb. also emit a blank line, to help set summary
                # apart from any previous output
                sys.stderr.write("\n")

        return True


class WarnSummaryIfProblems(logging.Filter):
    """
    Custom logging filter, to elevate the Luigi "execution summary" message to
    WARNING level, if any problems are detected for the run.  Note that this
    simply checks for the ``:)`` message to know if there were problem.
    """

    good_messages = [
        "This progress looks :) because there were no failed tasks or missing external dependencies",
        "This progress looks :) because there were no failed tasks or missing dependencies",
    ]


    def filter(self, record):
        if record.name == 'luigi-interface' and record.levelno == logging.INFO:
            if "===== Luigi Execution Summary =====" in record.msg:
                if not any([msg in record.msg for msg in self.good_messages]):
                    record.levelno = logging.WARNING
                    record.levelname = 'WARNING'
        return True
