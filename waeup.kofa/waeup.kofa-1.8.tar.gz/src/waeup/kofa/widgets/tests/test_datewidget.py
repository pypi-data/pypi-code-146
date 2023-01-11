## $Id: test_datewidget.py 9499 2012-11-02 02:19:06Z uli $
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
"""Formatted Date widget tests.
"""
import datetime
import unittest
import doctest
from zope.schema import Date
from zope.interface import Interface, implementer
from zope.interface.verify import verifyClass
from zope.publisher.browser import TestRequest

from zope.formlib.tests.test_browserwidget import (
    SimpleInputWidgetTest, BrowserWidgetTest, )
from zope.formlib.interfaces import IInputWidget, IDisplayWidget
from waeup.kofa.widgets.datewidget import (
    FormattedDateWidget, FormattedDateDisplayWidget, )
from zope.formlib.widgets import DateI18nWidget
from zope.formlib.interfaces import ConversionError, WidgetInputError


class FormattedDateWidgetTest(SimpleInputWidgetTest):
    """Documents and tests the formatted date widget.

        >>> verifyClass(IInputWidget, FormattedDateWidget)
        True
    """

    _FieldFactory = Date
    _WidgetFactory = FormattedDateWidget

    def setUpContent(self, desc=u'', title=u'Foo Title'):
        # same as in base class but with a min value of date(1910, 1, 1)
        field = self._FieldFactory(
            __name__='foo', title=title, description=desc,
            min=datetime.date(1910, 1, 1))
        class ITestContent(Interface):
            foo = field
        @implementer(ITestContent)
        class TestObject:
            pass
        self.content = TestObject()
        field = ITestContent['foo']
        self.field = field.bind(self.content)
        request = TestRequest(HTTP_ACCEPT_LANGUAGE='ru')
        request.form['field.foo'] = u'Foo Value'
        self._widget = self._WidgetFactory(field, request)

    def testRender(self):
        super(FormattedDateWidgetTest, self).testRender(
            datetime.date(2003, 3, 26),
            ('type="text"', 'id="field.foo"', 'name="field.foo"',
                'value="2003-03-26"'))

    def testRenderCustomFormat(self):
        self._widget.date_format = "%d/%m/%y"
        super(FormattedDateWidgetTest, self).testRender(
            datetime.datetime(2004, 3, 26, 12, 58, 59),
            ('type="text"', 'id="field.foo"', 'name="field.foo"',
                'value="26/03/04"'))

    def testProperties(self):
        self.assertEqual(self._widget.tag, 'input')
        self.assertEqual(self._widget.type, 'text')
        # By default the date format is ISO and the rendered CSS 'datepicker'
        self.assertEqual(self._widget.cssClass, 'datepicker')
        self.assertEqual(self._widget.extra, '')

    def test_hasInput(self):
        del self._widget.request.form['field.foo']
        self.assertFalse(self._widget.hasInput())
        self._widget.request.form['field.foo'] = u''
        self.assertTrue(self._widget.hasInput())
        self._widget.request.form['field.foo'] = u'2003-03-26'
        self.assertTrue(self._widget.hasInput())

    def test_getDefaultInputValue(self,
            value=u'2004-03-26',
            check_value=datetime.date(2004, 3, 26)):
        self._widget.request.form['field.foo'] = u''
        self.assertRaises(WidgetInputError, self._widget.getInputValue)
        self._widget.request.form['field.foo'] = value
        self.assertEquals(self._widget.getInputValue(), check_value)
        self._widget.request.form['field.foo'] = u'abc'
        self.assertRaises(ConversionError, self._widget.getInputValue)

    def test_getCustomInputValue_de(self):
        self._widget.date_format = "%d.%m.%y"
        self.test_getDefaultInputValue(u'26.03.04')

    def test_getCustomInputValue_de2(self):
        self._widget.date_format = "%d.%m.%Y"
        self.test_getDefaultInputValue(u'26.03.2004')

    def test_getCustomInputValue_us(self):
        self._widget.date_format = "%m/%d/%Y"
        self.test_getDefaultInputValue(u'03/26/2004')

    def test_minimal_value_respected(self):
        # we did set up the date field to require dates >= 1900-01-01
        request = TestRequest()
        # setting a date > 1900-01-01 is okay
        request.form['field.foo'] = '1912-03-27'
        widget = FormattedDateWidget(self.field, request)
        self.assertEqual(
            widget.getInputValue(), datetime.date(1912, 3, 27))

        # setting a date < 1900-01-01 will fail
        request.form['field.foo'] = '1812-03-27'
        widget = FormattedDateWidget(self.field, request)
        self.assertRaises(
            WidgetInputError,
            widget.getInputValue)
        # check the correct exception message
        try:
            widget.getInputValue()
        except WidgetInputError as exc:
            # just catch the exception
            pass
        exc = '%r' % exc  # turn exception into string
        self.assertEqual(
            exc,
            "WidgetInputError('foo', u'Foo Title', "
            "TooSmall(datetime.date(1812, 3, 27), datetime.date(1910, 1, 1)))"
            )
        return

class FormattedDateDisplayWidgetTest(BrowserWidgetTest):
    """The FormatterdDisplayDateWidget complies with IDisplayWidget.

        >>> verifyClass(IDisplayWidget, FormattedDateDisplayWidget)
        True
    """

    _WidgetFactory = FormattedDateDisplayWidget
    expected_class = "date"

    def setUp(self):
        super(FormattedDateDisplayWidgetTest, self).setUp()
        self._value = datetime.date(2004, 12, 01)

    def testDefaultDisplayStyle(self):
        self.assertFalse(self._widget.displayStyle)

    def testRenderDefault(self):
        self._widget.setRenderedValue(self._value)
        self.verifyResult(self._widget(),
                          ["<span",
                           'class="%s"' % self.expected_class,
                           "2004-12-01",
                           "</span"])

    def testRenderCustom(self):
        self._widget.setRenderedValue(self._value)
        self._widget.date_format = '%m/%d/%Y'
        self.verifyResult(self._widget(),
                          ["<span",
                           'class="%s"' % self.expected_class,
                           "12/01/2004",
                           "</span"])

    def testRenderNone(self):
        self._widget.setRenderedValue(None)
        self._widget.date_format = '%m/%d/%Y'
        self.assertEqual(self._widget(), '')

    def testNoValueSet(self):
        self._widget.date_format = '%m/%d/%Y'
        self.assertEqual(self._widget(), '')

def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(FormattedDateWidgetTest),
        unittest.makeSuite(FormattedDateDisplayWidgetTest),
        doctest.DocTestSuite(),
        ))

