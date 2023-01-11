## $Id: test_objectwidget.py 7819 2012-03-08 22:28:46Z henrik $
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
"""Tests for objectwidget.
"""
import doctest
import unittest
import sys
from zope.interface import Interface, implements
from zope.interface.verify import verifyClass
from zope.publisher.browser import TestRequest
from zope.schema import Object, TextLine
from zope.schema.interfaces import ITextLine
from zope.traversing.adapters import DefaultTraversable
from zope.traversing.interfaces import ITraversable
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope.component import provideAdapter

from zope.formlib.interfaces import (
    IInputWidget, IDisplayWidget,MissingInputError)
from zope.formlib.widgets import TextWidget, DisplayWidget
from zope.formlib.tests.test_browserwidget import BrowserWidgetTest
from zope.formlib.interfaces import IWidgetInputErrorView

from waeup.kofa.widgets.objectwidget import KofaObjectWidget as ObjectWidget
from waeup.kofa.widgets.objectwidget import (
    KofaObjectDisplayWidget as ObjectDisplayWidget)

class ITestContact(Interface):
    name = TextLine()
    email = TextLine()

class TestContact(object):
    implements(ITestContact)

class ITestContent(Interface):
    foo = Object(
        ITestContact,
        title = u'Foo Title',
        description = u'',
        )

class ObjectWidgetInputErrorView(object):
    implements(IWidgetInputErrorView)

    def __init__(self, error, request):
        self.error = error
        self.request = request

    def snippet(self):
        return repr(self.error)

class ObjectWidgetTest(BrowserWidgetTest):
    """Documents and tests the object widget.

        >>> from zope.interface.verify import verifyClass
        >>> verifyClass(IInputWidget, ObjectWidget)
        True
    """

    _FieldFactory = Object
    def _WidgetFactory(self, context, request, **kw):
        kw.update({'factory': TestContact})
        return ObjectWidget(context, request, **kw)

    def setUpContent(self, desc=u'', title=u'Foo Title'):
        provideAdapter(TextWidget, (ITextLine, IDefaultBrowserLayer),
                       IInputWidget)

        class TestObject(object):
            implements(ITestContent)

        self.content = TestObject()
        self.field = ITestContent['foo']
        self.request = TestRequest(HTTP_ACCEPT_LANGUAGE='pl')
        self.request.form['field.foo'] = u'Foo Value'
        self._widget = self._WidgetFactory(self.field, self.request)

    def setUp(self):
        super(ObjectWidgetTest, self).setUp()
        self.field = Object(ITestContact, __name__=u'foo')
        provideAdapter(TextWidget,
                       (ITextLine, IDefaultBrowserLayer),
                       IInputWidget)

    def test_applyChanges(self):
        self.request.form['field.foo.name'] = u'Foo Name'
        self.request.form['field.foo.email'] = u'foo@foo.test'
        widget = self._WidgetFactory(self.field, self.request)

        self.assertEqual(widget.applyChanges(self.content), True)
        self.assertEqual(hasattr(self.content, 'foo'), True)
        self.assertEqual(isinstance(self.content.foo, TestContact), True)
        self.assertEqual(self.content.foo.name, u'Foo Name')
        self.assertEqual(self.content.foo.email, u'foo@foo.test')

    def test_error(self):
        provideAdapter(
            ObjectWidgetInputErrorView,
            (MissingInputError, TestRequest),
            IWidgetInputErrorView)

        widget = self._WidgetFactory(self.field, self.request)
        self.assertRaises(MissingInputError, widget.getInputValue)
        error_html = widget.error()
        if sys.version_info < (2, 5):
            self.assertTrue("email: <zope.formlib.interfaces.Mis"
                             in error_html)
            self.assertTrue("name: <zope.formlib.interfaces.Miss"
                             in error_html)
        else:
            self.assertTrue(
                "email: MissingInputError(u'field.foo.email', u'', None)"
                in error_html)
            self.assertTrue(
                "name: MissingInputError(u'field.foo.name', u'', None)"
                in error_html)

    def test_applyChangesNoChange(self):
        self.content.foo = TestContact()
        self.content.foo.name = u'Foo Name'
        self.content.foo.email = u'foo@foo.test'

        self.request.form['field.foo.name'] = u'Foo Name'
        self.request.form['field.foo.email'] = u'foo@foo.test'
        widget = self._WidgetFactory(self.field, self.request)
        widget.setRenderedValue(self.content.foo)

        self.assertEqual(widget.applyChanges(self.content), False)
        self.assertEqual(hasattr(self.content, 'foo'), True)
        self.assertEqual(isinstance(self.content.foo, TestContact), True)
        self.assertEqual(self.content.foo.name, u'Foo Name')
        self.assertEqual(self.content.foo.email, u'foo@foo.test')

    def test_respect_custom_widgets(self):
        # We can use our own subwidgets when creating ObjectWidgets
        class CustomTextWidget(TextWidget):
            pass

        # We create a custom widget for the `name` field of ITestContact
        name_widget = CustomTextWidget(ITestContact['name'], self.request)

        # Custom widgets are passed by <fieldname>_widget keyword:
        widget = self._WidgetFactory(self.field, self.request,
                                     name_widget=name_widget)
        widget1, widget2 = widget.subwidgets()
        self.assertTrue(widget1 is name_widget)


