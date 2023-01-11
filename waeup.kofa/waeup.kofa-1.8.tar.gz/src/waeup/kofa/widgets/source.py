## $Id: source.py 12506 2015-01-22 09:54:57Z henrik $
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
"""Improved source widgets.

"""

from zope.browserpage import ViewPageTemplateFile
from zope.formlib.source import SourceOrderedMultiSelectWidget
from zope.formlib.itemswidgets import OrderedMultiSelectWidget

class KofaSourceOrderedMultiSelectWidget(SourceOrderedMultiSelectWidget):
    """A multi-selection widget with ordering support."""

    template = ViewPageTemplateFile('orderedSelectionList.pt')

    def __call__(self):
        return self.template()

class KofaOrderedMultiSelectWidget(OrderedMultiSelectWidget):
    """A multi-selection widget with ordering support."""

    template = ViewPageTemplateFile('orderedSelectionList.pt')

    def __call__(self):
        return self.template()