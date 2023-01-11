## $Id: field.py 8171 2012-04-16 07:49:22Z uli $
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
"""Special fields.
"""
from zope.interface import implements
from zope.schema import TextLine, Date
from zope.schema.interfaces import (
    ITextLine, IBaseVocabulary, ISource, IContextSourceBinder, InvalidValue,)
from zope.schema.vocabulary import (
    SimpleVocabulary, getVocabularyRegistry, VocabularyRegistryError)
from waeup.kofa.schema.interfaces import IFormattedDate, IPhoneNumber

class CustomizableErrorMsg(object):
    # Still work in progress

    def __init__(self, not_in_vocab=InvalidValue, **kw):
        self.not_in_vocab = not_in_vocab
        return

class TextLineChoice(TextLine, CustomizableErrorMsg):
    """A TextLine field that also accepts sources, vocabs and values.

    You can use this field like a regular zope.schema.TextLine field.

    You can additionally give `source`, `values` or `vocabulary`
    parameters which will work mainly as with regular
    zope.schema.Choice fields (hence the name). Different to
    `Choice` field, these parameters are not mandatory. Leave them
    out and you have a regular `TextLine` field.

    If you pass a simple source parameter, only those values are
    allowed which also appear in the source. The source should of
    course provide string values as suitable for TextLine fields only!

    If, for example you create a TextLineChoice like this:

      name = TextLineChoice(
        title = u'Some name',
        values = [u'foo', u'bar']  # unicode allowed only!
        )

    any formlib form rendering this field will only accept input u'foo'
    or u'bar'.

    The main advantage of this modified TextLine field is to support
    contextual sources. That means you can define some
    IContextSourceBinder component that looks up catalogs or something
    external else and decide then, whether the entered value of a form
    is allowed or not.

    The code herein is mainly copied over from
    zope.schema._field.Choice with slight modifications.
    """
    implements(ITextLine)

    def __init__(self, values=None, vocabulary=None, source=None, **kw):
        if vocabulary is not None:
            assert (isinstance(vocabulary, basestring)
                    or IBaseVocabulary.providedBy(vocabulary))
            assert source is None, (
                "You cannot specify both source and vocabulary.")
        elif source is not None:
            vocabulary = source

        assert values is None or vocabulary is None, (
               "You cannot specify both values and vocabulary.")

        self.vocabulary = None
        self.vocabularyName = None
        if values is not None:
            self.vocabulary = SimpleVocabulary.fromValues(values)
        elif isinstance(vocabulary, (unicode, str)):
            self.vocabularyName = vocabulary
        elif (ISource.providedBy(vocabulary) or
              IContextSourceBinder.providedBy(vocabulary)):
            self.vocabulary = vocabulary
        super(TextLineChoice, self).__init__(**kw)
        return

    source = property(lambda self: self.vocabulary)

    def bind(self, object):
        """See zope.schema._bootstrapinterfaces.IField."""
        clone = super(TextLineChoice, self).bind(object)
        # get registered vocabulary if needed:
        if IContextSourceBinder.providedBy(self.vocabulary):
            clone.vocabulary = self.vocabulary(object)
            assert ISource.providedBy(clone.vocabulary)
        elif clone.vocabulary is None and self.vocabularyName is not None:
            vr = getVocabularyRegistry()
            clone.vocabulary = vr.get(object, self.vocabularyName)
            assert ISource.providedBy(clone.vocabulary)
        return clone

    def _validate(self, value):
        """First validate against the regular TextLine rules. Then check any
        vocabularies/sources.
        """
        # Do TextLine validation
        super(TextLineChoice, self)._validate(value)

        # Check allowed value range (the vocabulary part)
        vocabulary = self.vocabulary
        if vocabulary is None and self.vocabularyName is not None:
            vr = getVocabularyRegistry()
            try:
                vocabulary = vr.get(None, self.vocabularyName)
            except VocabularyRegistryError:
                raise ValueError("Can't validate value without vocabulary")
        if vocabulary and value not in vocabulary:
            raise InvalidValue(value)
        return

class FormattedDate(Date):
    """A date field that supports additional formatting attributes.

    Stores extra attributes (see below). To make use of these
    attributes in forms, you have to provide widgets that read them
    and use them in their operations, for instance the
    `waeup.kofa.widgets.datewidget.FormattedDateWidget`.

    Extra attributes are as follows:

    `date_format`
      additional attribute to describe desired date format. Must be a
      string that can be fed to strftime/strptime functions. By
      default `None`.

    `show_year`
      boolean indicating whether some kind of year selection should
      be used with this instance. `False` by default.
    """
    implements(IFormattedDate)
    date_format = None
    show_year = False
    def __init__(self, date_format=None, show_year=False, *args, **kw):
        self.date_format = date_format
        self.show_year = show_year
        return super(FormattedDate, self).__init__(*args, **kw)

class PhoneNumber(TextLine):
    """A schema field for phone numbers.
    """
    implements(IPhoneNumber)
