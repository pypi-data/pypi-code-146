import jwt
from django.conf import settings
from django_rds_iam_auth.middleware.jwt_exposer import local


class JWTInjector(object):

    def __call__(self, **kwargs):
        # user_data = jwt.decode(id_token, verify=False)
        if 'IdToken' not in kwargs or 'AccessToken' not in kwargs or 'IPI' not in kwargs or 'UPI' not in kwargs:
            raise Exception('missing information')
        local.ibrag_access_token = kwargs['AccessToken']
        local.ibrag_idToken = kwargs['IdToken']
        local.ibrag_IdentityPoolId = kwargs['IPI']
        local.ibrag_UserPoolId = kwargs['UPI']
        local.ibrag_tenant = kwargs['ttn']
        local.ibrag_accountId = settings.AWS_ACCOUNT_ID