from swimlane import Swimlane
import json
import uuid


class swimlane_server(object):

    def __init__(self, sw_url, sw_api_key, logger):
        self.logger = logger

        self.logger.info('Connect to Source: {}'.format(sw_url))
        self.swimlane = Swimlane(sw_url, access_token=sw_api_key, verify_ssl=False)

        self.logger.info('Building App Dictionary')
        self.apps_dictionary = self.getApplicationDictionary()
        self.logger.info('Building Task Dictionary')
        self.task_dictionary = self.getTaskDictionary()
        self.roles_dictionary = self.getRoleDictionary()
        self.asset_dictionary_name,self.asset_dictionary_id = self.getAssetDictionary()
        self.action_dictionary = self.getActionDictionary()

        self.log_dictionary = {}

        self.apps_objects = {}

    def updateWorkflow(self, AppName, workflow):
        workflow_response = self.swimlane.request(
            'put',
            '/workflow/{}'.format(workflow['id']),
            json=workflow
        )

        workflow = json.loads(workflow_response.text)

    def saveApp(self, AppName):
        app_obj = self.loadApp(appName=AppName)
        app_response = self.swimlane.request(
            'put',
            '/app/{}'.format(self.apps_dictionary[AppName]['id']),
            json = app_obj
        )

        self.apps_objects[self.apps_dictionary[AppName]['id']] = json.loads(app_response.text)

    def createEmptyApp(self, appName, **kwargs):

        app_obj = {
            "$type": "Core.Models.Application.Application, Core",
            "acronym": kwargs.pop('acronym', 'FEA'),
            "layout": [],
            "fields": [],
            "maxTrackingId": 0,
            "workspaces": [],
            "createWorkspace": False,
            "timeTrackingEnabled": False,
            "permissions": {
                "$type": "Core.Models.Security.PermissionMatrix, Core"
            },
            "id": kwargs.pop('id', str(uuid.uuid1()).replace('-', '')),
            "name": kwargs.pop('name', 'Fake Empty Application'),
            "description" : kwargs.pop('description', ''),
            "disabled": False
        }

        app_response = self.swimlane.request(
            'post',
            '/app',
            json = app_obj
        )

        raw_app_obj = json.loads(app_response.text)
        self.apps_objects[raw_app_obj['id']] = raw_app_obj
        self.apps_dictionary = self.getApplicationDictionary()

    def getAssetDictionary(self):
        asset_response = self.swimlane.request(
            'get',
            '/asset',
        )
        asset_raw = json.loads(asset_response.text)

        asset_dictionary_name = {}
        asset_dictionary_id = {}
        for asset in asset_raw:
            asset_dictionary_name[asset['name']] = asset
            asset_dictionary_id[asset['id']] = asset

        return asset_dictionary_name,asset_dictionary_id

    def getActionDictionary(self):
        action_response = self.swimlane.request('get','task/actions').json()

        action_dictionary = {}
        for action in action_response:
            action_dictionary[action['id']] = action

        return action_dictionary

    def getApplicationDictionary(self):
        apps_response = self.swimlane.request(
            'get',
            '/app/light',
        )
        apps_raw = json.loads(apps_response.text)

        apps_dictionary = {}
        for app in apps_raw:
            apps_dictionary[app['name']] = app

        return apps_dictionary

    def getRoleDictionary(self):
        roles_response = self.swimlane.request(
            'get',
            '/roles/light',
        )
        roles_raw = json.loads(roles_response.text)

        roles_dictionary = {}
        for role in roles_raw:
            roles_dictionary[role['name']] = role

        return roles_dictionary

    def getTaskDictionary(self):
        task_response = self.swimlane.request(
            'get',
            '/task/light',
        )
        task_raw = json.loads(task_response.text)

        tasks_dictionary = {}
        for task in task_raw:
            tasks_dictionary[task['name']] = task

        return tasks_dictionary

    def getFieldDictinoary(self, byID = None, byName = None, forceReload = False):
        if byID is not None:
            app_obj = self.loadApp(appID=byID, fieldsOnly = True, forceReload = forceReload)
        else:
            app_obj = self.loadApp(appName=byName, fieldsOnly = True, forceReload = forceReload)

        field_dictionary = {}
        for field_obj in app_obj:
            if 'id' in field_obj and 'name' in field_obj:
                field_dictionary[field_obj['name']] = field_obj

        return field_dictionary

    def loadWorkflow(self, appID=None, appName=None):
        if appName is not None:
            if appName in self.apps_dictionary:
                appID = self.apps_dictionary[appName]['id']
            else:
                #raise Exception('Unable to find AppID for {}'.format(appName))
                return {}


        workflow_response = self.swimlane.request(
            'get',
            '/workflow/{}'.format(appID),
        )

        return json.loads(workflow_response.text)

    def loadApp(self, appID=None, appName=None, forceReload = False, **kwargs):
        if appName is not None:
            if appName in self.apps_dictionary:
                appID = self.apps_dictionary[appName]['id']
            else:
                #raise Exception('Unable to find AppID for {}'.format(appName))
                return {"fields": [], "permissions": [], "layout": []}

        if forceReload or appID not in self.apps_objects:
            appdetail_response = self.swimlane.request(
                'get',
                '/app/{}'.format(appID),
            )

            self.apps_objects[appID] = json.loads(appdetail_response.text)

        if kwargs.pop('fieldsOnly', False):
            return self.apps_objects[appID]['fields']

        if kwargs.pop('layoutOnly', False):
            return self.apps_objects[appID]['layout']

        return self.apps_objects[appID]

    def validateAsset(self, byID = None, byName = None):
        if byID is not None:
            return self.asset_dictionary_id.get(byID, dict())

        if byName is not None:
            return self.asset_dictionary_name.get(byName,dict())

    def validateApp(self, byID = None, byName = None):
        if byID is not None:
            return self.lookupLabel(self.apps_dictionary, byValue=byID)

        if byName is not None:
            return self.lookupLabel(self.apps_dictionary, byKey=byName)

    def validateField(self, field_dictionary, byID = None, byName = None):
        if byID is not None:
            return self.lookupLabel(field_dictionary, byValue=byID)

        if byName is not None:
            return self.lookupLabel(field_dictionary, byKey=byName)

    def validateTask(self, byID = None, byName = None):
        if byID is not None:
            return self.lookupLabel(self.task_dictionary, byValue=byID)

        if byName is not None:
            return self.lookupLabel(self.task_dictionary, byKey=byName)

    def validateRole(self, byID = None, byName = None):
        if byID is not None:
            return self.lookupLabel(self.roles_dictionary, byValue=byID)

        if byName is not None:
            return self.lookupLabel(self.roles_dictionary, byKey=byName)

    def lookupLabel(self, lookup_dictionary, byValue=None, byKey=None):

        if byValue is not None:
            for key, value in list(lookup_dictionary.items()):
                if byValue == value['id']:
                    return key

        if byKey is not None:
            if byKey in lookup_dictionary:
                return lookup_dictionary[byKey]['id']

        return False
