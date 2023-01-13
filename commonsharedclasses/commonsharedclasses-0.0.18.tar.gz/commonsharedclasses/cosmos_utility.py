from commonsharedclasses import CosmosConnection
from commonsharedclasses import DynamicCosmosRetrieve
from cachetools import cached, TTLCache
import os,logging

class CosmosUtility():
    cache_tenant = TTLCache(maxsize=500, ttl=60)
    cache_platform = TTLCache(maxsize=100, ttl=300)
    def __init__(self):
        pass

    def tenant_query(self,tenant_name,query,database_name,container_name):
        return CosmosUtility.tenant_query_cached(tenant_name,query,database_name,container_name)

    def platform_db_query(self,query,platform_db_name,platform_db_container):
        return CosmosUtility.platform_db_query_cached(query,platform_db_name,platform_db_container)

    @cached(cache_tenant)
    def tenant_query_cached(tenant_name,query,database_name,container_name):
        ##  DYNAMIC COSMOS ##
        kv_client_id = os.environ['KV_CLIENT_ID']
        kv_client_secret = os.environ['KV_CLIENT_SECRET']
        kv_tenant_id = os.environ['KV_TENANT_ID']
        key_vault_name = os.environ['KV_NAME']
        if "-" in tenant_name:
            kv_func_url_key = os.environ['KV_FUNC_URL_TENANTID_KEY']
            kv_func_master_key = os.environ['KV_FUNC_TENANTID_MASTER_KEY']
        else:
            kv_func_url_key = os.environ['KV_FUNC_URL_TENANT_KEY']
            kv_func_master_key = os.environ['KV_FUNC_TENANT_MASTER_KEY']
        obj = DynamicCosmosRetrieve(kv_client_id, kv_client_secret,
                                    kv_tenant_id, key_vault_name, kv_func_url_key, kv_func_master_key)
        logging.debug('Dynamic cosmos query started')
        obj.get_response(tenant_name)
        logging.debug('Dynamic cosmos query completed')
        cosmos_details = obj.get_cosmos_details()
        tenant_cosmos_host, tenant_cosmos_master_key = cosmos_details[
            'cosmos_host'], cosmos_details['cosmos_master_key']
        cosmos_tenant_client = CosmosConnection(
            host=tenant_cosmos_host, master_key=tenant_cosmos_master_key)

        cosmos_tenant_client.set_database(database_name)
        cosmos_tenant_client.set_container(container_name)
        logging.debug('tenant_query query started: '+query)
        result = cosmos_tenant_client.query(query)
        logging.debug('tenant_query query completed: '+query)
        return result

    @cached(cache_platform)
    def platform_db_query_cached(query,platform_db_name,platform_db_container):
        cosmos_host = os.environ['COSMOS_PLATFORM_HOST']
        cosmos_master_key = os.environ['COSMOS_PLATFORM_KEY']
        cosmos_client = CosmosConnection(
            host=cosmos_host, master_key=cosmos_master_key)
        cosmos_client.set_database(platform_db_name)
        cosmos_client.set_container(platform_db_container)
        logging.debug('platform_db_query query started: '+query)
        result = cosmos_client.query(query)
        logging.debug('platform_db_query query completed: '+query)
        return result