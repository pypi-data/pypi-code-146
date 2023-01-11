import datetime
import os
import pytz
import shutil
import tempfile
import unittest
from zope.catalog.interfaces import ICatalog
from zope.component import queryUtility, getUtility, createObject
from zope.interface.verify import verifyObject, verifyClass
from zope.intid.interfaces import IIntIds
from waeup.kofa.applicants import ApplicantsContainer
from waeup.kofa.applicants.export import (
    ApplicantsContainerExporter, ApplicantExporter,
    ApplicantPaymentExporter)
from waeup.kofa.applicants.interfaces import (
    AppCatSource, ApplicationTypeSource)
from waeup.kofa.applicants.tests.test_batching import (
    ApplicantImportExportSetup)
from waeup.kofa.interfaces import ICSVExporter
from waeup.kofa.schoolgrades import ResultEntry
from waeup.kofa.testing import KofaUnitTestLayer, FunctionalLayer
from waeup.kofa.utils.utils import KofaUtils

class ApplicantsContainersExporterTest(unittest.TestCase):

    layer = KofaUnitTestLayer

    def setUp(self):
        self.workdir = tempfile.mkdtemp()
        self.outfile = os.path.join(self.workdir, 'myoutput.csv')
        return

    def tearDown(self):
        shutil.rmtree(self.workdir)
        return

    def test_ifaces(self):
        # make sure we fullfill interface contracts
        obj = ApplicantsContainerExporter()
        verifyObject(ICSVExporter, obj)
        verifyClass(ICSVExporter, ApplicantsContainerExporter)
        return

    def test_get_as_utility(self):
        # we can get a faculty exporter as utility
        result = queryUtility(ICSVExporter, name="applicantscontainers")
        self.assertTrue(result is not None)
        return

    def setup_container(self, container):
        # set all attributes of a container
        container.code = u'dp2017'
        container.title = u'General Studies'
        container.prefix = list(ApplicationTypeSource()(container))[0]
        container.year = 2017
        container.application_category = list(AppCatSource()(container))[0]
        container.description = u'Some Description\nwith linebreak\n'
        container.description += u'<<de>>man spriht deutsh'
        container.startdate = datetime.datetime(
            2017, 1, 1, 12, 0, 0, tzinfo=pytz.utc)
        container.enddate = datetime.datetime(
            2017, 1, 31, 23, 0, 0, tzinfo=pytz.utc)
        return container

    def test_export(self):
        # we can export a set of applicants containers (w/o applicants)
        container = ApplicantsContainer()
        container = self.setup_container(container)
        exporter = ApplicantsContainerExporter()
        exporter.export([container], self.outfile)
        result = open(self.outfile, 'rb').read()
        self.assertEqual(
            result,
            'application_category,application_fee,application_slip_notice,code,'
            'description,enddate,hidden,mode,prefix,send_email,startdate,'
            'strict_deadline,title,with_picture,year\r\n'

            'basic,0.0,,dp2017,'
            '"Some Description\nwith linebreak\n<<de>>man spriht deutsh",'
            '2017-01-31 23:00:00+00:00#,0,,app,0,2017-01-01 12:00:00+00:00#,1,'
            'General Studies,1,2017\r\n'
            )
        return

