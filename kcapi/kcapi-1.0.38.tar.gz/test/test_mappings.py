import unittest, time
from kcapi import OpenID, Keycloak
from .testbed import TestBed, KcBaseTestCase

ADMIN_USER = "admin"
ADMIN_PSW  = "admin1234"
REALM = "test_heroes_test"
ENDPOINT = 'https://sso-cvaldezr-stage.apps.sandbox-m2.ll9k.p1.openshiftapps.com'


TEST_REALM = "TESTING"

class Testing_Mappings(KcBaseTestCase):
    def testing_adding_removing_roles_to_group(self):
        groups = self.kc.build('groups', self.realm)
        self.assertTrue(hasattr(groups, "realmRoles"))

        #TestBed class will create one group called "DC"
        #And three roles called [level-1, level-2, level-3]
        # Initially group has 0 role assigned
        group = {"key":"name", "value": self.groupName}
        roles_mapping = groups.realmRoles(group)
        rolesInGroup = roles_mapping.all()
        self.assertEqual(len(rolesInGroup), 0, 'should be 0 roles initially')

        # assign roles to group
        state = roles_mapping.add(self.roleNames)
        self.assertTrue(state)

        rolesInGroup = roles_mapping.all()
        self.assertEqual(len(rolesInGroup), 3, 'should be 3 roles: [level-1, level-2, level-3]')

        # remove_roles_from_group
        roles_mapping.remove(["level-1", "level-2"])
        rolesInGroup = roles_mapping.all()
        self.assertEqual(len(rolesInGroup), 1, 'we should got only 1 role: [level-3]')

    def testing_adding_removing_user_to_group(self):
        users = self.kc.build('users', self.realm)
        self.assertTrue(hasattr(users, "joinGroup"))

        usr = {"key": "username", "value": "batman"}
        gpr = {"key": "name", "value": self.groupName}

        join_state = users.joinGroup(usr, gpr).isOk()
        self.assertTrue(join_state)

        # def testing_user_group_mapping(self):
        #users = self.kc.build('users', self.realm)
        #usr = {"key": "username", "value": "batman"}
        batman = users.groupMapping(usr)
        self.assertEqual(len(batman.all()), 1, 'the user batman should belong to one group')

        # def testing_user_leaving_group(self):
        # users = self.kc.build('users', self.realm)
        self.assertTrue(hasattr(users, "joinGroup"))

        leave_status = users.leaveGroup(usr, gpr).isOk()
        self.assertTrue(leave_status)

        groups = users.groups(usr)
        self.assertEqual(len(groups), 0)

    def setUp(self):
        super().setUp(create_all=False)
        # self.testbed = TestBed(REALM, ADMIN_USER, ADMIN_PSW, ENDPOINT)
        self.testbed.createRealms()
        self.testbed.createUsers()
        self.testbed.createGroups()
        self.kc = self.testbed.getKeycloak()
        self.realm = self.testbed.REALM
        self.master_realm = self.testbed.getAdminRealm()
        self.roleNames = self.testbed.roleNames
        self.groupName = self.testbed.groupName

    def tearDown(self):
        if self.master_realm.exist(TEST_REALM):
            self.master_realm.remove(TEST_REALM)
        super().tearDown()


if __name__ == '__main__':
    unittest.main()
