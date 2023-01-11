## $Id: test_converters.py 16818 2022-02-21 06:21:10Z henrik $
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
Tests for converterts.
"""
import datetime
import shutil
import tempfile
import unittest
from zope import schema
from zope.component import provideUtility
from zope.component.factory import Factory
from zope.component.hooks import clearSite
from zope.component.interfaces import IFactory
from zope.formlib import form
from zope.interface import (
    Interface, implements, invariant, Invalid, implementedBy, verify)

from waeup.kofa.app import University
from waeup.kofa.testing import FunctionalLayer, FunctionalTestCase
from waeup.kofa.interfaces import (
    SimpleKofaVocabulary, SubjectSource, GradeSource, IFieldConverter,
    DELETION_MARKER, IGNORE_MARKER)
from waeup.kofa.schoolgrades import ResultEntryField
from waeup.kofa.utils.converters import (
    IObjectConverter, DefaultFieldConverter, ListFieldConverter,
    PhoneNumberFieldConverter, ResultEntryConverter, DefaultObjectConverter)
from waeup.kofa.utils.helpers import attrs_to_fields

colors = SimpleKofaVocabulary(
    ('Red', u'red'),
    ('Green', u'green'),
    ('Blue', u'blue'),
    )
car_nums = SimpleKofaVocabulary(
    ('None', 0),
    ('One', 1),
    ('Two', 2),
    ('Three', 3),
    )


class IContact(Interface):
    """Sample interface for sample content type used here in tests.
    """
    name = schema.TextLine(
        title=u'Name',
        default=u'Manfred',
        readonly=True,
        )
    age = schema.Int(
        title=u'Age',
        default=23,
        required=True,
        )
    city = schema.TextLine(
        title=u'City',
        required=True,
        )
    vip = schema.Bool(
        title=u'Celebrity',
        default=False,
        required=True,
        )
    birthday = schema.Date(
        title=u'Birthday',
        default=None,
        )
    fav_color = schema.Choice(
        title=u'Favourite color',
        default=u'red',
        vocabulary=colors,
        )
    num_cars = schema.Choice(
        title=u'Number of cars owned',
        default=None,
        vocabulary=car_nums,
        )
    grades = schema.List(
        title=u'School Grades',
        value_type=ResultEntryField(),
        required=True,
        defaultFactory=list
        )
    fav_colors = schema.List(
        title=u'Favourite colors',
        value_type=schema.Choice(
            vocabulary=colors
            ),
        required=True,
        defaultFactory=list
        )
    friends = schema.List(
        title=u'Friends',
        value_type=schema.TextLine(
            title=u'Name',
            )
        )

    @invariant
    def kevinIsYoung(contact):
        if contact.age > 16 and contact.name == 'Kevin':
            raise Invalid('Kevins are age 16 or below.')


class Contact(object):
    """Sample content type.
    """
    implements(IContact)
Contact = attrs_to_fields(Contact)

form_fields_select = form.Fields(IContact).select('name', 'vip')
form_fields_omit = form.Fields(IContact).omit('name', 'vip')


class TestContacts(unittest.TestCase):
    # make sure the Contact class inhere works as expected

    def test_default_lists_not_shared(self):
        # 'grades' is a Contact property with empty list as default.
        # Ensure lists are unique if set as default this test fails if
        # `default` is set to empty list in interface.
        c1 = Contact()
        c2 = Contact()
        self.assertTrue(c1.grades is not c2.grades)


class FieldConverterTests(unittest.TestCase):

    def test_iface(self):
        # make sure we fullfill interface contracts
        obj1 = DefaultFieldConverter(None)
        obj2 = ListFieldConverter(None)
        obj3 = PhoneNumberFieldConverter(None)
        obj4 = ResultEntryConverter(None)
        verify.verifyObject(IFieldConverter, obj1)
        verify.verifyObject(IFieldConverter, obj2)
        verify.verifyObject(IFieldConverter, obj3)
        verify.verifyObject(IFieldConverter, obj4)
        verify.verifyClass(IFieldConverter, DefaultFieldConverter)
        verify.verifyClass(IFieldConverter, ListFieldConverter)
        verify.verifyClass(IFieldConverter, PhoneNumberFieldConverter)
        verify.verifyClass(IFieldConverter, ResultEntryConverter)
        return


class ConverterTests(FunctionalTestCase):

    layer = FunctionalLayer

    def setUp(self):
        super(ConverterTests, self).setUp()

        # Setup a sample site for each test
        app = University()
        self.dc_root = tempfile.mkdtemp()
        app['datacenter'].setStoragePath(self.dc_root)

        # Prepopulate the ZODB...
        self.getRootFolder()['app'] = app
        self.app = self.getRootFolder()['app']

        self.workdir = tempfile.mkdtemp()

        # Create a factory for contacts and register it as global utility
        factory = Factory(Contact)
        provideUtility(factory, IFactory, 'contact')
        return

    def tearDown(self):
        super(ConverterTests, self).tearDown()
        shutil.rmtree(self.workdir)
        shutil.rmtree(self.dc_root)
        clearSite()
        return

    def test_iface(self):
        # make sure we fullfill interface contracts
        obj = DefaultObjectConverter(IContact)
        verify.verifyObject(IObjectConverter, obj)
        verify.verifyClass(IObjectConverter, DefaultObjectConverter)
        return

    def test_valid_data(self):
        contact = Contact()
        contact.age = 33
        input_data = dict(name='  Rudi    ', age=' 99 ')
        converter = IObjectConverter(IContact)  # a converter to IContact
        err, inv_err, data = converter.fromStringDict(
            input_data, contact)
        assert data['name'] == 'Rudi'
        assert data['age'] == 99
        return

    def test_bool(self):
        contact1 = Contact()
        contact2 = Contact()
        input_data1 = dict(vip='on')
        input_data2 = dict(vip='')
        converter = IObjectConverter(IContact)  # a converter to IContact
        err1, inv_err1, data1 = converter.fromStringDict(
            input_data1, contact1)
        err2, inv_err2, data2 = converter.fromStringDict(
            input_data2, contact2)
        assert data1['vip'] is True
        assert data2['vip'] is False

    def test_bool_nonstandard_values1(self):
         # We accept 'true', 'True', 'tRuE', 'faLSE' and similar.
        contact1 = Contact()
        contact2 = Contact()
        input_data1 = dict(vip='True')
        input_data2 = dict(vip='false')
        converter = IObjectConverter(IContact)  # a converter to IContact
        err1, inv_err1, data1 = converter.fromStringDict(
            input_data1, contact1)
        err2, inv_err2, data2 = converter.fromStringDict(
            input_data2, contact2)
        assert data1['vip'] is True
        assert data2['vip'] is False

    def test_bool_nonstandard_values2(self):
        # We accept '1' and '0' as bool values.
        contact1 = Contact()
        contact2 = Contact()
        input_data1 = dict(vip='1')
        input_data2 = dict(vip='0')
        converter = IObjectConverter(IContact)  # a converter to IContact
        err1, inv_err1, data1 = converter.fromStringDict(
            input_data1, contact1)
        err2, inv_err2, data2 = converter.fromStringDict(
            input_data2, contact2)
        assert data1['vip'] is True
        assert data2['vip'] is False

    def test_bool_nonstandard_values3(self):
        # We accept 'yEs', 'no' and similar as bool values.
        contact1 = Contact()
        contact2 = Contact()
        input_data1 = dict(vip='Yes')
        input_data2 = dict(vip='no')
        converter = IObjectConverter(IContact)  # a converter to IContact
        err1, inv_err1, data1 = converter.fromStringDict(
            input_data1, contact1)
        err2, inv_err2, data2 = converter.fromStringDict(
            input_data2, contact2)
        assert data1['vip'] is True
        assert data2['vip'] is False

    def test_int(self):
        contact = Contact()
        input_data = dict(age='99')
        converter = IObjectConverter(IContact)  # a converter to IContact
        err, inv_err, data = converter.fromStringDict(
            input_data, contact)
        assert data['age'] == 99
        return

    def test_int_invalid(self):
        contact = Contact()
        input_data = dict(age='sweet sixteen')
        converter = IObjectConverter(IContact)  # a converter to IContact
        err, inv_err, new_contact = converter.fromStringDict(
            input_data, contact)
        self.assertEqual(err, [('age', u'Invalid integer data')])
        return

    def test_textline(self):
        contact = Contact()
        input_data = dict(name=' Rudi     ')
        converter = IObjectConverter(IContact)  # a converter to IContact
        err, inv_err, data = converter.fromStringDict(
            input_data, contact)
        self.assertEqual(data['name'], u'Rudi')
        assert isinstance(data['name'], unicode)
        return

    def test_invariant(self):
        contact = Contact()
        input_data = dict(name='Kevin', age='22')
        converter = IObjectConverter(IContact)  # a converter to IContact
        err, inv_err, new_contact = converter.fromStringDict(
            input_data, contact)
        self.assertEqual(inv_err, ['Kevins are age 16 or below.'])
        return

    def test_date(self):
        contact = Contact()
        converter = IObjectConverter(IContact)  # a converter to IContact

        # The input format for dates: YYYY-MM-DD
        err, inv_err, data = converter.fromStringDict(
            dict(birthday='1945-12-23'), contact)
        assert data['birthday'] == datetime.date(1945, 12, 23)
        assert isinstance(data['birthday'], datetime.date)

        err, inv_err, data = converter.fromStringDict(
            dict(birthday='1945-23-12'), contact)
        #assert data['birthday'] == datetime.date(1945, 12, 23)
        assert err[0][1] == 'Invalid datetime data'

        # '08' is not interpreted as octal number
        err, inv_err, data = converter.fromStringDict(
            dict(birthday='1945-12-08'), contact)
        assert data['birthday'] == datetime.date(1945, 12, 8)
        return

    def test_date_invalid(self):
        contact = Contact()
        converter = IObjectConverter(IContact)  # a converter to IContact
        err, inv_err, data = converter.fromStringDict(
            dict(birthday='not-a-date'), contact)
        self.assertEqual(err, [('birthday', u'Invalid datetime data')])

    def test_inject_formfields_select(self):
        # We can use our own formfields and select only a subset of fields
        contact = Contact()
        converter = IObjectConverter(IContact)  # a converter to IContact
        input_data = dict(name='Bruno', age='99', vip='on')
        err, inv_err, data = converter.fromStringDict(
            input_data, contact, form_fields=form_fields_select)
        self.assertEqual(data['name'], 'Bruno')
        assert 'age' not in data.keys()
        assert data['vip'] is True
        return

    def test_inject_formfields_omit(self):
        # We can use our own formfields and omit some fields
        contact = Contact()
        converter = IObjectConverter(IContact)  # a converter to IContact
        input_data = dict(name='Bruno', age='99', vip='on')
        err, inv_err, data = converter.fromStringDict(
            input_data, contact, form_fields=form_fields_omit)
        self.assertEqual(data['age'], 99)
        assert 'name' not in data.keys()
        assert 'vip' not in data.keys()
        return

    def test_factory(self):
        # We can use factories to convert values
        converter = IObjectConverter(IContact)  # a converter to IContact
        # pass string ``contact`` instead of a real object
        err, inv_err, data = converter.fromStringDict(
            dict(name='  Gabi  ', age='23  '), 'contact')
        self.assertEqual(data['age'], 23)
        self.assertEqual(data['name'], u'Gabi')
        return

    def test_choice_vocab(self):
        # We can handle vocabularies
        converter = IObjectConverter(IContact)  # a converter to IContact
        err, inv_err, data = converter.fromStringDict(
            dict(fav_color='blue'), 'contact')
        assert data['fav_color'] == u'blue'
        assert isinstance(data['fav_color'], unicode)
        return

    def test_choice_vocab_invalid_value(self):
        # We can handle vocabularies
        converter = IObjectConverter(IContact)  # a converter to IContact
        err, inv_err, data = converter.fromStringDict(
            dict(fav_color='magenta'), 'contact')
        self.assertEqual(err, [('fav_color', u'Invalid value')])
        assert 'fav_color' not in data.keys()
        return

    def test_non_string_choice(self):
        # We can handle vocabs with non-string values
        converter = IObjectConverter(IContact)  # a converter to IContact
        err, inv_err, data = converter.fromStringDict(
            dict(num_cars='1'), 'contact')
        assert data['num_cars'] == 1
        return

    def test_list_of_textlines(self):
        # We can convert lists of text lines
        converter = IObjectConverter(IContact)
        err, inv_err, data = converter.fromStringDict(
            {"friends": "['Fred', 'Wilma']"}, 'contact')
        self.assertEqual(
            data, {'friends': ['Fred', 'Wilma']})
        return

    def test_list_of_resultentries(self):
        # We can handle lists of result entries
        converter = IObjectConverter(IContact)
        # get currently valid values
        s_src, g_src = SubjectSource(), GradeSource()
        s_val1, s_val2 = list(s_src.factory.getValues())[0:2]
        g_val1, g_val2 = list(g_src.factory.getValues())[0:2]
        req_string = u"[('%s', '%s'), ('%s', '%s')]" % (
            s_val1, g_val1, s_val2, g_val2)
        err, inv_err, data = converter.fromStringDict(
            {"grades": req_string,
             },
            'contact')
        result_grades = data['grades']
        self.assertTrue(isinstance(result_grades, list))
        self.assertEqual(len(result_grades), 2)
        self.assertEqual(result_grades[0].subject, s_val1)
        self.assertEqual(result_grades[0].grade, g_val1)
        return

    def test_list_of_choices(self):
        # We cannot handle lists of choices because we are using
        # a widget which is not yet supported.
        converter = IObjectConverter(IContact)
        err, inv_err, data = converter.fromStringDict(
            {"fav_colors": "['red', 'green']"}, 'contact')
        self.assertEqual(
            data, {})
        return

    def test_ignore_values(self):
        # in update mode we ignore marked values
        converter = IObjectConverter(IContact)
        err, inv_err, data = converter.fromStringDict(
            {"friends": IGNORE_MARKER},
            Contact(),
            mode='update')
        # the ignored key/value are not part of the result
        self.assertEqual(data, {})
        return

    def test_delete_values(self):
        # in update mode we delete values marked accordingly
        # 'deleting' means setting to missing_value or to default if required.
        converter = IObjectConverter(IContact)
        err, inv_err, data = converter.fromStringDict(
            {"grades": DELETION_MARKER,
             "friends": DELETION_MARKER},
            'contact', mode='update')
        # grades are about to be set to default, friends to None
        self.assertEqual(data, {'grades': [], 'friends': None})
        return