class ApplicantExporterTest(ApplicantImportExportSetup):

    layer = FunctionalLayer

    def setUp(self):
        super(ApplicantExporterTest, self).setUp()
        self.outfile = os.path.join(self.workdir, 'myoutput.csv')
        self.cat = getUtility(ICatalog, name='applicants_catalog')
        self.intids = getUtility(IIntIds)
        return

    def test_ifaces(self):
        # make sure we fullfill interface contracts
        obj = ApplicantExporter()
        verifyObject(ICSVExporter, obj)
        verifyClass(ICSVExporter, ApplicantExporter)
        return

    def test_get_as_utility(self):
        # we can get an applicant exporter as utility
        result = queryUtility(ICSVExporter, name="applicants")
        self.assertTrue(result is not None)
        return

    def setup_applicant(self, applicant):
        # set predictable values for `applicant`
        applicant.reg_number = u'123456'
        applicant.applicant_id = u'dp2011_654321'
        applicant.firstname = u'Anna'
        applicant.lastname = u'Tester'
        applicant.middlename = u'M.'
        applicant.date_of_birth = datetime.date(1981, 2, 4)
        applicant.sex = 'f'
        applicant.email = 'anna@sample.com'
        applicant.phone = u'+234-123-12345'
        applicant.course1 = self.certificate
        applicant.course2 = self.certificate
        applicant.course_admitted = self.certificate
        applicant.notice = u'Some notice\nin lines.'
        applicant.password = 'any password'
        result_entry = ResultEntry(
            KofaUtils.EXAM_SUBJECTS_DICT.keys()[0],
            KofaUtils.EXAM_GRADES[0][0]
            )
        applicant.school_grades = [
            result_entry]
        return applicant

    def test_export_emtpy(self):
        # we can export nearly empty applicants
        self.applicant.applicant_id = u'dp2011_654321'
        exporter = ApplicantExporter()
        exporter.export([self.applicant], self.outfile)
        result = open(self.outfile, 'rb').read()
        # The exported records do contain a real date in their
        # history dict. We skip the date and split the comparison
        # into two parts.
        self.assertTrue(
            'applicant_id,course1,course2,course_admitted,date_of_birth,'
            'email,firstname,lastname,locked,middlename,notice,phone,'
            'reg_number,sex,special_application,student_id,suspended,'
            'password,state,history,container_code,application_number,'
            'display_fullname,application_date\r\n'
            'dp2011_654321,,,,,,Anna,Tester,0'
            in result)
        self.assertTrue(
            'Application initialized by system\'],dp2011,654321,Anna Tester'
            in result)
        return

    def test_export(self):
        # we can really export applicants
        # set values we can expect in export file
        applicant = self.setup_applicant(self.applicant)
        exporter = ApplicantExporter()
        exporter.export([applicant], self.outfile)
        result = open(self.outfile, 'rb').read()
        # The exported records do contain a real date in their
        # history dict. We skip the date and split the comparison
        # into two parts.
        self.assertTrue(
            'applicant_id,course1,course2,course_admitted,date_of_birth,'
            'email,firstname,lastname,locked,middlename,notice,phone,'
            'reg_number,sex,special_application,student_id,suspended,'
            'password,state,history,container_code,application_number,'
            'display_fullname,application_date\r\n'
            'dp2011_654321,CERT1,CERT1,CERT1,1981-02-04#,'
            'anna@sample.com,Anna,Tester,'
            in result)
        self.assertTrue(
            'Application initialized by system\'],dp2011,654321,'
            'Anna M. Tester,\r\n'
            in result)

        return

    def test_export_all(self):
        # we can export all applicants in a portal
        # set values we can expect in export file
        self.applicant = self.setup_applicant(self.applicant)
        exporter = ApplicantExporter()
        exporter.export_all(self.app, self.outfile)
        result = open(self.outfile, 'rb').read()
        self.assertTrue(
            'applicant_id,course1,course2,course_admitted,date_of_birth,'
            'email,firstname,lastname,locked,middlename,notice,phone,'
            'reg_number,sex,special_application,student_id,suspended,'
            'password,state,history,container_code,application_number,'
            'display_fullname,application_date\r\n'
            'dp2011_654321,CERT1,CERT1,CERT1,1981-02-04#,'
            'anna@sample.com,Anna,Tester,'
            in result)
        self.assertTrue(
            'Application initialized by system\'],dp2011,654321,'
            'Anna M. Tester,\r\n'
            in result)
        return

    def test_export_filtered(self):
        self.applicant = self.setup_applicant(self.applicant)
        exporter = ApplicantExporter()
        exporter.export_filtered(
            self.app, self.outfile, container=self.container.code)
        result = open(self.outfile, 'rb').read()
        self.assertTrue(
            'applicant_id,course1,course2,course_admitted,date_of_birth,'
            'email,firstname,lastname,locked,middlename,notice,phone,'
            'reg_number,sex,special_application,student_id,suspended,'
            'password,state,history,container_code,application_number,'
            'display_fullname,application_date\r\n'
            'dp2011_654321,CERT1,CERT1,CERT1,1981-02-04#,'
            'anna@sample.com,Anna,Tester,'
            in result)
        self.assertTrue(
            'Application initialized by system\'],dp2011,654321,'
            'Anna M. Tester,\r\n'
            in result)
        # In empty container no applicants are exported
        container = ApplicantsContainer()
        container.code = u'anything'
        self.app['applicants']['anything'] = self.container
        exporter.export_filtered(
            self.app, self.outfile, container=container.code)
        result = open(self.outfile, 'rb').read()
        self.assertTrue(
            'applicant_id,course1,course2,course_admitted,date_of_birth,'
            'email,firstname,lastname,locked,middlename,notice,phone,'
            'reg_number,sex,special_application,student_id,suspended,'
            'password,state,history,container_code,application_number,'
            'display_fullname,application_date\r\n'
            in result)
        return


