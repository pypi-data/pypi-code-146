import json
from .resp import ResponseHandler
from .kcsession import KcSession


class KeycloakCRUD(object):
    # some derived classes (roles) need extra query paramters for list/read REST operations
    _rest_params_read = {}

    @classmethod
    def get_child(cls, that, resource_id, resource_name):
        # .get_child in derived classes need to return instance of derived class
        kc = cls()
        kc.token = that.token
        kc.targets = that.targets.copy()

        kc.targets.addResources([resource_id, resource_name])

        return kc

    def __init__(self): 
        self.targets = None
        self.token = None

    def headers(self):

        if self.token.expired():
            self.token = self.token.refresh()

        return {
                'Content-type': 'application/json', 
                'Authorization': 'Bearer '+ self.token.get_token()
        }

    def setIdentifier(self, _id = None, url = None):
        if _id:
            return url.addResource(_id)
        else:
            return url
    
    def create(self, payload):
        url = self.targets.url('create')

        with KcSession() as session:
            ret = session.post(url, data=json.dumps(payload), headers=self.headers())
        return ResponseHandler(url, method='Post', payload=payload).handleResponse(ret)

    def update(self, obj_id=None, payload=None):
        url = self.targets.url('update')
        target = str(self.setIdentifier(obj_id, url))

        with KcSession() as session:
            ret = session.put(target, data=json.dumps(payload), headers=self.headers())
        return ResponseHandler(target, method='Put', payload=payload).handleResponse(ret)

    def remove(self, _id, payload=None):
        delete = self.targets.url('delete')
        url = self.setIdentifier(_id, delete)
        with KcSession() as session:
            ret = session.delete(url, data=json.dumps(payload), headers=self.headers())
        return ResponseHandler(url, method='Delete', payload=payload).handleResponse(ret)
        
    def get(self, _id):
        params = self._rest_params_read
        url = self.targets.url('read')
        with KcSession() as session:
            ret = session.get(str(self.setIdentifier(_id, url)), params=params, headers=self.headers())
        return ResponseHandler(url, method='Get').handleResponse(ret)

    def findAll(self, params=None):
        if not params:
            # TODO drop method param params - now it can be set on per instance (or per-derived class) basis.
            params = self._rest_params_read
        url = self.targets.url('read')
        with KcSession() as session:
            ret = session.get(url, params=params, headers=self.headers())
        return ResponseHandler(url, method='Get').handleResponse(ret)

    def findFirst(self, params):
        return self.findFirstByKV(params['key'], params['value'])

    def findFirstByKV(self, key, value):
        rows = self.findAll().verify().resp().json()

        for row in rows:
            # Some components do not have Name attribute.
            if key in row and row[key].lower() == value.lower():
                return row

        return []

    def all(self, params=None):
        return self.findAll(params).verify().resp().json()

    def updateUsingKV(self, key, value, obj): 
        res_data = self.findFirstByKV(key,value)

        if res_data: 
            data_id = res_data['id']
            res_data.update(obj)
            return self.update(data_id, res_data).isOk() 
        else:
            return False

    def removeFirstByKV(self, key, value, custom_key="id"):
        row = self.findFirstByKV(key,value)

        if row:
            return self.remove(row[custom_key]).isOk()
        else:
            return False

    def existByKV(self, key, value): 
        ret = self.findFirstByKV(key, value)
        return ret != []

    def exist(self, _id):
        return self.get(_id).ok()

    def get_one(self, obj_id):
        """
        Returns a dict with response content.
        """
        return self.get(obj_id).verify().resp().json()

    def update_rmw(self, obj_id=None, partial_payload=None):
        """
        read/modify/write update - existing object will be partially updated.
        We first read current state, then send to server new state.

        Calling .update() on realm object with partial data can destroy some realm attributes.
        See https://github.com/justinc1/keycloak-fetch-bot/commit/c68610c671193aaf2fe71c23b68e3af3c989db2f.
        """
        if not partial_payload:
            partial_payload = {}
        full_payload = self.get_one(obj_id)
        full_payload.update(partial_payload)
        return self.update(obj_id, full_payload)
