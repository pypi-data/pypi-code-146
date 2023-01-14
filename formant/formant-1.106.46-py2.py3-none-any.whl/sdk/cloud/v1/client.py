from typing import Optional, List, Dict
import ntpath
import os
import requests
import sys
import time
import datetime
from dateutil.tz import tzutc
import copy

FORMANT_REQUEST_ON_DEMAND_DATA_COMMAND_NAME = "formant.demand_data"


def get_current_isodate():
    return datetime.datetime.now(tz=tzutc()).isoformat()


def get_timestamp_str(
    dt,  # type: datetime.datetime
):
    return str(int(dt.timestamp()))


class Client:
    """
    A client for interacting with the Formant Cloud. There are methods for:
    - Ingesting telemetry datapoints for device(s)
    - Query telemetry datapoints
    - Query stream(s) last known value
    - Create intervention requests
    - Create intervention responses
    Requires service account credentials (environment variables):
    - FORMANT_EMAIL
    - FORMANT_PASSWORD
    """

    def __init__(
        self,
        admin_api="https://api.formant.io/v1/admin",
        ingest_api="https://api.formant.io/v1/ingest",
        query_api="https://api.formant.io/v1/queries",
    ):
        self._admin_api = admin_api
        self._ingest_api = ingest_api
        self._query_api = query_api

        self._email = os.getenv("FORMANT_EMAIL")
        self._password = os.getenv("FORMANT_PASSWORD")
        if self._email is None:
            raise ValueError("Missing FORMANT_EMAIL environment variable")
        if self._password is None:
            raise ValueError("Missing FORMANT_PASSWORD environment variable")

        self._headers = {
            "Content-Type": "application/json",
            "App-ID": "formant/python-cloud-sdk",
        }

        self._token = None
        self._token_expiry = 0
        self._organization_id = None
        self._user_id = None

    def get_user_id(self):
        if self._user_id is None:
            self._authenticate()
        return self._user_id

    def get_organization_id(self):
        if self._organization_id is None:
            self._authenticate()
        return self._organization_id

    def ingest(self, params):
        """Administrator credentials required.
        Example ingestion params:
        {
            deviceId: "ced176ab-f223-4466-b958-ff8d35261529",
            name: "engine_temp",
            type: "numeric",
            tags: {"location":"sf"},
            points: [...],
        }
        """

        def call(token):
            headers = self._headers.copy()
            headers["Authorization"] = "Bearer %s" % token
            response = requests.post(
                "%s/batch" % self._ingest_api, headers=headers, json=params
            )
            response.raise_for_status()

        self._authenticate_request(call)

    def query(self, params):
        """Example query params (only start and end time are required):
        {
            start: "2021-01-01T01:00:00.000Z",
            end: "2021-01-01T02:00:00.000Z",
            deviceIds: ["99e8ee37-0a27-4a11-bba2-521facabefa3"],
            names: ["engine_temp"],
            types: ["numeric"],
            tags: {"location":["sf","la"]},
            notNames: ["speed"],
        }
        """

        def call(token):
            headers = self._headers.copy()
            headers["Authorization"] = "Bearer %s" % token
            # enable pagination by default
            # TODO: support for aggregate queries
            query = copy.deepcopy(params)
            nextToken = None if len(query.get("aggregate", "")) > 0 else "true"
            result = {"items": []}
            while True:
                if nextToken is not None:
                    query["next"] = nextToken
                response = requests.post(
                    "%s/queries" % self._query_api, headers=headers, json=query
                )
                response.raise_for_status()
                parsed = response.json()
                nextToken = parsed.get("next")
                result["items"] += parsed["items"]
                if nextToken is None:
                    break
            return result

        return self._authenticate_request(call)

    def query_devices(self, params):
        """Example params to filter on (all optional)
        {
            name: "model00.001",
            tags: {"location":["sf", "la"]},
        }
        """

        def call(token):
            headers = self._headers.copy()
            headers["Authorization"] = "Bearer %s" % token
            response = requests.post(
                "%s/devices/query" % self._admin_api, headers=headers, json=params
            )
            response.raise_for_status()
            return response.json()

        return self._authenticate_request(call)

    def patch_device(self, device_id, params):
        """Example params
        {
            "desiredConfiguration": 43
        }
        """

        def call(token):
            headers = self._headers.copy()
            headers["Authorization"] = "Bearer %s" % token
            response = requests.patch(
                "%s/devices/%s" % (self._admin_api, device_id),
                headers=headers,
                json=params,
            )
            response.raise_for_status()
            return response.json()

        return self._authenticate_request(call)

    def query_stream_current_value(self, params):
        """Example query params (all optional):
        {
            start: "2021-01-01T01:00:00.000Z",
            end: "2021-01-01T02:00:00.000Z",
            deviceIds: ["99e8ee37-0a27-4a11-bba2-521facabefa3"],
            names: ["engine_temp"],
            types: ["numeric"],
            tags: {"location":["sf","la"]},
            notNames: ["speed"],
        }
        """

        def call(token):
            headers = self._headers.copy()
            headers["Authorization"] = "Bearer %s" % token
            response = requests.post(
                "%s/stream-current-value" % self._query_api,
                headers=headers,
                json=params,
            )
            response.raise_for_status()
            return response.json()

        return self._authenticate_request(call)

    def upload_file(self, params):
        """
        Upload a file.

        Example params
        {
            path: "/tmp/model.dat"
        }
        """

        file_name = ntpath.basename(params["path"])
        byte_size = os.path.getsize(params["path"])
        if not (byte_size > 0):
            raise ValueError("File is empty")

        def begin_upload(token):
            headers = self._headers.copy()
            headers["Authorization"] = "Bearer %s" % token
            response = requests.post(
                "%s/files/begin-upload" % self._admin_api,
                headers=headers,
                json={"fileName": file_name, "fileSize": byte_size},
            )
            response.raise_for_status()
            return response.json()

        begin_result = self._authenticate_request(begin_upload)
        part_size = begin_result["partSize"]

        etags = []
        part_index = 0
        with open(params["path"], "rb") as file_obj:
            for part_url in begin_result["partUrls"]:
                file_obj.seek(part_index * part_size)
                part_index = part_index + 1
                data = file_obj.read(part_size)
                response = requests.put(part_url, data=data)
                etags.append(response.headers["etag"])

        def complete_upload(token):
            headers = self._headers.copy()
            headers["Authorization"] = "Bearer %s" % token
            response = requests.post(
                "%s/files/complete-upload" % self._admin_api,
                headers=headers,
                json={
                    "fileId": begin_result["fileId"],
                    "uploadId": begin_result["uploadId"],
                    "eTags": etags,
                },
            )
            response.raise_for_status()

        self._authenticate_request(complete_upload)

        return {
            "file_id": begin_result["fileId"],
        }

    def create_command(self, params):
        """
        Create a command.

        Example params
        {
            deviceId: "99e8ee37-0a27-4a11-bba2-521facabefa3"
            command: "return_to_charge_station"
            parameter: {
                "scrubberTime": "2014-11-03T19:38:34.203Z",
                "value": "A-2",
                "files": [{
                    "id": "eb4a823f-58eb-41d6-9b57-c2113261dbbb",
                    "name": "optional_name1"
                }]
            },
        }

        The "value" and "files" keys are optional.
        """

        def call(token):
            headers = self._headers.copy()
            headers["Authorization"] = "Bearer %s" % token
            response = requests.post(
                "%s/commands" % self._admin_api,
                headers=headers,
                json=params,
            )
            response.raise_for_status()
            return response.json()

        return self._authenticate_request(call)

    def demand_device_data(
        self,
        device_id,  # type: str
        start,  # type: datetime.datetime
        end,  # type: datetime.datetime
    ):
        params = {
            "deviceId": device_id,
            "command": FORMANT_REQUEST_ON_DEMAND_DATA_COMMAND_NAME,
            "organizationId": self._organization_id,
            "parameter": {
                "meta": {
                    "start": get_timestamp_str(start),
                    "end": get_timestamp_str(end),
                },
                "scrubberTime": get_current_isodate(),
            },
        }
        return self.create_command(params)

    def query_commands(self, params):
        """
        Query undelivered commands by device ID.

        Example params
        {
            deviceId: "99e8ee37-0a27-4a11-bba2-521facabefa3",
        }
        """

        def call(token):
            headers = self._headers.copy()
            headers["Authorization"] = "Bearer %s" % token
            response = requests.post(
                "%s/commands/query" % self._admin_api,
                headers=headers,
                json=params,
            )
            response.raise_for_status()
            return response.json()

        return self._authenticate_request(call)

    def create_intervention_response(self, params):
        """
        Example intervention response params:
        {
            "interventionId": "518e24fc-64ef-47bb-be5e-036a97aeafaa",
            "interventionType": "teleop",
            "data": {
                "state": "success",
                "notes": "looks good!"
            }
        }
        """

        def call(token):
            headers = self._headers.copy()
            headers["Authorization"] = "Bearer %s" % token
            response = requests.post(
                "%s/intervention-responses" % self._admin_api,
                headers=headers,
                json=params,
            )
            return response.json()

        return self._authenticate_request(call)

    def create_intervention_request(self, params):
        """
        Example intervention request params:
        {
            "message": "A teleop for a customer is requested",
            "interventionType": "teleop",
            "time": "2022-02-17T11:41:33.389-08:00",
            "deviceId": "b306de84-33ca-4917-9218-f686730e24e0",
            "tags": {},
            "data": {
                "instruction": "Look at the users item on the table"
            }
        }
        """

        def call(token):
            headers = self._headers.copy()
            headers["Authorization"] = "Bearer %s" % token
            response = requests.post(
                "%s/intervention-requests" % self._admin_api,
                headers=headers,
                json=params,
            )
            return response.json()

        return self._authenticate_request(call)

    def create_adapter(self, params):
        """
        Example create an adapter params:
        {
            "execCommand": "./start.sh",
            "path": "/tmp/model.dat"
            "name": "adapters_name"
        }
        """

        def call(token):
            file_id = self.upload_file(params={"path": params["path"]})
            params["fileId"] = file_id["file_id"]
            del params["path"]
            headers = self._headers.copy()
            headers["Authorization"] = "Bearer %s" % token
            response = requests.post(
                "%s/adapters" % self._admin_api,
                headers=headers,
                json=params,
            )
            return response.json()

        return self._authenticate_request(call)

    def get_device(self, device_id):
        def call(token):
            headers = self._headers.copy()
            headers["Authorization"] = "Bearer %s" % token
            response = requests.get(
                "%s/devices/%s" % (self._admin_api, device_id), headers=headers
            )
            response.raise_for_status()
            return response.json()

        return self._authenticate_request(call)

    def get_device_configuration(self, device_id, desired_configuration_version):
        def call(token):
            headers = self._headers.copy()
            headers["Authorization"] = "Bearer %s" % token
            response = requests.get(
                "%s/devices/%s/configurations/%s"
                % (self._admin_api, device_id, desired_configuration_version),
                headers=headers,
            )
            response.raise_for_status()
            return response.json()

        return self._authenticate_request(call)

    def post_device_configuration(self, device_id, params):
        """
        Example post configuration params:
        {
            "document": {
                adapter: [{
                    id: "84f98678-5f18-478d-aed8-631d9ea043a9",
                    name: "ROS-diagnostics",
                    "execCommand": "./start.sh"
                    }],
                tags: {},
                telemetry: {
                    streams: []
                }

            },

        }
        """

        def call(token):
            headers = self._headers.copy()
            headers["Authorization"] = "Bearer %s" % token
            response = requests.post(
                "%s/devices/%s/configurations" % (self._admin_api, device_id),
                headers=headers,
                json=params,
            )
            return response.json()

        return self._authenticate_request(call)

    def get_views(self):
        def call(token):
            headers = self._headers.copy()
            headers["Authorization"] = "Bearer %s" % token
            response = requests.get(
                "%s/views/" % self._admin_api,
                headers=headers,
            )
            return response.json()

        return self._authenticate_request(call)

    def get_view(self, view_id):
        def call(token):
            headers = self._headers.copy()
            headers["Authorization"] = "Bearer %s" % token
            response = requests.get(
                "%s/views/%s" % (self._admin_api, view_id),
                headers=headers,
            )
            return response.json()

        return self._authenticate_request(call)

    def patch_view(self, view_id, params):
        def call(token):
            headers = self._headers.copy()
            headers["Authorization"] = "Bearer %s" % token
            response = requests.patch(
                "%s/views/%s" % (self._admin_api, view_id),
                headers=headers,
                json=params,
            )
            return response.json()

        return self._authenticate_request(call)

    def get_annotation_templates(self):
        def call(token):
            headers = self._headers.copy()
            headers["Authorization"] = "Bearer %s" % token
            response = requests.get(
                "%s/annotation-templates/" % self._admin_api,
                headers=headers,
            )
            return response.json()

        return self._authenticate_request(call)

    def post_annotation(self, params):
        def call(token):
            self._add_user_id_to_params(params)
            self._add_organization_id_to_params(params)
            params_stripped = _strip_none_values(params)
            headers = self._headers.copy()
            headers["Authorization"] = "Bearer %s" % token
            response = requests.post(
                "%s/annotations/" % (self._admin_api),
                headers=headers,
                json=params_stripped,
            )
            return response.json()

        return self._authenticate_request(call)

    def query_events(self, params):
        def call(token):
            headers = self._headers.copy()
            headers["Authorization"] = "Bearer %s" % token
            response = requests.post(
                "%s/events/query" % (self._admin_api),
                headers=headers,
                json=params,
            )
            return response.json()

        return self._authenticate_request(call)

    def query_annotations(
        self,
        start_time,  # type: datetime.datetime
        device_ids=None,  # type: Optional[List[str]]
        tags=None,  # type: Optional[Dict[str,List[str]]]
        annotation_template_ids=None,  # type: Optional[List[str]]
        message=None,  # type:str
        keyword=None,  # type: str
        end_time=datetime.datetime.now(tz=tzutc()),  # type: datetime.datetime
        params=None,  # type: Dict
    ):
        params = params if params is not None else {}

        params["tags"] = tags
        params["start"] = start_time.isoformat()
        params["end"] = end_time.isoformat()
        params["deviceIds"] = device_ids
        params["annotationTemplateIds"] = annotation_template_ids
        params["message"] = message
        params["keyword"] = keyword
        params["eventTypes"] = ["annotation"]

        params_stripped = _strip_none_values(params)
        return self.query_events(params_stripped)

    def _add_user_id_to_params(self, params):
        params["userId"] = self.get_user_id()

    def _add_organization_id_to_params(self, params):
        params["organizationId"] = self.get_organization_id()

    def _authenticate(self):
        payload = {
            "email": self._email,
            "password": self._password,
            "tokenExpirationSeconds": 3600,
        }
        response = requests.post(
            "%s/auth/login" % self._admin_api,
            headers=self._headers,
            json=payload,
        )
        response.raise_for_status()
        result = response.json()
        if "authentication" not in result:
            raise ValueError("Authentication failed")
        self._token_expiry = int(time.time()) + 3530
        self._token = result["authentication"]["accessToken"]
        self._organization_id = result["authentication"]["organizationId"]
        self._user_id = result["authentication"]["userId"]

    def _authenticate_request(self, call):
        if self._token is None or self._token_expiry < int(time.time()):
            self._authenticate()
        try:
            return call(self._token)
        except requests.exceptions.HTTPError as error:
            if error.response.status_code == 401:
                self._authenticate()
                try:
                    return call(self._token)
                except requests.exceptions.HTTPError as error:
                    sys.stderr.write("%s\n" % error.response.text)
                    raise error
            else:
                sys.stderr.write("%s\n" % error.response.text)
                raise error


def _strip_none_values(dict):
    return {k: v for k, v in dict.items() if v is not None}
