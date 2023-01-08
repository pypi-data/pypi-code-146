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

import warnings

from .logging import WarnSummaryAlways, WarnSummaryIfProblems

# TODO: eventually stop importing these, so that caller may import
# *some* things from this subpkg without it all breaking if luigi is
# not installed.  primary motivation here is to let the LuigiHandler
# still be created for sake of web views, where we then warn user
# that luigi is not installed.
from .tasks import (OvernightTask as OvernightTaskBase,
                    OvernightTaskWrapper as OvernightTaskWrapperBase)


class OvernightTask(OvernightTaskBase):

    def __init__(self, *args, **kwargs):
        super(OvernightTask, self).__init__(*args, **kwargs)

        warnings.warn("importing OvernightTask from `rattail.luigi` is "
                      "deprecated; please import from `rattail.luigi.tasks` "
                      "instead.", DeprecationWarning, stacklevel=2)


class OvernightTaskWrapper(OvernightTaskWrapperBase):

    def __init__(self, *args, **kwargs):
        super(OvernightTaskWrapper, self).__init__(*args, **kwargs)

        warnings.warn("importing OvernightTaskWrapper from `rattail.luigi` is "
                      "deprecated; please import from `rattail.luigi.tasks` "
                      "instead.", DeprecationWarning, stacklevel=2)
