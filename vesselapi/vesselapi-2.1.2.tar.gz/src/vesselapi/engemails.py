import requests
from typing import Optional
from vesselapi.models import operations
from . import utils

class EngEmails:
    _client: requests.Session
    _security_client: requests.Session
    _server_url: str
    _language: str
    _sdk_version: str
    _gen_version: str

    def __init__(self, client: requests.Session, security_client: requests.Session, server_url: str, language: str, sdk_version: str, gen_version: str) -> None:
        self._client = client
        self._security_client = security_client
        self._server_url = server_url
        self._language = language
        self._sdk_version = sdk_version
        self._gen_version = gen_version

    
    def find(self, request: operations.GetOneEngagementEmailRequest) -> operations.GetOneEngagementEmailResponse:
        r"""Get Email
        Retrieve a Email by Id.
        """
        
        base_url = self._server_url
        
        url = base_url.removesuffix("/") + "/engagement/email"
        
        query_params = utils.get_query_params(request.query_params)
        
        client = self._security_client
        
        r = client.request("GET", url, params=query_params)
        content_type = r.headers.get("Content-Type")

        res = operations.GetOneEngagementEmailResponse(status_code=r.status_code, content_type=content_type)
        
        if r.status_code == 200:
            if utils.match_content_type(content_type, "application/json"):
                out = utils.unmarshal_json(r.text, Optional[operations.GetOneEngagementEmailResponseBody])
                res.response_body = out

        return res

    
    def list(self, request: operations.GetAllEngagementEmailsRequest) -> operations.GetAllEngagementEmailsResponse:
        r"""Get All Emails
        Retrieve all Emails
        """
        
        base_url = self._server_url
        
        url = base_url.removesuffix("/") + "/engagement/emails"
        
        query_params = utils.get_query_params(request.query_params)
        
        client = self._security_client
        
        r = client.request("GET", url, params=query_params)
        content_type = r.headers.get("Content-Type")

        res = operations.GetAllEngagementEmailsResponse(status_code=r.status_code, content_type=content_type)
        
        if r.status_code == 200:
            if utils.match_content_type(content_type, "application/json"):
                out = utils.unmarshal_json(r.text, Optional[operations.GetAllEngagementEmailsResponseBody])
                res.response_body = out

        return res

    