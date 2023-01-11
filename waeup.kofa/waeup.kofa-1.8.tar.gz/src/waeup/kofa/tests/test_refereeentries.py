# Tests for schoolgrades module.
import unittest
from zope.component import getGlobalSiteManager
from zope.interface.verify import verifyObject, verifyClass
from zope.schema.interfaces import ConstraintNotSatisfied, WrongType
from waeup.kofa.interfaces import (
    IRefereeEntry, IRefereeEntryField, IKofaUtils, NotAnEmailAddress)
from waeup.kofa.refereeentries import RefereeEntry, RefereeEntryField
from waeup.kofa.utils.utils import KofaUtils


class RefereeEntryTests(unittest.TestCase):

    def setUp(self):
        self.valid_name = u'Otis Stone'
        self.valid_email = 'otis@stones.de'
        return

    def tearDown(self):
        return

    def test_ifaces(self):
        # make sure we implement the promised interfaces
        obj = RefereeEntry()
        verifyObject(IRefereeEntry, obj)
        verifyClass(IRefereeEntry, RefereeEntry)
        return

    def test_init(self):
        # we can pass initial values
        item1 = RefereeEntry()
        item2 = RefereeEntry(self.valid_name, self.valid_email)
        self.assertTrue(item1.name is None)
        self.assertTrue(item1.email is None)
        self.assertEqual(item2.name, self.valid_name)
        self.assertEqual(item2.email, self.valid_email)
        self.assertFalse(item1.email_sent)
        self.assertFalse(item2.email_sent)
        return

    def test_illegal_value(self):
        # we do not accept wrong values
        item = RefereeEntry()
        self.assertRaises(
            WrongType, RefereeEntry, 'invalid', 'invalid')
        self.assertRaises(
            WrongType, RefereeEntry, 'invalid')
        self.assertRaises(
            WrongType, setattr, item, 'name', 99)
        self.assertRaises(
            NotAnEmailAddress, setattr, item, 'email', 'blah')
        return

    def test_to_string(self):
        # the string representation is handy for export
        item1 = RefereeEntry()
        item2 = RefereeEntry(self.valid_name, self.valid_email)
        self.assertEqual(item1.to_string(), u"(None, None, False)")
        self.assertEqual(item2.to_string(), u"(u'%s', '%s', False)" % (
            self.valid_name, self.valid_email))
        return

    def test_from_string(self):
        # we can create new result entries based on strings
        myinput = u"(u'%s','%s',True)" % (
            self.valid_name, self.valid_email)
        item1 = RefereeEntry.from_string(myinput)
        item2 = RefereeEntry.from_string(u"(u'','',999)")
        item3 = RefereeEntry.from_string(u"(None, None, False)")
        self.assertEqual(item1.name, self.valid_name)
        self.assertEqual(item1.email, self.valid_email)
        self.assertTrue(item1.email_sent is True)
        self.assertTrue(item2.name is None)
        self.assertTrue(item2.email is None)
        self.assertTrue(item2.email_sent is False)
        self.assertTrue(item3.name is None)
        self.assertTrue(item3.email is None)
        self.assertTrue(item3.email_sent is False)
        return

    def test_eq(self):
        # we can compare equality of RefereeEntry objects
        item1 = RefereeEntry(self.valid_name, self.valid_email)
        item2 = RefereeEntry(self.valid_name, self.valid_email)
        item3 = RefereeEntry()
        item4 = RefereeEntry()
        assert item1 is not item2
        assert item1 == item1
        assert item1 == item2
        assert item3 is not item4
        assert item3 == item4
        assert item1.__eq__(item2) is True
        assert item1.__eq__(item3) is False

    def test_ne(self):
        # we can also tell, which ResultEntries are _not_ equal
        item1 = RefereeEntry(self.valid_name, self.valid_email)
        item2 = RefereeEntry()
        assert item1 != item2
        assert item1.__ne__(item2) is True
        assert item1.__ne__(item1) is False


class RefereeEntryFieldTests(unittest.TestCase):

    def test_ifaces(self):
        # make sure we implement the promised interfaces.
        obj = RefereeEntryField()
        verifyObject(IRefereeEntryField, obj)
        verifyClass(IRefereeEntryField, RefereeEntryField)
        return
