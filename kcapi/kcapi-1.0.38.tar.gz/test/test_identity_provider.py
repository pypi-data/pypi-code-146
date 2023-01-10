import unittest, time
from .testbed import KcBaseTestCase
import json


def load_sample(fname):
    f = open(fname)
    file1 = json.loads(f.read())
    f.close()
    return file1


class TestingUserAPI(KcBaseTestCase):

    def test_identity_provider_adding_saml_and_oid_IDP_providers(self):
        idp1 = self.kc.build('identity-provider', self.REALM)
        idp = self.kc.build('idp', self.REALM)
        saml = load_sample('./test/payloads/idp_saml.json')
        oid = load_sample('./test/payloads/idp_oid.json')
        state1 = idp.create(saml).isOk()
        self.assertTrue(state1)

        state2 = idp1.create(oid).isOk()
        self.assertTrue(state2)

        oidc_ip = idp1.findFirstByKV('alias', 'oidc666')
        saml_ip = idp1.findFirstByKV('alias', 'saml666')

        self.assertEqual(saml_ip['alias'], saml['alias'], 'SAML alias should match')
        self.assertEqual(oidc_ip['alias'], oid['alias'], 'SAML alias should match')

    def setUp(self):
        super().setUp(create_all=False)
        self.testbed.createRealms()
        self.REALM = self.testbed.REALM
        self.kc = self.testbed.getKeycloak()


if __name__ == '__main__':
    unittest.main()
