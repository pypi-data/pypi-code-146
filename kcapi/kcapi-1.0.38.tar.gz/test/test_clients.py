import unittest
import json
from copy import copy

from .testbed import KcBaseTestCase


def load_sample(fname):
    f = open(fname)
    file1 = json.loads(f.read())
    f.close()
    return file1


class TestClients(KcBaseTestCase):
    def test_client_extra_methods(self):
        clients = self.testbed.getKeycloak().build('clients', self.REALM)
        self.assertIsNotNone(clients.roles, 'The client object should have a roles method.')

    def test_client_secrets(self):
        secret_passphrase = "cf6c3215-2af0-42f7-a9ce-3a371e738417"
        clients = self.testbed.getKeycloak().build('clients', self.REALM)
        state = clients.create({"enabled":True,"attributes":{},"secret":secret_passphrase ,"redirectUris":[],"clientId":"44","protocol":"openid-connect", "publicClient": False}).isOk()
        self.assertTrue(state, "A private client should be created")

        #client_secrets = clients.secrets({'key': 'clientId', 'value':"44"})
        #remote_passphrase = client_secrets.all()

        #client_secrets_creation_state = client_secrets.create({"type":self.testbed.REALM,"client":secret_passphrase}).isOk()
        #self.assertTrue(client_secrets_creation_state, "A secret passphrase should be assigned.")
        #remote_passphrase = client_secrets.all()
        #self.assertTrue(len(remote_passphrase)>0, "We expect to obtain a new passphrase.")

    def test_client_roles(self):
        client_payload = load_sample('./test/payloads/client.json')
        clients_api = self.testbed.getKeycloak().build('clients', self.REALM)

        # initial cleanup
        ret = clients_api.removeFirstByKV('clientId', client_payload['clientId'])
        ret = clients_api.findFirstByKV('clientId', client_payload['clientId'])
        self.assertEqual(ret, [], 'Client should not exist before')
        # create empty client
        svc_state = clients_api.create(client_payload).isOk()
        self.assertTrue(svc_state, 'The service should return a 200.')

        ret = clients_api.findFirstByKV('clientId', client_payload['clientId'])
        self.assertNotEqual(ret, [], 'It should return the posted client')

        # test client role create, with attributes
        client_query = {'key': 'clientId', 'value': client_payload['clientId']}
        client_roles_api = clients_api.roles(client_query)
        role_doc = {
            "name": "new-role",
            "description": "here should go a description.",
            "attributes": {
                "ci-new-role-key0": [
                    "ci-new-role-value0"
                ]
            },
            'clientRole': True,
            'composite': False,
        }
        svc_roles_state = client_roles_api.create(role_doc).isOk()
        self.assertTrue(svc_roles_state, 'The client_roles service should return a 200.')

        client_roles = clients_api.get_roles(client_query)
        self.assertEqual(1, len(client_roles))
        new_role = client_roles[0]
        new_role_min = copy(new_role.value)
        new_role_min.pop("id")
        new_role_min.pop("containerId")
        self.assertEqual(role_doc, new_role_min)

        # create realm role, it will be added as composite (sub-role) to client role
        role = {"name": "x_black_magic_x"}
        roles = self.testbed.getKeycloak().build("roles", self.REALM)
        state = roles.create(role).isOk()
        self.assertTrue(state, "A role should be created")

        # test adding composite/sub-role
        state = new_role.composite().link(role['name']).isOk()

        self.assertTrue(state, "A composite role should be added to the current client role.")

        composites_roles = new_role.composite().findAll().resp().json()
        self.assertEqual(composites_roles[0]['name'], 'x_black_magic_x', "We should have a composite role called: x_black_magic_x")

        # test removing composite/sub-role
        state_delete = new_role.composite().unlink(role['name']).isOk()
        self.assertTrue(state, "A composite role should be deleted from the current client role.")

        empty_composites_role = new_role.composite().findAll().resp().json()
        self.assertEqual(empty_composites_role, [],
                         "We should have a empty roles")

    def test_client_roles_update(self):
        client_payload = load_sample('./test/payloads/client.json')
        clients_api = self.testbed.getKeycloak().build('clients', self.REALM)

        # initial cleanup
        ret = clients_api.removeFirstByKV('clientId', client_payload['clientId'])
        ret = clients_api.findFirstByKV('clientId', client_payload['clientId'])
        self.assertEqual(ret, [], 'Client should not exist before')
        # create empty client
        svc_state = clients_api.create(client_payload).isOk()
        self.assertTrue(svc_state, 'The service should return a 200.')

        ret = clients_api.findFirstByKV('clientId', client_payload['clientId'])
        self.assertNotEqual(ret, [], 'It should return the posted client')

        # create role
        client_query = {'key': 'clientId', 'value': client_payload['clientId']}
        client_roles_api = clients_api.roles(client_query)
        svc_roles_state = client_roles_api.create(
            {"name": "new-role", "description": "here should go a description."}).isOk()
        self.assertTrue(svc_roles_state, 'The client_roles service should return a 200.')
        # ----

        # check initial state
        assert str(clients_api.targets.targets["read"]).endswith("/clients")
        # is ok
        new_role_a = clients_api.get_roles(client_query)[0]
        # URL is corrupted
        assert str(clients_api.targets.targets["read"]).endswith("/clients")

        new_role_a_min = copy(new_role_a.value)
        new_role_a_min.pop("id")
        new_role_a_min.pop("containerId")
        self.assertEqual(
            {
                'attributes': {},
                'clientRole': True,
                'composite': False,
                'description': 'here should go a description.',
                'name': 'new-role'
            },
            new_role_a_min,
        )

        # update role
        # We need to send full payload.
        new_data = copy(new_role_a.value)
        new_data.update({
            "description": "here should go a description. NEW",
            "attributes": {
                "ci-new-role-key0": [
                    "ci-new-role-value0"
                ]
            },
        })
        client_roles_api.update(new_role_a.value["id"], new_data).isOk()

        # check updated state
        new_role_b = clients_api.get_roles(client_query)[0]
        new_role_b_min = copy(new_role_b.value)
        new_role_b_min.pop("id")
        new_role_b_min.pop("containerId")
        self.assertEqual(
            {
                'attributes': {'ci-new-role-key0': ['ci-new-role-value0']},
                'clientRole': True,
                'composite': False,
                'description': 'here should go a description. NEW',
                'name': 'new-role'
            },
            new_role_b_min,
        )

    def test_client_roles_removal(self):
        client_payload = load_sample('./test/payloads/client.json')
        client_payload['clientId'] = 'test_client_roles_removal'
        client_role_name = "deleteme-role"

        clients_api = self.testbed.getKeycloak().build('clients', self.REALM)
        svc_state = clients_api.create(client_payload).isOk()

        client_query = {'key': 'clientId', 'value': client_payload['clientId']}
        client_roles_api = clients_api.roles(client_query)
        svc_roles_state = client_roles_api.create(
            {"name": client_role_name, "description": "A role that need to be deleted."}).isOk()

        ret_client_roles = client_roles_api.findFirstByKV('name', client_role_name)
        self.assertNotEqual(ret_client_roles, [], 'It should return the posted client')

        result = client_roles_api.removeFirstByKV('name', client_role_name)
        self.assertTrue(result, 'The server should return ok.')

        self.assertEqual(client_roles_api.findFirstByKV('name', client_role_name), [], 'It should return the posted client')

    # TODO - likely all tests should use only setUp/tearDown
    #  - each test has clean environment
    #  - VCR than can really work
    # @classmethod
    # def setUpClass(cls):
    #     pass

    # @classmethod
    # def tearDownClass(cls):
    #     pass

    def setUp(self):
        super().setUp(create_all=False)
        self.testbed.createRealms()
        # not needed
        # cls.testbed.createUsers()
        # cls.testbed.createClients()
        self.REALM = self.testbed.REALM

    def tearDown(self):
        self.testbed.goodBye()


