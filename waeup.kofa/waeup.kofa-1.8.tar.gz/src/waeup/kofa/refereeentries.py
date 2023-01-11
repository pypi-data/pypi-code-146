## $Id: schoolgrades.py 12426 2015-01-08 14:25:54Z uli $
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
"""Components representing and aggregating referee entries.
"""
import grok
from zope.formlib.interfaces import IInputWidget, IDisplayWidget
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.schema.fieldproperty import FieldProperty
from zope.schema import Object
from waeup.kofa.interfaces import IRefereeEntry, IRefereeEntryField
from waeup.kofa.widgets.objectwidget import (
    KofaObjectWidget, KofaObjectDisplayWidget
    )


#: A unique default value.
DEFAULT_VALUE = object()


class RefereeEntry(grok.Model):
    """A referee entry contains a name and a email.
    """
    grok.implements(IRefereeEntry)
    name = FieldProperty(IRefereeEntry['name'])
    email = FieldProperty(IRefereeEntry['email'])

    def __init__(self, name=None, email=None, email_sent=False):
        super(RefereeEntry, self).__init__()
        if name is not None:
            self.name = name
        if email is not None:
            self.email = email
        self.email_sent = email_sent
        if not email_sent == True:
            self.email_sent = False
        return

    def __eq__(self, obj):
        """Two RefereeEntry objects are equal if their `name` and
           `email` are equal.
        """
        for name in ('name', 'email',):
            if getattr(self, name) != getattr(obj, name, DEFAULT_VALUE):
                return False
        return True

    def __ne__(self, other):
        """Two RefereeEntries are not equal, if their equality test fails.

        a != b <-> not(a == b). Python doc tell, that __ne__ should
        also be rovided, whenever __eq__ is implemented.
        """
        return not self.__eq__(other)

    def to_string(self):
        """A string representation that can be used in exports.

        Returned is a unicode string of format
        ``(u'<NAME>','<EMAIL>',<EMAILSENT>)``.
        """
        return unicode((self.name, self.email, self.email_sent))

    @classmethod
    def from_string(cls, string):
        """Create new RefereeEntry instance based on `string`.

        The string is expected to be in format as delivered by
        meth:`to_string`.

        This is a classmethod. This means, you normally will call::

          RefereeEntry.from_string(mystring)

        i.e. use the `RefereeEntry` class, not an instance thereof.
        """
        string = string.replace("u''", "None").replace("''", "None")
        name, email, email_sent = eval(string)
        return cls(name, email, email_sent)


class RefereeEntryField(Object):
    """A zope.schema-like field for usage in interfaces.

    If you want to define an interface containing referee entries, you
    can do so like this::

      class IMyInterface(Interface):
          my_referee_entry = RefereeEntryField()

    Default widgets are registered to render referee entry fields.
    """
    grok.implements(IRefereeEntryField)

    def __init__(self, **kw):
        super(RefereeEntryField, self).__init__(IRefereeEntry, **kw)
        return


# register KofaObjectWidgets as default widgets for IRefereeEntryFields
@grok.adapter(IRefereeEntryField, IBrowserRequest)
@grok.implementer(IInputWidget)
def referee_entry_input_widget(obj, req):
    return KofaObjectWidget(obj, req, RefereeEntry)


# register a display widget for IRefereeEntryFields
@grok.adapter(IRefereeEntryField, IBrowserRequest)
@grok.implementer(IDisplayWidget)
def referee_entry_display_widget(obj, req):
    return KofaObjectDisplayWidget(obj, req, RefereeEntry)
