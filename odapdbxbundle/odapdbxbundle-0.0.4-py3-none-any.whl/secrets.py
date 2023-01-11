from odapdbxbundle.common.databricks import resolve_dbutils, get_host, get_token, get_username
from pyspark.sql import SparkSession

import json
import requests


def create_scope(user_name):
    dbx_token = get_token()
    auth_header = {"authorization": f"Bearer {dbx_token}"}
    dbx_url = get_host()
    scope_name = user_name.split('@')[0]        # scope name is the first half of user name before @
    create_scope_api = f"{dbx_url}/api/2.0/secrets/scopes/create"
    create_scope_data = json.dumps({'scope': scope_name})
    requests.post(create_scope_api, headers=auth_header, data=create_scope_data)


def put_user_acl(user_name):
    dbx_token = get_token()
    auth_header = {"authorization": f"Bearer {dbx_token}"}
    dbx_url = get_host()
    scope_name = user_name.split('@')[0]
    put_acl_api = f"{dbx_url}/api/2.0/secrets/acls/put"
    put_acl_data = json.dumps({
        "scope": scope_name,
        "principal": user_name,
        "permission": "MANAGE"
    })
    requests.post(put_acl_api, headers = auth_header, data= put_acl_data)


def remove_service_account(user_name):
    if user_name != get_username():
        scope_name = user_name.split('@')[0]
        dbx_token = get_token()
        auth_header = {"authorization": f"Bearer {dbx_token}"}
        dbx_url = get_host()
        delete_acl_api = f"{dbx_url}/api/2.0/secrets/acls/delete"
        delete_acl_data = json.dumps({
          "scope": scope_name,
          "principal": get_username()
        })
        requests.post(delete_acl_api, headers = auth_header, data= delete_acl_data)


def get_secret_name(secret):
    return secret.name


def get_scope_name():
    username = get_username()
    return username.split('@')[0]


def create_scope_if_not_exists():
    dbutils = resolve_dbutils()
    spark = SparkSession.getActiveSession()
    df = spark.sql("SHOW USERS")
    df_list_of_users = df.rdd.map(lambda x: x.name).collect()

    scope_names = list(map(lambda x: x.name, dbutils.secrets.listScopes()))

    for user_name in df_list_of_users:
        scope_name = user_name.split('@')[0]
        if scope_name not in scope_names:
            create_scope(user_name)
            put_user_acl(user_name)
            remove_service_account(user_name)


def add_secret(secret_name, secret_value, secret_scope=None):
    if secret_scope is None:
        secret_scope = get_scope_name()
    dbx_token = get_token()
    auth_header = {"authorization": f"Bearer {dbx_token}"}
    dbx_url = get_host()
    create_scope_api = f"{dbx_url}/api/2.0/secrets/put"
    put_secret_data = json.dumps({'scope': secret_scope, 'key': secret_name, 'string_value': secret_value})
    return requests.post(create_scope_api, headers=auth_header, data=put_secret_data).content


