from searchunify.utils.http_client.request_handler import RequestManager
from searchunify.core.auth.auth_header_type import get_auth_header
from searchunify.utils.constants.constants import AuthVariables
from searchunify.utils.apis.apis import Apis
import json

API = Apis.get_apis('search')
AUTH_VARS = AuthVariables()

class Search:
    def get_search_results(**payload):
        url = AUTH_VARS.INSTANCE + API['searchResults']
        payload = json.dumps(payload)
        response = RequestManager.http_request(
            "POST", url, headers=get_auth_header(), data=payload)
        return response
