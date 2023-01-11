## $Id: datetimewidget.py 12110 2014-12-02 06:43:10Z henrik $
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
"""Datetimewidgets that are compatible with pytz.
"""
import datetime
import pytz
from zope.component import queryUtility
from zope.datetime import parseDatetimetz
from zope.datetime import DateTimeError
from zope.formlib.i18n import _
from zope.formlib.interfaces import ConversionError
from zope.formlib.textwidgets import DatetimeWidget
from waeup.kofa.utils.helpers import to_timezone
from waeup.kofa.interfaces import IKofaUtils

class _DummyUtils(object):
    tzinfo = pytz.utc

# A fallback, if no IKofaUtils can be found
_DUMMY_UTILS = _DummyUtils()

class PytzDatetimeWidget(DatetimeWidget):
    """pytz-conform, non-ambigous UTC datetimes.

    While the standard formlib datetime widget makes use of
    zope.datetime and creates also not too reliable (or ambigous)
    datetimes based on local servertime, this widget provides
    non-ambigous UTC datetimes with a pytz timezone (pytz.utc).

    Using this widget for datetime data we always get clean UTC
    datetimes compatible with other Python packages (as pytz is more
    wide-spread than zope.datetime).

    For datetimes in other timezones we compute the correct UTC value
    and store this. A way to help making sure, only UTC-based values
    go into the DB.

    For datetimes without any timezone set, we interpret the input to
    be meant as local app-time. I.e. if application TZ is
    ``Africa/Lagos``, we assume that a string like '2012-02-01 12:13'
    (apparently not providing TZ info) was meant as 12:13 h Lagos
    time.

    From zope.datetime, however, we save the parser abilities to
    interpret even bizarre entered data as some datetime.
    """
    def _toFieldValue(self, string):
        """Turn string into a UTC-based datetime.

        The TZ data is guaranteed to be pytz.utc.

        """
        # In import files we can use the hash symbol at the end of a
        # datetime and date strings to avoid annoying automatic date
        # transformation by Excel or Calc.
        string = string.strip('#')
        if string == self._missing:
            return self.context.missing_value
        else:
            try:
                # Different to original implementation we do not
                # automatically request local server time if no TZ was
                # set in `string`. In this case we want a datetime with
                # tzinfo set to `None` instead.
                value = parseDatetimetz(string, local=False)
            except (DateTimeError, ValueError, IndexError), v:
                raise ConversionError(_("Invalid datetime data"), v)

        if not isinstance(value, datetime.datetime):
            return value
        if value.tzinfo is None:
            utils = queryUtility(IKofaUtils, default=_DUMMY_UTILS)
            value = utils.tzinfo.localize(value)
        return value.astimezone(pytz.utc)
