# -*- coding: utf-8 -*-
import unittest
import grok
from zope.component import getUtility, queryUtility, createObject
from zope.catalog.interfaces import ICatalog
from waeup.kofa.students.interfaces import IStudentsUtils
from waeup.kofa.students.utils import formatted_text
from waeup.kofa.students.tests.test_browser import StudentsFullSetup

class FormatterTests(unittest.TestCase):

    def test_formatted_text(self):
        # we can format strings, unicode and things convertable to unicode.
        result1 = formatted_text('sample')
        result2 = formatted_text('ümlaut')
        result3 = formatted_text(3)
        result4 = formatted_text(u'unicöde')
        result5 = formatted_text(u'sample', color='red')
        self.assertTrue(isinstance(result1, unicode))
        self.assertEqual(
            result1, u'<font color="black">sample</font>')
        self.assertEqual(
            result2, u'<font color="black">ümlaut</font>')
        self.assertEqual(
            result3, u'<font color="black">3</font>')
        self.assertEqual(
            result4, u'<font color="black">unicöde</font>')
        self.assertEqual(
            result5, u'<font color="red">sample</font>')
        return

class StudentsUtilsTests(StudentsFullSetup):

    def test_setReturningData(self):
        utils = getUtility(IStudentsUtils)
        self.student['studycourse'].current_level = 600
        utils.setReturningData(self.student)
        # The new level exceeds the certificates end_level.
        # In this case current_level remains unchanged and no error is raised.
        self.assertEqual(self.student['studycourse'].current_level, 600)

    def test_setMatricNumber(self):
        site = grok.getSite()
        utils = getUtility(IStudentsUtils)
        # Matric number can't be set twice.
        msg, mnumber = utils.setMatricNumber(self.student)
        self.assertEqual(msg, 'Matriculation number already set.')
        self.assertEqual(mnumber, None)
        self.assertEqual(self.student.matric_number, '234')
        self.student.matric_number = None
        # Matric number can't be set if next_matric_integer is 0.
        msg, mnumber = utils.setMatricNumber(self.student)
        self.assertEqual(msg, 'Matriculation number cannot be set.')
        self.assertEqual(mnumber, None)
        site['configuration'].next_matric_integer = 1
        # Now all requirements are met and matric number can be set.
        msg, mnumber = utils.setMatricNumber(self.student)
        self.assertEqual(msg, None)
        self.assertEqual(mnumber, '1')
        self.assertEqual(self.student.matric_number, '1')
        self.assertEqual(site['configuration'].next_matric_integer, 2)
        # Student can be found in catalog with new matric number.
        cat = queryUtility(ICatalog, name='students_catalog')
        results = list(cat.searchResults(matric_number=('1', '1')))
        self.assertEqual(self.student,results[0])
        # Add another student.
        another_student = createObject('waeup.Student')
        another_student.matric_number = u'2'
        self.app['students'].addStudent(another_student)
        # Matric number can't be assigned twice.
        self.student.matric_number = None
        msg, mnumber = utils.setMatricNumber(self.student)
        self.assertEqual(msg, 'Matriculation number 2 exists.')
        self.assertEqual(mnumber, None)
        self.assertEqual(self.student.matric_number, None)
        # Certificate must be set.
        self.student.matric_number = None
        another_student.matric_number = u'999'
        self.student['studycourse'].certificate = None
        msg, mnumber = utils.setMatricNumber(self.student)
        self.assertEqual(msg, 'No certificate assigned.')
        return

    def test_set_payment_details(self):
        self.app['configuration']['2004'].gown_fee = 150.0
        self.app['configuration']['2004'].transcript_fee = 90.0
        self.app['configuration']['2004'].late_registration_fee = 180.0
        utils = getUtility(IStudentsUtils)
        error, payment = utils.setPaymentDetails(
            'combi',self.student, None, None,
            ['gown', 'transcript', 'late_registration'])
        self.assertEqual(payment.p_level, 100)
        self.assertEqual(payment.p_session, 2004)
        self.assertEqual(payment.amount_auth, 420.0)
        self.assertEqual(payment.p_item,
            u'Gown Hire Fee + Transcript Fee + Late Course Registration Fee')
        self.assertEqual(payment.p_combi,
            ['gown', 'transcript', 'late_registration'])
        return