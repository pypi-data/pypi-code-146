from .cosmos_connection import CosmosConnection

class FetchDetails():
    
    def __init__(self, platform_db, host, masterKey, tenant_name=None):
        self.platform_db = platform_db
        self.host = host
        self.masterKey = masterKey
        self.tenant_name = tenant_name
        self.client = CosmosConnection(host=host,master_key=masterKey)

    def cosmos_retrieve(self, host, masterKey, database_name, container_name, query):
        """
            Executes the given query on the given container of the specified database
        """
        database = self.client.set_database(database_name)
        container = self.client.set_container(container_name)
        cosmos_item_list = self.client.query(query)
        return cosmos_item_list

    def get_conf(self):
        """
            Retrieves the storage settings of the tenant
        """
        query="Select * from d where d.name = '"+self.tenant_name+"'"
        tenant_info = self.cosmos_retrieve(self.host, self.masterKey, self.platform_db, 'Tenants', query)
        query='SELECT * FROM d WHERE d.type="Configuration"'
        configuration_info = self.cosmos_retrieve(self.host, self.masterKey, self.platform_db, 'Settings', query)
        
        if(tenant_info[0]["isSkyPointDefaultSettings"]):
            storage_account_key=configuration_info[0]['settings']['AccountKey']
            storage_account_name=configuration_info[0]['settings']['AccountName']
            storage_container_name=configuration_info[0]['settings']['ContainerName']
            tenant_id = configuration_info[0]['settings']['DefaultDatabricksADLSGen2AppTenantId']
            app_id = configuration_info[0]['settings']['DefaultDatabricksADLSGen2AppId']
            app_key = configuration_info[0]['settings']['DefaultDatabricksADLSGen2AppSecret']
        else:
            storage_account_key=tenant_info[0]["appSetting"]["azureDataLakeGen2Settings"]["accountKey"]
            storage_account_name=tenant_info[0]["appSetting"]["azureDataLakeGen2Settings"]["accountName"]
            storage_container_name=tenant_info[0]["appSetting"]["azureDataLakeGen2Settings"]["containerName"]
            databricksADLSGen2AppSettings = tenant_info[0]["appSetting"]["databricksADLSGen2AppSettings"]
            tenant_id = databricksADLSGen2AppSettings['tenantId']
            app_id = databricksADLSGen2AppSettings['appId']
            app_key = databricksADLSGen2AppSettings['appSecret']
        
        return storage_account_key, storage_account_name, storage_container_name, tenant_id, app_id, app_key