class TestClientRoleCRUD(KcBaseTestCase):
    def setUp(self):
        super().setUp(create_all=False)
        self.testbed.goodBye()  # removes only realm
        self.testbed.createRealms()
        self.testbed.createClients()
        self.REALM = self.testbed.REALM

    def tearDown(self):
        pass
        # self.testbed.goodBye()

    def _compare_role_doc(self, role1, role2):
        r1 = copy(role1)
        r2 = copy(role2)
        for rr in [r1, r2]:
            rr.pop("id", None)
            rr.pop("containerid", None)
        return r1 == r2

    def test_ClientRoleCRUD_no_attributes(self):
        # the test role, without attributes, very minimal
        role_doc = {
            "name": "new-role",
            "description": "here should go a description.",
            # "attributes": {
            #     "ci-new-role-key0": [
            #         "ci-new-role-value0"
            #     ]
            # },
            # 'clientRole': True,
            # 'composite': False,
        }
        expected_role = copy(role_doc)
        expected_role.update({
            "attributes": {},
            'clientRole': True,
            'composite': False,
        })
        self.do_test_ClientRoleCRUD_attributes(role_doc, expected_role)

    def test_ClientRoleCRUD_with_attributes(self):
        # the test role, with all fields
        role_doc = {
            "name": "new-role",
            "description": "here should go a description.",
            "attributes": {
                "ci-new-role-key0": [
                    "ci-new-role-value0"
                ]
            },
            'clientRole': True,
            'composite': False,
        }
        expected_role = copy(role_doc)
        self.do_test_ClientRoleCRUD_attributes(role_doc, expected_role)

    def do_test_ClientRoleCRUD_attributes(self, role_doc, expected_role):
        """
        Ensure ClientRoleCRUD .get()/all()/... do always include also "attributes".
        E.g. briefRepresentation=False must be used.
        """
        client_clientId = "dc"
        clients_api = self.testbed.getKeycloak().build('clients', self.REALM)
        client_query = {'key': 'clientId', 'value': client_clientId}
        client_roles_api = clients_api.roles(client_query)

        # check initial state
        client_roles = client_roles_api.all()
        self.assertEqual(0, len(client_roles))

        # prepare test role
        svc_roles_state = client_roles_api.create(role_doc).isOk()
        self.assertTrue(svc_roles_state, 'The client_roles service should return a 200.')
        # ---------------------

        # test .get(), .all(), findFirst...(), etc
        client_roles = client_roles_api.all()
        self.assertEqual(1, len(client_roles))
        self.assertTrue(expected_role, client_roles[0])
        role_id = client_roles[0]["id"]

        client_roles = client_roles_api.findAll().verify().resp().json()
        self.assertEqual(1, len(client_roles))
        self.assertTrue(expected_role, client_roles[0])

        role = client_roles_api.get(role_id)
        self.assertTrue(expected_role, role)

        role = client_roles_api.findFirstByKV("name", "new-role")
        self.assertTrue(expected_role, role)
