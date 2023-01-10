import unittest, time
from copy import copy

from kcapi.rest.crud import KeycloakCRUD
from kcapi.rest.targets import Targets
from kcapi.rest.url import RestURL
from .testbed import KcBaseTestCase
import json
import os

def load_sample(fname):
    f = open(fname)
    file1 = json.loads(f.read())
    f.close()
    return file1

def exist(that, res, name):
    ret  = res.findFirstByKV('username', name)
    that.assertEqual(name, ret['firstName'], 'We expect a role ['+name+'] to be created')
    return ret['id']



def test_complete_CRUD(that, users):
        ## POST
        state = users.create(that.USER_DATA)
        that.assertTrue(state, 'fail while posting')

        ret  = users.findFirstByKV('username', 'pepe')
        that.assertEqual('pepe', ret['firstName'], 'We expect a user with pepe as username to be created')

        ## TEST existByKV True
        existByKV_true_state = users.existByKV("username",that.USER_DATA["username"])
        that.assertTrue(existByKV_true_state,msg="[TEST existByKV True] We expect True if user does exist")

        ## UPDATE
        state = users.update(ret['id'], {'firstName': 'pedro'})
        that.assertTrue(state, 'fail while updating')

        ret  = users.findFirstByKV('firstName', 'pedro')
        that.assertTrue(ret != False, 'Something wrong updating the resource.')
        that.assertEqual('pedro', ret['firstName'], 'We expect a user with pepe as username to be created')

        ## GET
        usr = users.get(ret['id']).resp().json()
        that.assertEqual(ret['id'], usr['id'])

        _all = users.all()
        that.assertEqual(len(_all), 4, 'All users amount to one')


        ## DELETE
        remove_state = users.remove(ret['id']).isOk()
        that.assertTrue(remove_state)
        removed = users.findFirstByKV('firstName', 'pedro')

        that.assertFalse(removed)

        ## TEST existByKV False
        existByKV_false_state = users.existByKV("username","user_existByKV")
        that.assertFalse(existByKV_false_state,msg="[TEST existByKV False] We expect False if user does not exist")


class SlowFile:
    def __init__(self, content, delays=[]):
        self.content = bytes(content, 'utf-8')
        self.delays = delays
        self.ii = -1

    def __iter__(self):
        # self.ii = -1
        return self

    def __next__(self):
        self.ii += 1
        if self.ii >= len(self.content):
            raise StopIteration
        if self.ii < len(self.delays):
            time.sleep(self.delays[self.ii])
        return self.content[self.ii: self.ii+1]


class Testing_slow_crud(KcBaseTestCase):

    def testing_crud_API(self):
        token = self.testbed.token

        users = KeycloakCRUD()
        users.targets = Targets.makeWithURL(str(self.USER_ENDPOINT))
        users.token = token

        test_complete_CRUD(self, users)

    @unittest.skipIf(not int(os.environ.get("KC_RUN_SLOW_TEST", "0")), "Test is run only if KC_RUN_SLOW_TEST is set")
    def test_slow_CRUD(self):
        """
        We test if long-lasting requests can complete.
        We monkey patch requests.put to achieve long upload time.
        The access_token expires in 60 sec.
        Assumption is that access_token is verified at beginning of request only.
        Verification: run
        KC_RUN_SLOW_TEST=1 python -m unittest test.test_crud.Testing_User_API.test_slow_CRUD
        and check TCP traffic with tcpdump.
        """
        token = self.testbed.token
        users = KeycloakCRUD()
        users.targets = Targets.makeWithURL(str(self.USER_ENDPOINT))
        users.token = token

        ## IS PRESENT
        user_present = users.findFirstByKV('firstName', 'pepe')
        self.assertFalse(user_present)

        ## POST
        # state = users.create(self.USER_DATA)
        # inline code for users.create()
        def users_create(obj, payload):
            import requests
            from kcapi.rest.resp import ResponseHandler
            url = obj.targets.url('create')
            data_file = SlowFile(json.dumps(payload), [10]*10)
            with KcSession() as session:
                ret = session.post(url, data=data_file, headers=obj.headers())
            return ResponseHandler(url, method='Post', payload=payload).handleResponse(ret)

        state = users_create(users, self.USER_DATA)
        self.assertTrue(state, 'fail while posting')

        ret = users.findFirstByKV('username', 'pepe')
        self.assertEqual('pepe', ret['firstName'], 'We expect a user with pepe as username to be created')

        ## DELETE
        remove_state = users.remove(ret['id']).isOk()
        self.assertTrue(remove_state)
        ## IS PRESENT
        user_present = users.findFirstByKV('firstName', 'pepe')
        self.assertFalse(user_present)

    def setUp(self):
        super().setUp()

        self.USER_ENDPOINT = RestURL(self.testbed.ENDPOINT)
        self.USER_ENDPOINT.addResources(['auth', 'admin', 'realms', self.REALM, 'users'])

        self.USER_DATA = {"enabled":True,"attributes":{},"username":"pepe","emailVerified":"", "firstName": 'pepe'}


class TestKeycloakCRUD_part2(KcBaseTestCase):
    def setUp(self):
        super().setUp(create_all=False)
        self.REALM = self.testbed.REALM
        self.testbed.createRealms()
        self.testbed.createUsers()

    def test_get_one_ok(self):
        users_api = self.testbed.kc.build("users", self.testbed.REALM)
        user_id = users_api.findFirstByKV("username", "batman")["id"]

        user = users_api.get_one(user_id)

        self.assertIsInstance(user, dict)
        # "assertDictContainsSubset(a, b)" == "a == a|b"
        self.assertEqual(user, user | {
            "username": "batman",
            "lastName": "Wayne",
            "enabled": True,
        })

    def test_get_one_invalid_id(self):
        users_api = self.testbed.kc.build('users', self.testbed.REALM)
        self.assertRaises(Exception, users_api.get_one, "no-such-user-uuid")

    def test_update_rmw_ok(self):
        users_api = self.testbed.kc.build("users", self.testbed.REALM)
        user_old = users_api.findFirstByKV("username", "batman")
        user_id = user_old["id"]

        # data1 = {"username": "batman-new"}  # username cannot be updated, but API return 204
        data1 = {"lastName": "Wayne-new"}
        data2 = {"email": "bw@example.com"}
        data3 = {"enabled": False}

        ret = users_api.update_rmw(user_id, {})
        ret = users_api.update_rmw(user_id, data1)
        ret = users_api.update_rmw(user_id, data2)
        ret = users_api.update_rmw(user_id, data3)

        user_new = users_api.get_one(user_id)
        # "assertDictContainsSubset(a, b)" == "a == a|b"
        self.assertEqual(user_new, user_old | {
            "username": "batman",
            "lastName": "Wayne-new",
            "email": "bw@example.com",
            "enabled": False,
        })

    def test_update_rmw_invalid_id(self):
        users_api = self.testbed.kc.build('users', self.testbed.REALM)
        self.assertRaises(Exception, users_api.update_rmw, "no-such-user-uuid", {})


if __name__ == '__main__':
    unittest.main()

# setUp vs setUpClass
