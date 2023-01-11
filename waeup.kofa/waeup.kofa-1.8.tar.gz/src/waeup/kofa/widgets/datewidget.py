## $Id: datewidget.py 9498 2012-11-01 15:41:38Z henrik $
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
A datewidget with customizable date format.
"""
import pytz
from datetime import datetime
from zope.component import queryUtility
from zope.formlib.interfaces import ConversionError, IDisplayWidget
from zope.formlib.textwidgets import DateWidget, DateDisplayWidget, escape
from zope.formlib.widget import renderElement, CustomWidgetFactory
from zope.interface import implements
from waeup.kofa.interfaces import IKofaUtils
from waeup.kofa.utils.helpers import to_timezone


#: A dictionary of supported date formats.
#:
#: The following formats are supported:
#:
#: ``iso``
#:    ISO format ``YYYY-MM-DD``
#: ``le``
#:    little endian with slashes: ``DD/MM/YYYY``
#: ``de``
#:    german date format: ``DD.MM.YYYY``
#: ``us``
#:    middle endian format common in the U.S.: ``MM/DD/YYYY``
#:
#: Furthermore we support for input widgets an additional year
#: marker. Input date widgets with this marker provide also a year
#: selector, handy for dates of birth etc.
#:
#: The year-supporting formats are similar to the basic versions above:
#:
#: ``iso-year``
#:    ISO format ``YYYY-MM-DD``
#: ``le-year``
#:    little endian with slashes: ``DD/MM/YYYY``
#: ``de-year``
#:    german date format: ``DD.MM.YYYY``
#: ``us-year``
#:    middle endian format common in the U.S.: ``MM/DD/YYYY``
#:
#: For date display widgets there is naturally no difference between a
#: year and non-year setting (you can for instance use 'le' or 'le-year'
#: with the same output).
DATE_FORMATS = {
    'iso': ('datepicker', '%Y-%m-%d'),
    'le':  ('datepicker-le', '%d/%m/%Y'),
    'de':  ('datepicker-de', '%d.%m.%Y'),
    'us':  ('datepicker-us', '%m/%d/%Y'),
    'iso-year': ('datepicker-year', '%Y-%m-%d'),
    'le-year':  ('datepicker-le-year', '%d/%m/%Y'),
    'de-year':  ('datepicker-de-year', '%d.%m.%Y'),
    'us-year':  ('datepicker-us-year', '%m/%d/%Y'),
    }

#: a dict containing tuples (<FORMAT>, <SHOW_YEAR>) as keys and
#: suitable CSS tags as values.
FORMATS_BY_VALUE = dict(
    [((val[1], 'year' in key), val[0]) for key, val in DATE_FORMATS.items()])

class FormattedDateWidget(DateWidget):
    """A date widget that supports different (and _explicit_) date formats.

    If the widget is bound to a schema field with respective
    attributes, it reads its `show_year` and `date_format` attributes
    (see waeup.kofa.schema.FormattedDate for an example) and sets a
    CSS tag according to these values.

    The widget also accepts ISO format as a fallback, even if a
    different format was set. This should help with imports.

    This is an input widget.
    """
    date_format = '%Y-%m-%d'
    show_year = False

    def __init__(self, context, request, *args, **kw):
        # try to grab date_format and show_year from bound schema field.
        date_format = getattr(context, 'date_format', self.date_format)
        if date_format is not None:
            self.date_format = date_format
        self.show_year = getattr(context, 'show_year', self.show_year)
        # add css class determined by date_format and show_year
        css_cls = FORMATS_BY_VALUE.get((self.date_format, self.show_year), '')
        self.cssClass = ' '.join([self.cssClass, css_cls]).strip()
        return super(FormattedDateWidget, self).__init__(
            context, request, *args, **kw)

    def _toFieldValue(self, input):
        # In import files we can use the hash symbol at the end of a
        # date string to avoid annoying automatic date transformation
        # by Excel or Calc
        input = input.strip('#')
        if input == self._missing:
            return self.context.missing_value
        else:
            try:
                value = datetime.strptime(input, self.date_format)
            except (ValueError, IndexError), v:
                try:
                    # Try ISO format as fallback.
                    # This is needed for instance during imports.
                    value = datetime.strptime(
                        input, FormattedDateWidget.date_format)
                except (ValueError, IndexError), v:
                    raise ConversionError("Invalid datetime data", v)
        return value.date()

    def _toFormValue(self, value):
        if value:
            try:
                value = value.strftime(self.date_format)
            except ValueError:
                return value
        return value


class FormattedDateDisplayWidget(DateDisplayWidget):
    """A date widget that supports different (and _explicit_) date formats.

    This is a display widget.

    It can also be used for displaying datetimes. If used to display a
    datetime (not a date), the widget returns local datetime with
    timezone set according to KofaUtils.
    """
    date_format = '%Y-%m-%d'
    show_year = False

    implements(IDisplayWidget)

    def __init__(self, context, request, *args, **kw):
        # try to grab date_format and show_year from bound schema field.
        date_format = getattr(context, 'date_format', self.date_format)
        if date_format is not None:
            self.date_format = date_format
        self.show_year = getattr(context, 'show_year', self.show_year)
        return super(FormattedDateDisplayWidget, self).__init__(
            context, request, *args, **kw)

    def __call__(self):
        if self._renderedValueSet():
            content = self._data
        else:
            content = self.context.default
        if content == self.context.missing_value:
            return ""
        if isinstance(content, datetime):
            # shift value to local timezone
            tz = pytz.utc
            utils = queryUtility(IKofaUtils)
            if utils is not None:
                tz = utils.tzinfo
            content = to_timezone(content, tz)
        try:
            content = content.strftime(self.date_format)
        except ValueError:
            return None
        return renderElement("span", contents=escape(content),
                             cssClass=self.cssClass)

class DateLEWidget(FormattedDateWidget):
    date_format = '%d/%m/%Y'

class DateDEWidget(FormattedDateWidget):
    date_format = '%d.%m.%Y'

class DateUSWidget(FormattedDateWidget):
    date_format = '%m/%d/%Y'

class DateLEDisplayWidget(FormattedDateDisplayWidget):
    date_format = '%d/%m/%Y'

class DateDEDisplayWidget(FormattedDateDisplayWidget):
    date_format = '%d.%m.%Y'

class DateUSDisplayWidget(FormattedDateDisplayWidget):
    date_format = '%m/%d/%Y'

def FriendlyDateWidget(format):
    """Get a friendly date input widget for `format`.

    This widget is suitable for edit and add forms.

    Valid `format` values are the keys of `DATE_FORMATS`
    dict. Default is ``le`` (little endian; DD/MM/YYYY).

    Friendly date widgets are rendered with a specialized CSS tag for
    enabling JavaScript datepickers.
    """
    css_class, date_format = DATE_FORMATS.get(format, DATE_FORMATS['le'])
    return CustomWidgetFactory(
        FormattedDateWidget,
        cssClass=css_class,
        date_format=date_format)

def FriendlyDateDisplayWidget(format):
    """Get a friendly date display widget for `format`.

    This widget is suitable for display forms.

    Valid `format` values are the keys of `DATE_FORMATS`
    dict. Default is ``le`` (little endian; DD/MM/YYYY).

    This widget is not rendered with a specialized CSS tag for
    enabling JavaScript datepickers. `css_class` is ignored which means
    there is nor difference between e.g. ``le`` and ``le-year``.`
    """
    css_class, date_format = DATE_FORMATS.get(format, DATE_FORMATS['le'])
    return CustomWidgetFactory(
        FormattedDateDisplayWidget,
        date_format=date_format)

def FriendlyDatetimeDisplayWidget(format):
    """Get a friendly datetime display widget for `format`.

    This widget is suitable for display forms.

    Valid `format` values are the keys of `DATE_FORMATS`
    dict. Default is ``le`` (little endian; DD/MM/YYYY %H:%M:%S).

    This widget is not rendered with a specialized CSS tag for
    enabling JavaScript datepickers. `css_class` is ignored which means
    there is no difference between e.g. ``le`` and ``le-year``.`
    """
    css_class, date_format = DATE_FORMATS.get(format, DATE_FORMATS['le'])
    datetime_format = date_format + ' %H:%M:%S'
    return CustomWidgetFactory(
        FormattedDateDisplayWidget,
        date_format=datetime_format)
