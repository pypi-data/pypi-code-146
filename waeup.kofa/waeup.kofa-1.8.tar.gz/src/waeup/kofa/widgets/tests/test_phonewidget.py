## $Id: test_phonewidget.py 8168 2012-04-16 06:51:20Z uli $
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
Tests for PhoneWidget.

Most tests are reimplementation of similar tests in zope.formlib.
"""
from zope import schema
from zope.component import getGlobalSiteManager
from zope.formlib import form
from zope.formlib.tests.test_functional_textwidget import(
    FunctionalWidgetTestCase, patternExists)
from zope.formlib.textwidgets import TextWidget
from zope.interface import Interface, implements
from zope.publisher.browser import TestRequest
from zope.schema.interfaces import ITextLine
from waeup.kofa.widgets.phonewidget import PhoneWidget

# Dummy content
class ISampleContent(Interface):
    foo = schema.TextLine(
        title = u'Phone',
        description = u'Phone number',
        required = True,
        default=u'+234-1-1')

    bar = schema.TextLine(
        title = u'Phone',
        description = u'Phone number (not required)',
        required = False,
        missing_value = u'')

    baz = schema.TextLine(
        title = u'Phone',
        description = u'Required phone with a default',
        required = False,
        #default=u'+234--'
        )

class SampleContent:
    implements(ISampleContent)

    def __init__(self):
        self.foo = None
        self.bar = 'bar'
        self.baz = None

class SampleForm(form.EditForm):
    form_fields = form.fields(ISampleContent)
    form_fields['foo'].custom_widget = PhoneWidget
    form_fields['bar'].custom_widget = PhoneWidget
    form_fields['baz'].custom_widget = PhoneWidget

class PhoneWidgetTests(FunctionalWidgetTestCase):

    widgets = [
        (ITextLine, TextWidget),
        (ITextLine, TextWidget),
        (ITextLine, TextWidget),
        ]

    def test_display_editform(self):
        content = SampleContent()
        request = TestRequest()
        html = SampleForm(content, request)()
        # foo.country, foo.area and foo.ext exist
        self.assert_(patternExists(
            '<select .* name="form.foo.country".*>', html))
        self.assert_(patternExists(
            '<input .* name="form.foo.area".* value="".*>', html))
        self.assert_(patternExists(
            '<input .* name="form.foo.ext".* value="".*>', html))
        return

    def test_submit_editform(self):
        # we can submit an edit form
        content = SampleContent()
        request = TestRequest()

        # submit edit view
        request.form['form.foo.country'] = u'+123'
        request.form['form.foo.area'] = u'456'
        request.form['form.foo.ext'] = u'7890'
        request.form['form.actions.apply'] = u''
        SampleForm(content, request)()

        # check new values in object
        self.assertEqual(content.foo, u'+123-456-7890')
        return

    def test_invalid_type(self):
        # there is no invalid type for textline-based input
        content = SampleContent()
        request = TestRequest()

        # submit invalid type for text line
        request.form['form.foo.country'] = '+123'
        request.form['form.foo.area'] = '456'
        request.form['form.foo.ext'] = '7890'
        request.form['form.actions.apply'] = u''
        html = SampleForm(content, request)()

        # We don't have a invalid field value
        # since we convert the value to unicode
        self.assert_('Object is of wrong type.' not in html)
        return

    def test_missing_value(self):
        content = SampleContent()
        request = TestRequest()

        request.form['form.foo.country'] = u'+123'
        request.form['form.foo.area'] = u'456'
        request.form['form.foo.ext'] = u'7890'
        request.form['form.bar.country'] = u''
        request.form['form.bar.area'] = u''
        request.form['form.bar.ext'] = u''
        request.form['form.baz.country'] = u''
        request.form['form.baz.area'] = u''
        request.form['form.baz.ext'] = u''
        request.form['form.actions.apply'] = u''

        SampleForm(content, request)()

        # check new values in object
        self.assertEqual(content.foo, u'+123-456-7890')
        self.assertEqual(content.bar, u'') # default missing value
        self.assertEqual(content.baz, None)
        return

    def test_partial_values(self):
        # make sure partial numbers will not be enough
        # XXX: we have to test each single field alone as an error
        #      in one field will stop setting the other ones.
        content = SampleContent()
        request = TestRequest()

        request.form['form.foo.country'] = u'+123'
        request.form['form.foo.area'] = u'456'
        request.form['form.foo.ext'] = u''
        request.form['form.bar.country'] = u'+123'
        request.form['form.bar.area'] = u'12'
        request.form['form.bar.ext'] = u'789'
        request.form['form.baz.country'] = u'+123'
        request.form['form.baz.area'] = u'456'
        request.form['form.baz.ext'] = u'789'
        request.form['form.actions.apply'] = u''

        SampleForm(content, request)()

        # check new values in object
        # as there were errors in the form, no value was set at all
        self.assertEqual(content.foo, None)
        self.assertEqual(content.bar, 'bar')
        self.assertEqual(content.baz, None)
        return

    def test_no_values(self):
        # if the last two subfields contain no value, no phone will be set
        content = SampleContent()
        request = TestRequest()

        request.form['form.bar.country'] = u'+123'
        request.form['form.bar.area'] = u''
        request.form['form.bar.ext'] = u''
        request.form['form.baz.country'] = u'+124'
        request.form['form.baz.area'] = u''
        request.form['form.baz.ext'] = u''
        request.form['form.actions.apply'] = u''

        SampleForm(content, request)()

        # check new values in object
        self.assertEqual(content.bar, u'') # default missing value
        self.assertEqual(content.baz, None)
        return
