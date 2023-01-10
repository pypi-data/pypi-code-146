import requests
from typing import Optional
from vesselapi.models import operations
from . import utils

class EngContacts:
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

    
    def create(self, request: operations.PostEngagementContactRequest) -> operations.PostEngagementContactResponse:
        r"""Create Contact
        Create a new contact.
        """
        
        base_url = self._server_url
        
        url = base_url.removesuffix("/") + "/engagement/contact"
        
        headers = {}
        req_content_type, data, json, files = utils.serialize_request_body(request)
        if req_content_type != "multipart/form-data" and req_content_type != "multipart/mixed":
            headers["content-type"] = req_content_type
        
        client = self._security_client
        
        r = client.request("POST", url, data=data, json=json, files=files, headers=headers)
        content_type = r.headers.get("Content-Type")

        res = operations.PostEngagementContactResponse(status_code=r.status_code, content_type=content_type)
        
        if r.status_code == 200:
            if utils.match_content_type(content_type, "application/json"):
                out = utils.unmarshal_json(r.text, Optional[operations.PostEngagementContactResponseBody])
                res.response_body = out

        return res

    
    def find(self, request: operations.GetOneEngagementContactRequest) -> operations.GetOneEngagementContactResponse:
        r"""Get Contact
        Retrieve a Contact by Id.
        """
        
        base_url = self._server_url
        
        url = base_url.removesuffix("/") + "/engagement/contact"
        
        query_params = utils.get_query_params(request.query_params)
        
        client = self._security_client
        
        r = client.request("GET", url, params=query_params)
        content_type = r.headers.get("Content-Type")

        res = operations.GetOneEngagementContactResponse(status_code=r.status_code, content_type=content_type)
        
        if r.status_code == 200:
            if utils.match_content_type(content_type, "application/json"):
                out = utils.unmarshal_json(r.text, Optional[operations.GetOneEngagementContactResponseBody])
                res.response_body = out

        return res

    
    def list(self, request: operations.GetAllEngagementContactsRequest) -> operations.GetAllEngagementContactsResponse:
        r"""Get All Contacts
        Retrieve all Contacts
        """
        
        base_url = self._server_url
        
        url = base_url.removesuffix("/") + "/engagement/contacts"
        
        query_params = utils.get_query_params(request.query_params)
        
        client = self._security_client
        
        r = client.request("GET", url, params=query_params)
        content_type = r.headers.get("Content-Type")

        res = operations.GetAllEngagementContactsResponse(status_code=r.status_code, content_type=content_type)
        
        if r.status_code == 200:
            if utils.match_content_type(content_type, "application/json"):
                out = utils.unmarshal_json(r.text, Optional[operations.GetAllEngagementContactsResponseBody])
                res.response_body = out

        return res

    
    def update(self, request: operations.PutEngagementContactRequest) -> operations.PutEngagementContactResponse:
        r"""Update Contact
        Update an existing Contact.
        """
        
        base_url = self._server_url
        
        url = base_url.removesuffix("/") + "/engagement/contact"
        
        headers = {}
        req_content_type, data, json, files = utils.serialize_request_body(request)
        if req_content_type != "multipart/form-data" and req_content_type != "multipart/mixed":
            headers["content-type"] = req_content_type
        
        client = self._security_client
        
        r = client.request("PATCH", url, data=data, json=json, files=files, headers=headers)
        content_type = r.headers.get("Content-Type")

        res = operations.PutEngagementContactResponse(status_code=r.status_code, content_type=content_type)
        
        if r.status_code == 200:
            if utils.match_content_type(content_type, "application/json"):
                out = utils.unmarshal_json(r.text, Optional[operations.PutEngagementContactResponseBody])
                res.response_body = out

        return res

    