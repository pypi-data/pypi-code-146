from kcapi import OpenID, Keycloak
import os
import json
import unittest
from vcr_unittest import VCRTestCase

import logging
logging.basicConfig(level=logging.DEBUG)

def readFromJSON(filename):
    with open(filename) as json_file:
        return json.load(json_file)

class TestBed:
    def __init__(self, realm = None, username = None, password = None, endpoint = None): 

        self.USER = os.environ['KC_USER']
        self.PASSWORD = os.environ['KC_PASSWORD']
        self.REALM = os.environ['KC_REALM']
        self.ENDPOINT = os.environ['KC_ENDPOINT']

        self.groupName = 'DC'
        self.roleNames = ['level-1', 'level-2', 'level-3'] 

        # TODO this is not intercepted by vcrpy.
        token = OpenID.createAdminClient(self.USER, self.PASSWORD, url=self.ENDPOINT).getToken()
        self.kc = Keycloak(token, self.ENDPOINT)
        self.master_realm = self.kc.admin()
        self.realm = self.REALM 
        self.token = token

    def deleteRealms(self):
        realm = self.realm
        if self.master_realm.existByKV("id", realm):
            self.master_realm.removeFirstByKV("id", realm)

    def createRealms(self):
        realm = self.realm
        self.master_realm.create({"enabled": "true", "id": realm, "realm": realm})

    def createGroups(self):
        group = self.kc.build('groups', self.realm)
        g_creation_state = group.create({"name": self.groupName}).isOk()
        self.createRoles()


    def createRoles(self):
        roles = self.kc.build('roles', self.realm)
        for role in self.roleNames:
            roles.create({"name": role}).isOk() 


    def createClients(self):
        realm = self.realm
        client = {"enabled":True,
                  "attributes":{},
                  "redirectUris":[],
                  "clientId":"dc",
                  "protocol":"openid-connect", 
                  "directAccessGrantsEnabled":True
                  }

        clients = self.kc.build('clients', realm)
        if not clients.create(client).isOk(): 
            raise Exception('Cannot create Client')

    def createUsers(self):
        realm = self.realm
        test_users = [
                {"enabled":'true',"attributes":{},"username":"batman","firstName":"Bruce", "lastName":"Wayne", "emailVerified":""}, 
                {"enabled":'true',"attributes":{},"username":"superman","firstName":"Clark", "lastName":"Kent", "emailVerified":""}, 
                {"enabled":'true',"attributes":{},"username":"aquaman","firstName":"AAA%", "lastName":"Corrupt", "emailVerified":""}
        ]

        users = self.kc.build('users', realm)
        
        for usr in test_users: 
            users.create(usr).isOk()

    def goodBye(self):
        if self.master_realm.exist(self.realm):
            state = self.master_realm.remove(self.realm).ok()
            if not state:
                raise Exception("Cannot delete the realm -> " + self.realm )

    def getKeycloak(self):
        return self.kc
    def getAdminRealm(self):
        return self.master_realm


class KcBaseTestCase(VCRTestCase):
    # see https://github.com/agriffis/vcrpy-unittest/blob/master/vcr_unittest/testcase.py#L19
    # Try self.vcr_enabled=False to disable tests

    def setUp(self, *, create_all=True):
        super().setUp()
        self.testbed = TestBed()
        if create_all:
            self.testbed.createRealms()
            self.testbed.createUsers()
            self.testbed.createClients()
            self.REALM = self.testbed.REALM

    def tearDown(self):
        self.testbed.goodBye()
        super().tearDown()

    def _get_vcr_kwargs(self):
        kwargs = super()._get_vcr_kwargs()
        # https://vcrpy.readthedocs.io/en/latest/usage.html#record-modes
        # "once" or "new_episodes" makes sense - which is better?
        # "new_episodes" is more auto-magic, use it.
        # BUT - authentiaction is in setUp(), is not recorded, so each time a diffrent access token is send,
        # and VCR is not used.
        # We use "none".
        vcrpy_record_mode = os.environ.get("VCRPY_RECORD_MODE", "none")
        kwargs['record_mode'] = vcrpy_record_mode
        return kwargs
