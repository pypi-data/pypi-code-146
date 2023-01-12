import requests
import json
from pyspark.sql import SparkSession
spark = SparkSession.getActiveSession()
from odap.common.databricks import resolve_dbutils
dbutils = resolve_dbutils()

auth_header = {"authorization": "Bearer dapie1a45d7206d40455f818954f17ee5e43-2"}
dbx_url = "https://adb-823568827312066.6.azuredatabricks.net"
service_account_name = dbutils.notebook.entry_point.getDbutils().notebook().getContext().userName().get()

def create_scope(user_name):
    scope_name = user_name.split('@')[0]
    create_scope_api = f"{dbx_url}/api/2.0/secrets/scopes/create"
    create_scope_data = json.dumps({'scope': scope_name})
    response = requests.post(create_scope_api, headers=auth_header, data=create_scope_data)
    response.content

def put_user_acl(user_name):
    scope_name = user_name.split('@')[0]
    put_acl_api = f"{dbx_url}/api/2.0/secrets/acls/put"
    put_acl_data = json.dumps({
        "scope": scope_name,
        "principal": user_name,
        "permission": "MANAGE"
    })
    response = requests.post(put_acl_api, headers = auth_header, data= put_acl_data)
    response.content

def remove_service_account(user_name):
    scope_name = user_name.split('@')[0]
    delete_acl_api = f"{dbx_url}/api/2.0/secrets/acls/delete"
    delete_acl_data = json.dumps({
      "scope": scope_name,
      "principal": service_account_name
    })
    response = requests.post(delete_acl_api, headers = auth_header, data= delete_acl_data)
    response.content

def get_secret_name(secret):
    return secret.name

def create_scope_if_not_exists():
    df = spark.sql("SHOW USERS")
    df_list = df.rdd.map(lambda x: x.name).collect()
    df_list_scope_names = [item for items in df_list for item in items.split('@')][::2]

    list_of_scopes = list(map(get_secret_name, dbutils.secrets.listScopes()))

    users_to_create_scopes = list(set(df_list_scope_names) - set(list_of_scopes))

    for user_name in users_to_create_scopes:
        create_scope(user_name)
        put_user_acl(user_name)
        remove_service_account(user_name)



