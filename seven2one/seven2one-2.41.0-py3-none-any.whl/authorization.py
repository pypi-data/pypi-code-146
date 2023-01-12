from uuid import uuid4
import requests
import json
import pandas as pd
from loguru import logger

from .utils.ut import Utils

class Authorization:

    def __init__(self, endpoint:str, core:object) -> None:
        global client
        client = core

        self.raiseException = client.raiseException
        self.defaults = core.defaults
        self.structure = core.structure
        self.scheme = core.scheme

        self.header = {
            'Authorization': f'Bearer {client.accessToken}',
            'AcceptEncoding': 'deflate',
            'Accept': 'application/json',
            'Content-type': 'application/json',
            }

        self.baseUrl = endpoint

    def roles(self) -> pd.DataFrame:
        """
        Returns a DataFrame of available roles
        """

        url = f'{self.baseUrl}/roles'
        response = requests.get(url=url, headers=self.header)
        return AuthUtils.handleResponse(self, response)

    def rules(self) -> pd.DataFrame:
        """
        Returns a DataFrame of available rules
        """

        url = f'{self.baseUrl}/rules'
        response = requests.get(url=url, headers=self.header)
        return AuthUtils.handleResponse(self, response)

    def users(self) -> pd.DataFrame:
        """
        Returns a DataFrame of available users
        """

        url = f'{self.baseUrl}/users'
        response = requests.get(url=url, headers=self.header)
        return AuthUtils.handleResponse(self, response)

    def userGroups(self) -> pd.DataFrame:
        """
        Returns a DataFrame of available users
        """

        url = f'{self.baseUrl}/usergroups'
        response = requests.get(url=url, headers=self.header)
        return AuthUtils.handleResponse(self, response)

    def createRole(
        self,
        inventoryName:str, 
        roleName:str,
        userGroups:list=None, 
        objectPermissions:list=['Create', 'Delete'], 
        propertiesPermissions:list=['Read', 'Update']
        ) -> None:

        """
        Creates a role and sets all rights to all propertes except references

        Parameters:
        ----------
        inventoryName : str
            The name of the inventory for which the new role authorizes rights.
        roleName : str
            Name of the new role.
        userGroup : list = None
            List of user group names. If None, the role will be created without attaching user groups.
        objectPermissions : list = ['Create', 'Delete']
            Default is 'Create' and 'Delete' to allow creating and deleting items of the specified inventory.
            Other entries are not allowed.
        propertiesPermissions : list = ['Read', 'Update']
            Default is 'Read' and 'Update'. All properties except references will receive 
            the here specified rights. Other entries are not allowed.     
        """

        with logger.contextualize(correlation_id=uuid4()):

            # Parameter validation
            try:
                client.structure[inventoryName]
            except:
                Utils._error(self, f"Unknown inventory '{inventoryName}'")
                return
            
            try:
                roles = self.roles()
                if roleName in list(roles['name']):
                    Utils._error(self, f"Role '{roleName}' already exists.")
                    return
            except:
                pass

            if isinstance(userGroups, str):
                userGroups = [userGroups]

            if userGroups != None:
                dfUserGroups = self.userGroups()
                falseUserGroups = []
                for group in userGroups:
                    if group not in list(dfUserGroups['name']):
                        falseUserGroups.append(group)
                
                if falseUserGroups:
                    Utils._error(self, f"Unknown user group(s) {falseUserGroups}")
                    return

            # Create role
            properties = client.structure[inventoryName]['properties']

            def createPropertyDict(properties):
                propertyList = []
                for _, value in properties.items():
                    p = {}
                    p.setdefault('id',value['propertyId'])
                    p.setdefault('name',value['name'])
                    p.setdefault('nullable',value['nullable'])
                    if (value['type'] != 'reference'):
                        p.setdefault('dataType',value['dataType'])
                    p.setdefault('isArray',value['isArray'])
                    propertyList.append(p)

                return propertyList

            def createPermissionsDict(properties):
                return {'scalarPropertiesPermissions': {key:propertiesPermissions for key in properties}}

            role = {
                'name': roleName,
                'objectPermissions': objectPermissions,
                'rootTypeName': inventoryName,
                'propertiesPermissions': createPermissionsDict(properties),
                'DynamicObjectTypeModel':
                    [
                        {
                            'id':client.structure[inventoryName]['inventoryId'],
                            'name':inventoryName,
                            'isDomainUserType':client.structure[inventoryName]['isDomainUserType'],
                            'scalarProperties': createPropertyDict(properties),
                            'referencedProperties': []
                        }
                    ]
            }
            
            urlRole = f'{self.baseUrl}/roles/'
            responseRole = requests.post(url=urlRole, headers=self.header, data=json.dumps(role))
            if responseRole.status_code not in [200, 204]:
                Utils._error(self, f"Status: {responseRole.status_code}, {json.loads(responseRole.content)}")
                return
            logger.info(f"Role {roleName} created.")

            # Create rules
            if userGroups != None:
                for group in userGroups:
                    rule = {
                        'userGroup':group,
                        'roleRootType': inventoryName,
                        'role':roleName,
                    }
                    urlRule = f'{self.baseUrl}/rules/'
                    responseRule = requests.post(url=urlRule, headers=self.header, data=json.dumps(rule))
                    if responseRule.status_code not in [200, 204]:
                        Utils._error(self, f"Status: {responseRule.status_code}, {json.loads(responseRule.content)}")
                        return
                    else:
                        logger.info(f"Rule for {roleName} and user group {group} created.")

            return

    def deleteRole(self, role:str) -> None:
        """
        Deletes a role and all related rules.
        """

        with logger.contextualize(correlation_id=uuid4()):

            # Get Ids of roles and rules
            roles = self.roles().set_index('name')
            roleId = roles.loc[role,'id']

            rules = self.rules()
            rules = rules.set_index('role')
            try:
                ruleIds = rules.loc[role,'id']
            except:
                ruleIds = []
            if not isinstance(ruleIds, str):
                ruleIds = list(ruleIds)
            else:
                ruleIds = [ruleIds]

            # First delete rules
            if ruleIds:
                for ruleId in ruleIds:
                    url = f'{self.baseUrl}/rules/{ruleId}'
                    response = requests.delete(url=url, headers=self.header)
                    if response.status_code not in [200, 204]:
                        Utils._error(self, f"Rule of role {roleId} could not be deleted. (Status {response.status_code})")
                        return 
                    else:
                        logger.info(f"Rule of role {role} with id {ruleId} has been deleted.")     

            # After all rules have been deleted, delete the role
            url = f'{self.baseUrl}/roles/{roleId}'
            response = requests.delete(url=url, headers=self.header)
            if response.status_code not in [200, 204]:
                Utils._error(self, f"Role could not be deleted. (Status {response.status_code})")        
            else:
                logger.info(f"Role {role} with id {roleId} has been deleted.")   
                return


class AuthUtils:

    def handleResponse(client, response:object):
        if response.status_code not in [200, 204]:
            Utils._error(client, f"Status: {response.status_code}, {json.loads(response.content)}")        
        else:
            result = json.loads(response.content)
            return pd.json_normalize(result)