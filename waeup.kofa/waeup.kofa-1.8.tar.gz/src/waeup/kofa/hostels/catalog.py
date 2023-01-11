## $Id: catalog.py 15708 2019-10-28 22:37:30Z henrik $
##
## Copyright (C) 2011 Uli Fouquet & Henrik Bettermann
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
"""Cataloging and searching components for hostels.
"""
import grok
from grok import index
from waeup.kofa.interfaces import IUniversity
from waeup.kofa.hostels.interfaces import IBed

class BedIndexes(grok.Indexes):
    """A catalog for beds.
    """
    grok.site(IUniversity)
    grok.name('beds_catalog')
    grok.context(IBed)

    bed_type = index.Field(attribute='bed_type')
    owner = index.Field(attribute='owner')
    bed_id = index.Field(attribute='bed_id')
