import threading
from django.conf import settings

import jwt

local = threading.local()


class JWTExposer(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, is_middlware=True, token_meta_name=None, static_response=None):
        local.ibrag_access_token = request.META.get('HTTP_AUTHORIZATION', None)
        if not is_middlware:
            if token_meta_name is None:
                raise ('custom token injecition atttempted without specifying meta name!')
            local.ibrag_access_token = request.META.get(token_meta_name, None)

        local.ibrag_idToken = request.META.get('HTTP_IDTOKEN', None)
        local.ibrag_IdentityPoolId = request.META.get('HTTP_IPI', None)
        local.ibrag_UserPoolId = request.META.get('HTTP_UPI', None)
        local.ibrag_tenant = request.META.get('HTTP_TTN', None)
        local.ibrag_accountId = settings.AWS_ACCOUNT_ID
        local.ibrag_tenant_id = None
        if local.ibrag_access_token and local.ibrag_access_token.startswith("Bearer"):
            local.ibrag_access_token = str.replace(local.ibrag_access_token, 'Bearer ', '')
            try:
                local.ibrag_tenant_id = jwt.decode(local.ibrag_idToken, verify=False).get('custom:tenant_id', None)
            except jwt.DecodeError:
                pass

        if not is_middlware:
            return self.get_response(static_response)

        response = self.get_response(request)
        return response

