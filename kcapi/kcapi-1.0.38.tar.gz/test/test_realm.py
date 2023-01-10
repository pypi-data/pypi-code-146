import unittest, time
from .testbed import KcBaseTestCase
import json


def load_sample(file_name):
    f = open(file_name)
    payload = json.loads(f.read())
    f.close()

    return payload


class TestingRealmAPI(KcBaseTestCase):

    def testing_realm_api_methods(self):
        realms = self.testbed.getKeycloak().build('realms', self.REALM)
        self.assertTrue(hasattr(realms, 'caches'))


    def testing_realm_cache_reset(self):
        realms = self.testbed.getKeycloak().build('realms', self.REALM)

        caches = realms.caches(self.REALM)

        self.assertEqual(caches.clearRealmCache().resp().status_code, 204)

    def testing_user_cache_reset(self):
        realms = self.testbed.getKeycloak().build('realms', self.REALM)

        caches = realms.caches(self.REALM)
        self.assertEqual(caches.clearUserCache().resp().status_code, 204)

    def testing_key_cache_reset(self):
        realms = self.testbed.getKeycloak().build('realms', self.REALM)

        caches = realms.caches(self.REALM)

        self.assertEqual(caches.clearKeyCache().resp().status_code, 204)

    def testing_complex_realm_publishing(self):
        admin = self.testbed.getAdminRealm()
        realm_cfg = load_sample('./test/payloads/complex_realms.json')
        creation_state = admin.create(realm_cfg).isOk()
        self.assertTrue(creation_state, 'This realm should be created')

    def tearDown(self):
        realm = "4pl_1234"  # from ./test/payloads/complex_realms.json
        if self.testbed.master_realm.exist(realm):
            state = self.testbed.master_realm.remove(realm).ok()
        super().tearDown()

if __name__ == '__main__':
    unittest.main()