class ObjectDisplayWidgetTest(BrowserWidgetTest):
    """Documents and tests the display variant of object widget.

        >>> from zope.interface.verify import verifyClass
        >>> verifyClass(IDisplayWidget, ObjectDisplayWidget)
        True

   """
    _FieldFactory = Object
    def _WidgetFactory(self, context, request, **kw):
        kw.update({'factory': TestContact})
        return ObjectDisplayWidget(context, request, **kw)

    def setUpContent(self, desc=u'', title=u'Foo Title'):
        provideAdapter(TextWidget, (ITextLine, IDefaultBrowserLayer),
                       IInputWidget)
        provideAdapter(DisplayWidget, (ITextLine, IDefaultBrowserLayer),
                       IDisplayWidget)
        # The widget must be traversable. We register the default
        # adapter that can turn nearly any object into an ITraversable.
        provideAdapter(DefaultTraversable, (None,), ITraversable)

        class TestObject(object):
            implements(ITestContent)

        self.content = TestObject()
        self.content.name = u'Foo Name'
        self.content.email = u'foo@foo.test'
        self.field = ITestContent['foo']
        self.request = TestRequest(HTTP_ACCEPT_LANGUAGE='pl')
        self.request.form['field.foo'] = u'Foo Value'
        self._widget = self._WidgetFactory(self.field, self.request)

    def setUp(self):
        super(ObjectDisplayWidgetTest, self).setUp()
        self.field = Object(ITestContact, __name__=u'foo')
        provideAdapter(TextWidget,
                       (ITextLine, IDefaultBrowserLayer),
                       IInputWidget)
        provideAdapter(DisplayWidget,
                       (ITextLine, IDefaultBrowserLayer),
                       IDisplayWidget)


    def test_interfaces(self):
        self.assertTrue(IDisplayWidget.providedBy(self._widget))
        self.assertFalse(IInputWidget.providedBy(self._widget))
        self.assertTrue(verifyClass(IDisplayWidget, ObjectDisplayWidget))

    def test_render(self):
        widget = ObjectDisplayWidget(
            self.field, self.request, TestContact)
        widget.setRenderedValue(self.content)

        check_list = [
            '<span',
            'Foo Name',
            '</span>', '<span',
            'foo@foo.test',
            '</span>']
        self.verifyResult(widget(), check_list, inorder=True)

def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(ObjectWidgetTest),
        unittest.makeSuite(ObjectDisplayWidgetTest),
        doctest.DocTestSuite(),
        ))

if __name__=='__main__':
    unittest.main(defaultTest='test_suite')
