import requests
from typing import Optional
from vesselapi.models import operations
from . import utils

class EngTasks:
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

    
    def complete(self, request: operations.PostCompleteEngagementTaskRequest) -> operations.PostCompleteEngagementTaskResponse:
        r"""Complete Task
        Complete a task.
        """
        
        base_url = self._server_url
        
        url = base_url.removesuffix("/") + "/engagement/task/complete"
        
        headers = {}
        req_content_type, data, json, files = utils.serialize_request_body(request)
        if req_content_type != "multipart/form-data" and req_content_type != "multipart/mixed":
            headers["content-type"] = req_content_type
        
        client = self._security_client
        
        r = client.request("POST", url, data=data, json=json, files=files, headers=headers)
        content_type = r.headers.get("Content-Type")

        res = operations.PostCompleteEngagementTaskResponse(status_code=r.status_code, content_type=content_type)
        
        if r.status_code == 200:
            if utils.match_content_type(content_type, "application/json"):
                out = utils.unmarshal_json(r.text, Optional[operations.PostCompleteEngagementTaskResponseBody])
                res.response_body = out

        return res

    
    def create(self, request: operations.PostEngagementTaskRequest) -> operations.PostEngagementTaskResponse:
        r"""Create Task
        Create a new task.
        """
        
        base_url = self._server_url
        
        url = base_url.removesuffix("/") + "/engagement/task"
        
        headers = {}
        req_content_type, data, json, files = utils.serialize_request_body(request)
        if req_content_type != "multipart/form-data" and req_content_type != "multipart/mixed":
            headers["content-type"] = req_content_type
        
        client = self._security_client
        
        r = client.request("POST", url, data=data, json=json, files=files, headers=headers)
        content_type = r.headers.get("Content-Type")

        res = operations.PostEngagementTaskResponse(status_code=r.status_code, content_type=content_type)
        
        if r.status_code == 200:
            if utils.match_content_type(content_type, "application/json"):
                out = utils.unmarshal_json(r.text, Optional[operations.PostEngagementTaskResponseBody])
                res.response_body = out

        return res

    
    def find(self, request: operations.GetOneEngagementTaskRequest) -> operations.GetOneEngagementTaskResponse:
        r"""Get Task
        Retrieve a Task by Id.
        """
        
        base_url = self._server_url
        
        url = base_url.removesuffix("/") + "/engagement/task"
        
        query_params = utils.get_query_params(request.query_params)
        
        client = self._security_client
        
        r = client.request("GET", url, params=query_params)
        content_type = r.headers.get("Content-Type")

        res = operations.GetOneEngagementTaskResponse(status_code=r.status_code, content_type=content_type)
        
        if r.status_code == 200:
            if utils.match_content_type(content_type, "application/json"):
                out = utils.unmarshal_json(r.text, Optional[operations.GetOneEngagementTaskResponseBody])
                res.response_body = out

        return res

    
    def list(self, request: operations.GetAllEngagementTasksRequest) -> operations.GetAllEngagementTasksResponse:
        r"""Get All Tasks
        Retrieve all Tasks
        """
        
        base_url = self._server_url
        
        url = base_url.removesuffix("/") + "/engagement/tasks"
        
        query_params = utils.get_query_params(request.query_params)
        
        client = self._security_client
        
        r = client.request("GET", url, params=query_params)
        content_type = r.headers.get("Content-Type")

        res = operations.GetAllEngagementTasksResponse(status_code=r.status_code, content_type=content_type)
        
        if r.status_code == 200:
            if utils.match_content_type(content_type, "application/json"):
                out = utils.unmarshal_json(r.text, Optional[operations.GetAllEngagementTasksResponseBody])
                res.response_body = out

        return res

    
    def update(self, request: operations.PutEngagementTaskRequest) -> operations.PutEngagementTaskResponse:
        r"""Update Task
        Update an existing Task.
        """
        
        base_url = self._server_url
        
        url = base_url.removesuffix("/") + "/engagement/task"
        
        headers = {}
        req_content_type, data, json, files = utils.serialize_request_body(request)
        if req_content_type != "multipart/form-data" and req_content_type != "multipart/mixed":
            headers["content-type"] = req_content_type
        
        client = self._security_client
        
        r = client.request("PATCH", url, data=data, json=json, files=files, headers=headers)
        content_type = r.headers.get("Content-Type")

        res = operations.PutEngagementTaskResponse(status_code=r.status_code, content_type=content_type)
        
        if r.status_code == 200:
            if utils.match_content_type(content_type, "application/json"):
                out = utils.unmarshal_json(r.text, Optional[operations.PutEngagementTaskResponseBody])
                res.response_body = out

        return res

    