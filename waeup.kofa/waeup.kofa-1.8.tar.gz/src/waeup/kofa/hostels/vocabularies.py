## $Id: vocabularies.py 11450 2014-02-27 06:25:18Z henrik $
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
"""Vocabularies and sources for the accommodation section.
"""
from  grok import getSite
from zope.component import getUtility
from zope.catalog.interfaces import ICatalog
from zc.sourcefactory.contextual import BasicContextualSourceFactory
from waeup.kofa.interfaces import (
    SimpleKofaVocabulary, ContextualDictSourceFactoryBase)
from waeup.kofa.interfaces import MessageFactory as _

NOT_OCCUPIED = u'not occupied'

class SpecialHandlingSource(ContextualDictSourceFactoryBase):
    """A application category source delivers all special handling categories
    provided for accommodation booking.
    """
    #: name of dict to deliver from kofa utils.
    DICT_NAME = 'SPECIAL_HANDLING_DICT'

bed_letters = SimpleKofaVocabulary(
    (_('Bed A'),'A'),
    (_('Bed B'),'B'),
    (_('Bed C'),'C'),
    (_('Bed D'),'D'),
    (_('Bed E'),'E'),
    (_('Bed F'),'F'),
    (_('Bed G'),'G'),
    (_('Bed H'),'H'),
    (_('Bed I'),'I'),
    (_('Bed J'),'J'),
    (_('Bed K'),'K'),
    (_('Bed L'),'L'),
    )

blocks = SimpleKofaVocabulary(
    (_('Block A'),'A'),
    (_('Block B'),'B'),
    (_('Block C'),'C'),
    (_('Block D'),'D'),
    (_('Block E'),'E'),
    (_('Block F'),'F'),
    (_('Block G'),'G'),
    (_('Block H'),'H'),
    (_('Block I'),'I'),
    (_('Block J'),'J'),
    (_('Block K'),'K'),
    (_('Block L'),'L'),
    (_('Block M'),'M'),
    (_('Block N'),'N'),
    (_('Block O'),'O'),
    (_('Block P'),'P'),
    (_('Block Q'),'Q'),
    (_('Block R'),'R'),
    (_('Block S'),'S'),
    (_('Block T'),'T'),
    (_('Block U'),'U'),
    (_('Block V'),'V'),
    (_('Block W'),'W'),
    )
