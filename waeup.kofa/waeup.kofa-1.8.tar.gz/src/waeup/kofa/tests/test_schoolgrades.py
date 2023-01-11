# Tests for schoolgrades module.
import unittest
from zope.component import getGlobalSiteManager
from zope.interface.verify import verifyObject, verifyClass
from zope.schema.interfaces import ConstraintNotSatisfied
from waeup.kofa.interfaces import IResultEntry, IResultEntryField, IKofaUtils
from waeup.kofa.schoolgrades import ResultEntry, ResultEntryField
from waeup.kofa.utils.utils import KofaUtils


class ResultEntryTests(unittest.TestCase):

    def setUp(self):
        self.utils = KofaUtils()
        self.gsm = getGlobalSiteManager()
        self.gsm.registerUtility(self.utils, IKofaUtils)
        self.valid_subj = self.utils.EXAM_SUBJECTS_DICT.keys()[0]
        self.valid_grade = self.utils.EXAM_GRADES[0][0]
        return

    def tearDown(self):
        self.gsm.unregisterUtility(self.utils)
        return

    def test_ifaces(self):
        # make sure we implement the promised interfaces.
        obj = ResultEntry()
        verifyObject(IResultEntry, obj)
        verifyClass(IResultEntry, ResultEntry)
        return

    def test_init(self):
        # we can pass initial values
        item1 = ResultEntry()
        item2 = ResultEntry(self.valid_subj, self.valid_grade)
        self.assertTrue(item1.subject is None)
        self.assertTrue(item1.grade is None)
        self.assertEqual(item2.subject, self.valid_subj)
        self.assertEqual(item2.grade, self.valid_grade)
        return

    def test_illegal_value(self):
        # we do not accept values not stored in KofaUtils
        item = ResultEntry()
        self.assertRaises(
            ConstraintNotSatisfied, ResultEntry, 'invalid', 'invalid')
        self.assertRaises(
            ConstraintNotSatisfied, ResultEntry, 'invalid')
        self.assertRaises(
            ConstraintNotSatisfied, setattr, item, 'subject', 'blah')
        self.assertRaises(
            ConstraintNotSatisfied, setattr, item, 'grade', 'blah')
        return

    def test_to_string(self):
        # the string representation is handy for export
        item1 = ResultEntry()
        item2 = ResultEntry(self.valid_subj, self.valid_grade)
        self.assertEqual(item1.to_string(), u"(None, None)")
        self.assertEqual(item2.to_string(), u"('%s', '%s')" % (
            self.valid_subj, self.valid_grade))
        return

    def test_from_string(self):
        # we can create new result entries based on strings
        myinput = u"(u'%s',u'%s')" % (
            self.valid_subj, self.valid_grade)
        item1 = ResultEntry.from_string(myinput)
        item2 = ResultEntry.from_string(u"(u'',u'')")
        item3 = ResultEntry.from_string(u"(None, None)")
        self.assertEqual(item1.subject, self.valid_subj)
        self.assertEqual(item1.grade, self.valid_grade)
        self.assertTrue(item2.subject is None)
        self.assertTrue(item2.grade is None)
        self.assertTrue(item3.subject is None)
        self.assertTrue(item3.grade is None)
        return

    def test_eq(self):
        # we can compare equality of ResultEntry objects
        item1 = ResultEntry(self.valid_subj, self.valid_grade)
        item2 = ResultEntry(self.valid_subj, self.valid_grade)
        item3 = ResultEntry()
        item4 = ResultEntry()
        assert item1 is not item2
        assert item1 == item1
        assert item1 == item2
        assert item3 is not item4
        assert item3 == item4
        assert item1.__eq__(item2) is True
        assert item1.__eq__(item3) is False

    def test_ne(self):
        # we can also tell, which ResultEntries are _not_ equal
        item1 = ResultEntry(self.valid_subj, self.valid_grade)
        item2 = ResultEntry()
        assert item1 != item2
        assert item1.__ne__(item2) is True
        assert item1.__ne__(item1) is False


class ResultEntryFieldTests(unittest.TestCase):

    def test_ifaces(self):
        # make sure we implement the promised interfaces.
        obj = ResultEntryField()
        verifyObject(IResultEntryField, obj)
        verifyClass(IResultEntryField, ResultEntryField)
        return
