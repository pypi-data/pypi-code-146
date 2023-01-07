# -*- coding: utf-8; -*-
"""
Luigi "backfill" tasks
"""

from __future__ import unicode_literals, absolute_import

import os
import logging

from rattail.config import make_config
from rattail.luigi.tasks import (BackwardBackfillRange, ForwardBackfillRange,
                                 BackfillTask)
from rattail.luigi.logging import WarnSummaryAlways


# nb. BackfillTask must be able to fetch task command
config = make_config()
BackfillTask.config = config

# nb. also we must run from the 'luigi' folder to ensure output
# tracking behaves as expected
os.chdir(os.path.join(config.appdir(), 'luigi'))

# make final luigi summary get logged as a warning
logging.getLogger('luigi-interface').addFilter(WarnSummaryAlways())
