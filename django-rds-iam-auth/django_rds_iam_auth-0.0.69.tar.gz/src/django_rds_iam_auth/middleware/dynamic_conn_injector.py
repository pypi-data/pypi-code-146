import threading

import boto3
import jwt
from django_rds_iam_auth.aws.utils.aws_access_heper import CredentialsManager

from django_rds_iam_auth.middleware.jwt_exposer import local
from django.db import connections


class ConnectionInjector(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, middleware_mode=True, static_response=None):
        token = None
        try:
            token = jwt.decode(local.ibrag_idToken, verify=False)
            if not token or not isinstance(token, dict) or 'sub' not in token:
                raise Exception('User is not authenticated')
            dynamic_database = connections.databases.get('default', None).copy()
            if not dynamic_database:
                raise Exception('No Database configuration exists')
            if token.get('sub') in connections.databases:
                raise Exception('Connection Already Exist')
            try:
                rds_cred_manager = CredentialsManager(jwt_token=local.ibrag_access_token, id_token=local.ibrag_idToken,
                                                      identity_pool_id=local.ibrag_IdentityPoolId,
                                                      user_pool_id=local.ibrag_UserPoolId, account_id=local.ibrag_accountId)
                rds_creds = rds_cred_manager.get_credentials()
                rds_creds.pop('expiry_time')
                if not rds_creds:
                    raise Exception('no cached credentials')
                rds_boto3_session = boto3.session.Session(**rds_creds)
                boto3.DEFAULT_SESSION = rds_boto3_session
                rds_client = rds_boto3_session.client("rds",**rds_creds)
            except Exception as ex:
                rds_client =  boto3.DEFAULT_SESSION.resource("rds")

            dynamic_database['id'] = token.get('sub', None)
            dynamic_database['USER'] = token.get('sub', None)
            dynamic_database['PASSWORD'] = rds_client.generate_db_auth_token(
                DBHostname=dynamic_database['HOST'],
                Port=dynamic_database.get("port", 5432),
                DBUsername=token.get('sub', None),
            )
            connections.databases[dynamic_database['id']] = dynamic_database
        except Exception as extr:
            pass

        if not middleware_mode:
            return self.get_response(static_response)
        response = self.get_response(request)
        if not token or not isinstance(token, dict) or 'sub' not in token:
            return response
        try:
            connections.databases.pop(token.get('sub', None), None)
        except Exception as ex:
            pass

        return response

    def process_response(self,request, response):
        t=3

    def process_exception(self, request, exception):
        try:
            token = jwt.decode(local.ibrag_idToken, verify=False)
        except:
            return None
        if not token or not isinstance(token, dict) or 'sub' not in token:
            return None
        try:
            connections.databases.pop(token.get('sub', None), None)
        except Exception as ex:
            return None
        return None
