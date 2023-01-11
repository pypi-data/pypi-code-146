## $Id: sequencewidget.py 11495 2014-03-13 15:39:27Z uli $
##
## Copyright (C) 2012 Uli Fouquet & Henrik Bettermann
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
"""An improved sequence widget.

We provide a sequence widget that better suits our needs layout-wise
than the default implementation from zope.formlib.
"""
import grok
from zope.i18n import translate
from zope.browserpage import ViewPageTemplateFile
from zope.formlib.interfaces import IInputWidget, IDisplayWidget
from zope.formlib.widgets import (
    ListSequenceWidget, SequenceDisplayWidget)
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.schema.interfaces import IField, IList


class KofaSequenceWidget(ListSequenceWidget):
    """A sequence widget for lists.

    This is basically a plain copy from zope.formlib. We have,
    however, the possibility to tweak the attached template.
    """
    template = ViewPageTemplateFile('sequencewidget.pt')
    _kofa_seq_len_changed = False

    def _generateSequence(self):
        result = super(KofaSequenceWidget, self)._generateSequence()
        if ((self.name + '.add' in self.request.form) or
            (self.name + '.remove' in self.request.form)):
            self._kofa_seq_len_changed = True
        return result


class KofaSequenceDisplayWidget(SequenceDisplayWidget):
    """A sequence widget for lists.

    This is basically a plain copy from zope.formlib. We have,
    however, the possibility to tweak html tags.
    """

    tag = None
    itemTag = 'div'

    def __call__(self):
        """Patch for the orginal __call__ method.

        The orginal __call__ method doesn't call
        the translate function properly.
        """

        # get the data to display:
        if self._renderedValueSet():
            data = self._data
        else:
            data = self.context.get(self.context.context)

        # deal with special cases:
        if data == self.context.missing_value:
            return translate(self._missingValueMessage, context=self.request)
        data = list(data)
        if not data:
            return translate(self._emptySequenceMessage, context=self.request)

        parts = []
        for i, item in enumerate(data):
            widget = self._getWidget(i)
            widget.setRenderedValue(item)
            s = widget()
            if self.itemTag:
                s = "<%s>%s</%s>" % (self.itemTag, s, self.itemTag)
            parts.append(s)
        contents = "\n".join(parts)
        if self.tag:
            contents = "\n%s\n" % contents
            contents = renderElement(self.tag,
                                     cssClass=self.cssClass,
                                     extra=self.extra,
                                     contents=contents)
        return contents


# Register our sequence widgets as default for lists.
@grok.adapter(IList, IField, IBrowserRequest)
@grok.implementer(IInputWidget)
def seq_input_widget(obj, field, req, *args, **kw):
    return KofaSequenceWidget(obj, field, req, *args, **kw)


@grok.adapter(IList, IField, IBrowserRequest)
@grok.implementer(IDisplayWidget)
def seq_display_widget(obj, field, req, *args, **kw):
    return KofaSequenceDisplayWidget(obj, field, req, *args, **kw)
