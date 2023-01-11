# Tests for applicant webservices
from zope.app.testing.xmlrpc import ServerProxy
from waeup.kofa.testing import FunctionalLayer
from waeup.kofa.applicants.tests.test_browser import ApplicantsFullSetup


class XMLRPCTests(ApplicantsFullSetup):
    # check XMLRPC services for university portal

    layer = FunctionalLayer

    def setup_applicant(self, applicant):
        applicant.firstname = u'Bob'
        applicant.lastname = u'Bubble'
        applicant.email = 'bob@sample.com'
        pass

    def test_check_applicant_credentials_valid(self):
        # make sure we can get applicant infos providing valid creds
        server = ServerProxy('http://mgr:mgrpw@localhost/app')
        self.setup_applicant(self.applicant)
        apl_id = self.applicant.applicant_id
        result = server.check_applicant_credentials(apl_id, 'apwd')
        self.assertEqual(
            result, {
                'description': 'Bob Bubble',
                'email': 'bob@sample.com',
                'id': apl_id,
                'type': 'applicant'}
            )
        return

    def test_check_applicant_credentials_invalid(self):
        # invalid creds will give no results
        server = ServerProxy('http://mgr:mgrpw@localhost/app')
        self.setup_applicant(self.applicant)
        apl_id = self.applicant.applicant_id
        result = server.check_applicant_credentials(apl_id, 'wrong-pw')
        self.assertEqual(result, None)
        return

    def test_get_moodle_data(self):
        # make sure we can get applicant infos providing valid creds
        server = ServerProxy('http://mgr:mgrpw@localhost/app')
        self.setup_applicant(self.applicant)
        apl_id = self.applicant.applicant_id
        result = server.get_applicant_moodle_data(apl_id)
        self.assertEqual(
            result, {
                'lastname': 'Bubble',
                'email': 'bob@sample.com',
                'firstname': 'Bob',
                }
            )
        return

