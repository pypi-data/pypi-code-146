## $Id: container.py 7811 2012-03-08 19:00:51Z uli $
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
"""
Containers which contain payment objects.
"""
import grok
from grok import index
from waeup.kofa.payments.interfaces import IPaymentsContainer
from waeup.kofa.utils.helpers import attrs_to_fields

class PaymentsContainer(grok.Container):
    """This is a container for all kind of payments.
    """
    grok.implements(IPaymentsContainer)
    grok.provides(IPaymentsContainer)

    def __init__(self):
        super(PaymentsContainer, self).__init__()
        return

    def archive(self, id=None):
        raise NotImplementedError()

    def clear(self, id=None, archive=True):
        raise NotImplementedError()

PaymentsContainer = attrs_to_fields(PaymentsContainer)
