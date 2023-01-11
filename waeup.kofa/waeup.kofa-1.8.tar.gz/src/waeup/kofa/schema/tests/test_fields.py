"""Tests for waeup.kofa.schema fields.
"""
import unittest
from zope.interface.verify import verifyClass, verifyObject
from zope.schema.interfaces import IDate
from waeup.kofa.schema import FormattedDate, PhoneNumber
from waeup.kofa.schema.interfaces import IFormattedDate, IPhoneNumber

class FormattedDateTests(unittest.TestCase):
    # Tests for FormattedDate field.

    def test_iface(self):
        # make sure we fullfill interface contracts
        obj = FormattedDate()
        verifyClass(IDate, FormattedDate)
        verifyClass(IFormattedDate, FormattedDate)
        verifyObject(IDate, obj)
        verifyObject(IFormattedDate, obj)
        return

    def test_defaults(self):
        # we get expected default values for dates.
        obj = FormattedDate()
        self.assertEqual(obj.show_year, False)
        self.assertEqual(obj.date_format, None)
        return

    def test_attribs(self):
        # we can set the promised attributes.
        obj = FormattedDate(show_year=True, date_format='%d.%m.%Y')
        self.assertEqual(obj.show_year, True)
        self.assertEqual(obj.date_format, '%d.%m.%Y')
        return

class PhoneNumberTests(unittest.TestCase):
    # Tests for PhoneNumber field
    def test_iface(self):
        # make sure we fullfill interface contracts
        obj = PhoneNumber()
        verifyClass(IPhoneNumber, PhoneNumber)
        verifyObject(IPhoneNumber, obj)
        return
