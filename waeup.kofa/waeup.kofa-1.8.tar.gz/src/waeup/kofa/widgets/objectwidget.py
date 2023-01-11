## $Id: objectwidget.py 14013 2016-07-04 05:43:25Z henrik $
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
"""A widget to display IObject instances in forms.
"""
from zope.browserpage import ViewPageTemplateFile
from zope.formlib.interfaces import IDisplayWidget
from zope.formlib.objectwidget import ObjectWidget, ObjectWidgetView
from zope.formlib.utility import setUpWidgets
from zope.interface import implements, implementsOnly
from zope.schema import getFieldNamesInOrder

class KofaObjectWidgetView(ObjectWidgetView):
    template = ViewPageTemplateFile('objectwidget.pt')

class KofaObjectWidget(ObjectWidget):

    display = False

    def __init__(self, context, request, factory, **kw):
        #super(ResultsEntryWidget, self).__init__(context, request)
        super(ObjectWidget, self).__init__(context, request)

        # define view that renders the widget
        self.view = self._getView(request)

        # factory used to create content that this widget (field)
        # represents
        self.factory = factory

        # handle foo_widget specs being passed in
        self.names = getFieldNamesInOrder(self.context.schema)
        for k, v in kw.items():
            if k.endswith('_widget'):
                setattr(self, k, v)

        # set up my subwidgets
        self._setUpWidgets()

    def subwidgets(self):
        result = [self.getSubWidget(name) for name in self.names]
        return result

    def _setUpWidgets(self):
        return self._setUpEditWidgets()

    def _getView(self, request):
        return KofaObjectWidgetView(self, request)


class KofaObjectDisplayWidget(KofaObjectWidget):

    implementsOnly(IDisplayWidget)

    display = True

    def _setUpDisplayWidgets(self):
        # subwidgets need a new name
        setUpWidgets(self, self.context.schema, IDisplayWidget,
                         prefix=self.name, names=self.names,
                         context=self.context)

    def _setUpWidgets(self):
        return self._setUpDisplayWidgets()
