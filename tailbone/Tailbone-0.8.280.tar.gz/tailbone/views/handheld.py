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
(DEPRECATED) Views for handheld batches
"""

from __future__ import unicode_literals, absolute_import

import warnings

# nb. this is imported only for sake of legacy callers
from tailbone.views.batch.handheld import HandheldBatchView


def includeme(config):
    warnings.warn("tailbone.views.handheld is a deprecated module; "
                  "please use tailbone.views.batch.handheld instead",
                  DeprecationWarning)
    config.include('tailbone.views.batch.handheld')
