## $Id: interfaces.py 12110 2014-12-02 06:43:10Z henrik $
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
from zope import schema
from zope.schema.interfaces import IDate, ITextLine

class IFormattedDate(IDate):
    """A formatted date.

    Basically a zope.schema.IDate, but with optional additional
    attributes. These attributes _can_ be used by widgets to change
    the way of editing or displaying a date.

    The waeup.kofa.widgets.datewidget.FormattedDateWidget is a widget
    that supports these additional attributes.
    """
    show_year = schema.Bool(
        title = u'Show year selector when editing this date?',
        default = False,
        )
    date_format = schema.ASCII(
        title = u'A date format string suitable for use with strftime.',
        default = '%Y-%m-%d',
        )

class IPhoneNumber(ITextLine):
    """A phone number.
    """
