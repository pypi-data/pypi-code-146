import logging, json, os, traceback
from typing import Optional


from .databricks_sql import DatabricksSql
from .DynamicCosmosRetrieve import DynamicCosmosRetrieve
from .cosmos_connection import CosmosConnection
import re

class TenantLakehouseSQL():

    def __init__(self, tenant_id, tenant_name, instance_id):
        self.tenant_id = tenant_id
        self.tenant_name = tenant_name
        self.instance_id = instance_id
        self.connection_details_doc = None

    def createQualifiedTableName(self, tenant_name, instance_name, dataflow_name, entity_name, warehouseType, catalog_name = "None"):
        table_name = re.sub('[^A-Za-z0-9_]+','', entity_name)
        cleaned_source_name = re.sub('[^A-Za-z0-9_]+','', dataflow_name)
        if dataflow_name != None and dataflow_name != 'DatabricksSQLWarehouse':
            table_name = cleaned_source_name + "_" + table_name 
        schema_name = tenant_name.lower() + "_" + instance_name.lower()
        qualified_name = schema_name + "." + table_name

        if(warehouseType == "Unity"):
            if(catalog_name == "None"):
                catalog_name = tenant_name + "_" + instance_name + "_main"

            qualified_name = catalog_name + "." + qualified_name
        else:
            qualified_name = "hive_metastore" + "." + qualified_name
        return qualified_name

    def queryLakehouse(self, sql_query, isArrow = False, is_admin = False):
    
        if(self.connection_details_doc is None):
            kv_client_id = os.environ['KV_CLIENT_ID']
            kv_client_secret = os.environ['KV_CLIENT_SECRET']
            kv_tenant_id = os.environ['KV_TENANT_ID']
            key_vault_name = os.environ['KV_NAME']
    
            kv_func_url_key = os.environ['KV_FUNC_URL_TENANTID_KEY']
            kv_func_master_key = os.environ['KV_FUNC_TENANTID_MASTER_KEY']
            obj = DynamicCosmosRetrieve(kv_client_id, kv_client_secret,
                                    kv_tenant_id, key_vault_name, kv_func_url_key, kv_func_master_key)
            obj.get_response(self.tenant_id)
            cosmos_details = obj.get_cosmos_details()
            tenant_cosmos_host, tenant_cosmos_master_key = cosmos_details[
                'cosmos_host'], cosmos_details['cosmos_master_key']
            cosmos_tenant_client = CosmosConnection(
                host=tenant_cosmos_host, master_key=tenant_cosmos_master_key)

            cosmos_tenant_client.set_database(self.tenant_name)
            cosmos_tenant_client.set_container('Operations')

            documentTypeInstanceId = f'LakehouseSQL-{self.instance_id}'
            query_str = "select * from Operations o where o.documentTypeInstanceId='{}'".format(documentTypeInstanceId)
            result = cosmos_tenant_client.query(query_str)
            self.connection_details_doc = result[0]

        sql_endpoint_details = self.connection_details_doc['sqlEndpointDetails']
        server_hostname = sql_endpoint_details['serverHostname']
        http_path = sql_endpoint_details['httpPath']

        #check if admin pat required
        if is_admin==True:
            pat = os.environ['default_pat']
        else:
            pat = self.connection_details_doc['personalAccessToken']

        logging.info('Connecting to Databricks SQL to execute sql query.')
        databricksSql = DatabricksSql()

        databricksSql.connect(server_hostname=server_hostname, http_path=http_path, pas=pat)
        logging.debug('Executing SQL query.')
        query_result = databricksSql.query(sql_query)
        return query_result

    def getLakehouseSqlCursor(self, isArrow = False):
    
        if(self.connection_details_doc is None):
            kv_client_id = os.environ['KV_CLIENT_ID']
            kv_client_secret = os.environ['KV_CLIENT_SECRET']
            kv_tenant_id = os.environ['KV_TENANT_ID']
            key_vault_name = os.environ['KV_NAME']
    
            kv_func_url_key = os.environ['KV_FUNC_URL_TENANTID_KEY']
            kv_func_master_key = os.environ['KV_FUNC_TENANTID_MASTER_KEY']
            obj = DynamicCosmosRetrieve(kv_client_id, kv_client_secret,
                                    kv_tenant_id, key_vault_name, kv_func_url_key, kv_func_master_key)
            obj.get_response(self.tenant_id)
            cosmos_details = obj.get_cosmos_details()
            tenant_cosmos_host, tenant_cosmos_master_key = cosmos_details[
                'cosmos_host'], cosmos_details['cosmos_master_key']
            cosmos_tenant_client = CosmosConnection(
                host=tenant_cosmos_host, master_key=tenant_cosmos_master_key)

            cosmos_tenant_client.set_database(self.tenant_name)
            cosmos_tenant_client.set_container('Operations')

            documentTypeInstanceId = f'LakehouseSQL-{self.instance_id}'
            query_str = "select * from Operations o where o.documentTypeInstanceId='{}'".format(documentTypeInstanceId)
            result = cosmos_tenant_client.query(query_str)
            self.connection_details_doc = result[0]

        sql_endpoint_details = self.connection_details_doc['sqlEndpointDetails']
        server_hostname = sql_endpoint_details['serverHostname']
        http_path = sql_endpoint_details['httpPath']
        pat = self.connection_details_doc['personalAccessToken']

        logging.info('Connecting to Databricks SQL to execute sql query.')
        databricksSql = DatabricksSql()

        databricksSql.connect(server_hostname=server_hostname, http_path=http_path, pas=pat)
        logging.debug('Executing SQL query.')
        cursor = databricksSql.get_cursor()
        return cursor        

    def getSharedLakehouseSqlCursor(self, isArrow = False):
        logging.info('Connecting to Databricks SQL to execute sql query.')
        databricksSql = DatabricksSql()

        server_hostname = os.environ['default_server_hostname']
        http_path = os.environ['shared_warehouse_http_path']
        pat = os.environ['default_pat']

        databricksSql.connect(server_hostname=server_hostname, http_path=http_path, pas=pat)
        logging.debug('Executing SQL query.')
        cursor = databricksSql.get_cursor()
        return cursor 