class ApplicantPaymentExporterTest(ApplicantImportExportSetup):

    layer = FunctionalLayer

    def setUp(self):
        super(ApplicantPaymentExporterTest, self).setUp()
        self.outfile = os.path.join(self.workdir, 'myoutput.csv')
        self.cat = getUtility(ICatalog, name='applicants_catalog')
        self.intids = getUtility(IIntIds)
        return

    def test_ifaces(self):
        # make sure we fullfill interface contracts
        obj = ApplicantPaymentExporter()
        verifyObject(ICSVExporter, obj)
        verifyClass(ICSVExporter, ApplicantPaymentExporter)
        return

    def test_get_as_utility(self):
        # we can get an applicant exporter as utility
        result = queryUtility(ICSVExporter, name="applicantpayments")
        self.assertTrue(result is not None)
        return

    def setup_applicant(self, applicant):
        # set predictable values for `applicant`
        applicant.reg_number = u'123456'
        applicant.applicant_id = u'dp2011_654321'
        applicant.firstname = u'Anna'
        applicant.lastname = u'Tester'
        applicant.middlename = u'M.'
        applicant.date_of_birth = datetime.date(1981, 2, 4)
        applicant.sex = 'f'
        applicant.email = 'anna@sample.com'
        applicant.phone = u'+234-123-12345'
        # Add payment
        payment = createObject(u'waeup.ApplicantOnlinePayment')
        payment.p_id = 'p120'
        payment.p_session = 2012
        payment.p_category = 'application'
        payment.p_state = 'paid'
        applicant['p120'] = payment
        return applicant

    def test_export(self):
        applicant = self.setup_applicant(self.applicant)
        exporter = ApplicantPaymentExporter()
        exporter.export(applicant.payments, self.outfile)
        result = open(self.outfile, 'rb').read()
        cdate = str('%s#' % self.applicant['p120'].creation_date)
        self.assertEqual(
            'ac,amount_auth,creation_date,p_category,p_combi,p_id,'
            'p_item,p_session,p_state,payment_date,r_amount_approved,'
            'r_code,r_desc,applicant_id,reg_number,display_fullname\r\n'
            ',0.0,%s,application,[],p120,,2012,paid,,0.0,,,dp2011_654321,'
            '123456,Anna M. Tester\r\n' % cdate, result)
        return

    def test_export_all(self):
        self.applicant = self.setup_applicant(self.applicant)
        exporter = ApplicantPaymentExporter()
        exporter.export_all(self.app, self.outfile)
        result = open(self.outfile, 'rb').read()
        cdate = str('%s#' % self.applicant['p120'].creation_date)
        self.assertEqual(
            'ac,amount_auth,creation_date,p_category,p_combi,p_id,'
            'p_item,p_session,p_state,payment_date,r_amount_approved,'
            'r_code,r_desc,applicant_id,reg_number,display_fullname\r\n'
            ',0.0,%s,application,[],p120,,2012,paid,,0.0,,,dp2011_654321,'
            '123456,Anna M. Tester\r\n' % cdate, result)
        return

    def test_export_filtered(self):
        self.applicant = self.setup_applicant(self.applicant)
        exporter = ApplicantPaymentExporter()
        exporter.export_filtered(
            self.app, self.outfile, container=self.container.code)
        result = open(self.outfile, 'rb').read()
        cdate = str('%s#' % self.applicant['p120'].creation_date)
        self.assertEqual(
            'ac,amount_auth,creation_date,p_category,p_combi,p_id,'
            'p_item,p_session,p_state,payment_date,r_amount_approved,'
            'r_code,r_desc,applicant_id,reg_number,display_fullname\r\n'
            ',0.0,%s,application,[],p120,,2012,paid,,0.0,,,dp2011_654321,'
            '123456,Anna M. Tester\r\n' % cdate, result)
        return
