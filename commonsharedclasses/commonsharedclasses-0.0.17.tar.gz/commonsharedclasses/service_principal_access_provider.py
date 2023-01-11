from time import sleep
from msgraph.core import GraphClient
from azure.identity import ClientSecretCredential
import requests as req
from msal import ConfidentialClientApplication
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from retrying import retry
from .DynamicCosmosRetrieve import DynamicCosmosRetrieve
from .cosmos_connection import CosmosConnection
import os

class ServicePrincipalAccessProvider:
    
    APP_SUFFIX = "App"
    USER_SUFFIX = "User"

    def __init__(self, tenant_name, principal_client_id, principal_secret, principal_tenant_id, dbx_workspace_host, dbx_admin_pat ):
        self.tenant_name = tenant_name
        self.principal_secret = principal_secret
        self.client_id = principal_client_id
        self.principal_tenant_id = principal_tenant_id
        self.dbx_workspace_host = dbx_workspace_host
        self.dbx_admin_pat = dbx_admin_pat
        self.user_access_doc = None
        pass

    def grantAccessToUser(self):
        principal_client_id = self.client_id
        principal_secret = self.principal_secret
        principal_tenant_id = self.principal_tenant_id
        credentials = ClientSecretCredential(
            client_id=principal_client_id,
            client_secret=principal_secret,
            tenant_id= principal_tenant_id)
        
        #checking if service principal already exists
        if self.user_access_doc is None:
            client = GraphClient(credential=credentials)
            #response contains object id, client/app id            
            app_response = self.createApplication(client)
            app_obj_id = app_response['id']
            app_client_id = app_response['appId']

            app_secret = self.createSecret(client, app_obj_id)

            tenant_user_name = self.addAppToDBXWorkspace(app_client_id)
       
        else:
            app_obj_id = self.user_access_doc['app_obj_id']
            app_client_id = self.user_access_doc['app_id']
            app_secret = self.user_access_doc['app_secret']
            tenant_user_name = self.user_access_doc['tenant_user_name']

        app_auth_token = self.authorizeApplicationForDBX(app_client_id, app_secret)

        user_pat, user_pat_id ,pat_creation_time ,pat_expiry_time = self.generateDBXAccessToken(app_auth_token)

        result = {
            'tenant_name': self.tenant_name,
            'tenant_user_name': tenant_user_name,
            'app_auth_token': app_auth_token,
            'pat': user_pat,
            'pat_id': user_pat_id,
            'pat_creation_time': pat_creation_time,
            'pat_expiry_time': pat_expiry_time,
            'app_id': app_client_id,
            'app_obj_id': app_obj_id,
            'app_secret': app_secret
        }

        return result






        

    def createApplication(self, client: GraphClient):

        body = {
            "displayName": self.tenant_name + self.APP_SUFFIX
        }
        response = client.post( "/applications", json = body )
        
        if( response.status_code in [200, 201] ):
            res = response.json()

        return res

    def createSecret(self, client: GraphClient, app_obj_id):
        
        body = {
                "passwordCredential": {
                  "displayName": "MySecretCred"
                }
             }
        
        response = client.post("/applications/{}/addPassword".format(app_obj_id), json=body)
        
        if( response.status_code in [200, 201] ):
            res = response.json()
        else:
            raise Exception(f"creating secret for Service Principal Failed: {response.json()}")

        return res['secretText']

    def addAppToDBXWorkspace(self, app_client_id):
        body = {
             "schemas": [ "urn:ietf:params:scim:schemas:core:2.0:ServicePrincipal" ],
                           "applicationId": app_client_id,
                           "displayName": self.tenant_name + self.USER_SUFFIX,
                                    "entitlements": [
                                        {
                                            "value":"databricks-sql-access"
                                        }
                        ]
                }
        header={'Authorization': 'Bearer ' + self.dbx_admin_pat}
        response = req.request("POST", "https://" + self.dbx_workspace_host + "/api/2.0/preview/scim/v2/ServicePrincipals", headers=header, json=body)
        if( response.status_code in [200, 201] ):
            res1 = response.json()
        else:
            raise Exception("Request for adding Service principal to dbx failed")

        token_authorize_body = {
            "access_control_list": [
                  {
                  "user_name": app_client_id,
                  "permission_level": "CAN_USE"
                  }
              ]
        }

        token_auth_response = req.request("PATCH", "https://" + self.dbx_workspace_host + "/api/2.0/preview/permissions/authorization/tokens",
                                        headers=header, json=token_authorize_body)
        if( token_auth_response.status_code in [200, 201] ):
            res2 = token_auth_response.json()

        else:
            raise Exception("Authorizing Service Principal to use tokens failed")


        return res1['displayName']

    @retry(wait_exponential_multiplier=1000, wait_exponential_max=10000, stop_max_delay=300000)
    def authorizeApplicationForDBX(self, app_client_id, app_secret):

        client = BackendApplicationClient(client_id=app_client_id)
        oauth = OAuth2Session(client=client)
        token = oauth.fetch_token(token_url='https://login.microsoftonline.com/19393f3e-7639-4afe-bd82-ffb6e79b24b3/oauth2/v2.0/token', client_id=app_client_id,
        client_secret=app_secret,scope='2ff814a6-3304-4ab8-85cb-cd0e6f879c1d/.default')
        access_token = token['access_token']
        return access_token

    def generateDBXAccessToken(self, app_auth_token):

        lifetime_seconds = self.config_doc['pat_lifetime_seconds']
        body = {"comment": self.tenant_name + " PAT for LakehouseSQL" , "lifetime_seconds": lifetime_seconds}
        header={'Authorization': 'Bearer ' + app_auth_token}       
        response = req.request("POST",  "https://" + self.dbx_workspace_host + "/api/2.0/token/create",
                headers = header, json=body)
        if( response.status_code in [200, 201] ):
            res2 = response.json()
        else:
            raise Exception("Creation of personal access token failed: " + response.json())

        return res2['token_value'], res2['token_info']['token_id'], res2['token_info']['creation_time'], res2['token_info']['expiry_time']

    def retrieveCosmosDocs(self, tenant_name, instance_id, tenant_id):
        kv_client_id = os.environ['KV_CLIENT_ID']
        kv_client_secret = os.environ['KV_CLIENT_SECRET']
        kv_tenant_id = os.environ['KV_TENANT_ID']
        key_vault_name = os.environ['KV_NAME']
    
        kv_func_url_key = os.environ['KV_FUNC_URL_TENANTID_KEY']
        kv_func_master_key = os.environ['KV_FUNC_TENANTID_MASTER_KEY']
    
        obj = DynamicCosmosRetrieve(kv_client_id, kv_client_secret,
                                    kv_tenant_id, key_vault_name, kv_func_url_key, kv_func_master_key)
        obj.get_response(tenant_id)
        cosmos_details = obj.get_cosmos_details()
        tenant_cosmos_host, tenant_cosmos_master_key = cosmos_details[
            'cosmos_host'], cosmos_details['cosmos_master_key']
        cosmos_tenant_client = CosmosConnection(
            host=tenant_cosmos_host, master_key=tenant_cosmos_master_key)

        cosmos_tenant_client.set_database(tenant_name)
        cosmos_tenant_client.set_container('Operations')

        #fetching user access doc from cosmos
        documentTypeInstanceId = f'LakehouseSQLUserAccess-{instance_id}'
        query_str = "select * from Operations o where o.documentTypeInstanceId='{}'".format(documentTypeInstanceId)
        user_access_doc = cosmos_tenant_client.query(query_str)
        
        #fetching connection details doc from cosmos
        documentTypeInstanceId = f'LakehouseSQL-{instance_id}'
        query_str = "select * from Operations o where o.documentTypeInstanceId='{}'".format(documentTypeInstanceId)
        connection_doc = cosmos_tenant_client.query(query_str)

        #fetching instance specific config details doc from cosmos
        documentTypeInstanceId = f'LakehouseSQLConfig-{instance_id}'
        query_str = "select * from Operations o where o.documentTypeInstanceId='{}'".format(documentTypeInstanceId)
        config_doc = cosmos_tenant_client.query(query_str)
       
        #fetching default config details if instance specific config details doc is not present       
        if len(config_doc)==0:
            host = os.environ['COSMOS_PLATFORM_HOST']
            masterKey = os.environ['COSMOS_PLATFORM_KEY']
            cosmos_connection = CosmosConnection(host, masterKey)
            cosmos_connection.set_database("platformdb")
            cosmos_connection.set_container("Settings")
            query_str = "select * from Settings s where s.name='LakehouseSQLConfig-default'"
            config_doc = cosmos_connection.query(query_str)

        if len(user_access_doc)!=0:
            self.user_access_doc = user_access_doc[0]
        if len(connection_doc)!=0:
            self.connection_doc = connection_doc[0]
        if len(config_doc)!=0:
            self.config_doc = config_doc[0]

        return cosmos_tenant_client





        
        




