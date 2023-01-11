## $Id: utils.py 13484 2015-11-19 11:34:48Z henrik $
##
## Copyright (C) 2015 Uli Fouquet & Henrik Bettermann
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##
"""General helper functions and utilities for the hostels section.
"""

import grok
from zope.component import getUtility
from zope.catalog.interfaces import ICatalog
from waeup.kofa.interfaces import MessageFactory as _
from waeup.kofa.hostels.interfaces import IHostelsUtils
from waeup.kofa.hostels.vocabularies import NOT_OCCUPIED

class HostelsUtils(grok.GlobalUtility):
    """A collection of parameters and methods subject to customization.
    """
    grok.implements(IHostelsUtils)

    def getBedStatistics(self):
        cat = getUtility(ICatalog, name='beds_catalog')
        stats = {}
        bed_types = (
            'regular_female_fr',
            'regular_female_re',
            'regular_female_fi',
            'regular_female_all',
            'regular_female_reserved',
            'regular_male_fr',
            'regular_male_re',
            'regular_male_fi',
            'regular_male_all',
            'regular_male_reserved',)
        for bed_type in bed_types:
            free = cat.searchResults(
                bed_type=(bed_type, bed_type),
                owner=(NOT_OCCUPIED, NOT_OCCUPIED))
            all = cat.searchResults(
                bed_type=(bed_type, bed_type))
            free = len(free)
            total = len(all)
            occ = total - free
            stats[bed_type] = (occ, free, total)
        return stats