## $Id: catalog.py 12009 2014-11-20 15:52:29Z henrik $
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
"""Components to help cataloging and searching payments.
"""
import grok
from waeup.kofa.interfaces import IUniversity
from waeup.kofa.payments.interfaces import IPayment

class PaymentIndexes(grok.Indexes):
    """A catalog for all payments.
    """
    grok.site(IUniversity)
    grok.name('payments_catalog')
    grok.context(IPayment)

    p_id = grok.index.Field(attribute='p_id')
    p_session = grok.index.Field(attribute='p_session')
    p_category = grok.index.Field(attribute='p_category')
    p_item = grok.index.Field(attribute='p_item')
    p_state = grok.index.Field(attribute='p_state')
