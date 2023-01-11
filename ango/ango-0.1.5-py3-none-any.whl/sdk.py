import datetime
import mimetypes
import urllib.request
import uuid
import zipfile
from typing import List

import requests
import json

from tqdm import tqdm

from ango.models.label_category import ToolCategory, ClassificationCategory, RelationCategory


class SDK:
    """Ango python SDK is python library for Angohub Rest API eg: https://docs.ango.ai/api/api-documentation
    Examples:
        Initializing Ango SDK:

        sdk = SDK(api_key="<YOUR_API_KEY_HERE>",)

    """

    def __init__(self, api_key, host="https://api.ango.ai"):
        self.api_key = api_key
        self.host = host

    def list_projects(self, page=1, limit=10):
        """List projects of users current organization

        Args:
        Returns:
         {
            "projects": [
                {
                    "_id": "123123123123123123123123",
                    "name": "Project Name",
                    "description": "Project Description",
                    "organization": "234234234234234234234234",
                    "createdAt": "2021-10-14T07:44:46.373Z"
                }
            ],
            "total": 1
        }
        """
        url = "%s/v2/listProjects?page=%s&limit=%s" % (self.host, page, limit)

        payload = {}
        headers = {
            'Content-Type': 'application/json',
            'apikey': self.api_key
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        return response.json()

    def get_project(self, project_id):
        """Get project Details with from project id

        Args:
            project_id: id of a project.

        Returns:
            {
            "project": {
                "categorySchema": {
                    "tools": [
                        {
                            "title": "Vehicle",
                            "tool": "bounding-box",
                            "required": false,
                            "schemaId": "4b8ac18a570747f87b27025",
                            "columnField": false,
                            "classifications": [
                                {
                                    "title": "Type",
                                    "tool": "radio",
                                    "required": false,
                                    "schemaId": "ae40cb11c104045c1a31698",
                                    "columnField": false,
                                    "options": [
                                        {
                                            "value": "Car",
                                            "schemaId": "27504d2d08f05b9944aa713"
                                        },
                                        {
                                            "value": "Truck",
                                            "schemaId": "c734a046cbee0646886a067"
                                        },
                                        {
                                            "value": "Bus",
                                            "schemaId": "41abb6003990d2aa1ce3605"
                                        },
                                        {
                                            "value": "Other",
                                            "schemaId": "32b3611a68df286fe6eb281"
                                        }
                                    ]
                                }
                            ],
                            "color": "#9c27b0",
                            "shortcutKey": "h"
                        }
                    ],
                    "classifications": [],
                    "relations": []
                },
                "consensusCount": 1,
                "deleted": false,
                "reviewConf": {
                    "filters": []
                },
                "_id": "6167dfee2a810d000e9d313f",
                "name": "Project Name",
                "description": "Project Description",
                "user": {
                    "organizationRole": "admin",
                    "deleted": false,
                    "_id": "614348d554e17400149964b1",
                    "name": "Name Surname",
                    "email": "name_surname@example.com",
                    "organization": "61435781cdb61b0013d05a03",
                    "lastActiveAt": "2021-10-14T09:55:54.814Z",
                    "apiKey": "API-KEY-HERE"
                },
                "organization": "61435781cdb61b0013d05a03",
                "createdAt": "2021-10-14T07:44:46.373Z",
                "assignedTo": [],
                "__v": 0,
                "role": "Manager"
            }
        }
        """
        url = "%s/v2/project/%s" % (self.host, project_id)

        payload = {}
        headers = {
            'Content-Type': 'application/json',
            'apikey': self.api_key
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        return response.json()

    def get_tasks(self, project_id, page=1, limit=10, status=None):
        """Get tasks of project

        Args:
            project_id: id of a project.
            page: page number for pagination starting from 1.
            limit: page size default is 10, For faster fetching tasks increase this up to 1000
            status: "TODO" or "Completed", Default None to fetch all tasks.

        Returns:
            {"tasks": [
                {
                    "sample": {
                        "isSample": false,
                        "updatedAt": "2021-10-14T08:20:31.259Z"
                    },
                    "review": {
                        "status": "Todo"
                    },
                    "answer": {
                        "tools": [
                            {
                                "schemaId": "258f3a07abdb690af46b879",
                                "classifications": [
                                    {
                                        "schemaId": "a20942feeaa72bd14d25150",
                                        "answer": "b8135ff7ae3c7ff38347978"
                                    },
                                    {
                                        "schemaId": "195857feb959465d20c8215",
                                        "answer": "fb19996138864f54eb61839"
                                    },
                                    {
                                        "schemaId": "c6403fdb451daad92247100",
                                        "answer": "Ocre"
                                    }
                                ],
                                "lock": false,
                                "objectId": "014273c35ff83e2e19c9392",
                                "ner": {
                                    "start": 10,
                                    "end": 15
                                },
                                "metadata": {
                                    "createdAt": 1634199730392,
                                    "createdBy": "import"
                                }
                            }
                        ],
                        "classifications": [],
                        "relations": []
                    },
                    "status": "TODO",
                    "isBenchmark": false,
                    "deleted": false,
                    "issues": [],
                    "openIssuesCount": 0,
                    "isPreLabeled": true,
                    "isFlag": false,
                    "isStar": false,
                    "_id": "6167e84f2a810d000e9d3186",
                    "project": "6167dfee2a810d000e9d313f",
                    "asset": {
                        "_id": "6167e84f2a810d000e9d3185",
                        "externalId": "text_file.txt",
                        "data": "https://angohub-public-assets.s3.eu-central-1.amazonaws.com/uploaded-data-d187239d-9fc0-4565-983d-50c7b42b258b.txt"
                    },
                    "organization": "61435781cdb61b0013d05a03",
                    "createdAt": "2021-10-14T08:20:31.259Z"
                },
                {
                    "sample": {
                        "isSample": false,
                        "updatedAt": "2021-10-14T07:47:23.457Z"
                    },
                    "review": {
                        "status": "Todo"
                    },
                    "answer": {
                        "tools": [
                            {
                                "schemaId": "4b8ac18a570747f87b27025",
                                "classifications": [
                                    {
                                        "schemaId": "ae40cb11c104045c1a31698",
                                        "answer": "27504d2d08f05b9944aa713"
                                    },
                                    {
                                        "schemaId": "2ea7c2a0712af78cd9bb827",
                                        "answer": "ca9e9c4c13caa3f11a3d292"
                                    },
                                    {
                                        "schemaId": "364dc1e2a7ed4d9f57ce731",
                                        "answer": "Ocre"
                                    }
                                ],
                                "lock": false,
                                "objectId": "7719679ed20f149af886359",
                                "bounding-box": {
                                    "x": 50.3,
                                    "y": 30.4,
                                    "width": 120.005,
                                    "height": 135.345
                                },
                                "metadata": {
                                    "createdAt": 1634199268359,
                                    "createdBy": "import"
                                }
                            }
                        ],
                        "classifications": [],
                        "relations": []
                    },
                    "status": "TODO",
                    "isBenchmark": false,
                    "deleted": false,
                    "issues": [],
                    "openIssuesCount": 0,
                    "isPreLabeled": true,
                    "isFlag": false,
                    "isStar": false,
                    "_id": "6167e08b2a810d000e9d314d",
                    "project": "6167dfee2a810d000e9d313f",
                    "asset": {
                        "_id": "6167e08b2a810d000e9d314c",
                        "externalId": "test.jpg",
                        "data": "https://angohub-public-assets.s3.amazonaws.com/uploaded-data-15c12f8e-4b46-4d55-8fd4-776455448810.jpg"
                    },
                    "organization": "61435781cdb61b0013d05a03",
                    "createdAt": "2021-10-14T07:47:23.457Z"
                }
                ],
                "total": 2
            }

        """
        url = "%s/v2/project/%s/tasks?page=%s&limit=%s" % (self.host, project_id, page, limit)
        if status:
            url += "&status[eq]=%s" % status
        payload = {}
        headers = {
            'Content-Type': 'application/json',
            'apikey': self.api_key
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        return response.json()

    def get_task(self, task_id):
        """Get specific task of a project

                Args:
                    task_id: id of teh task.

                Returns:
                {"task":
                    {
                        "sample": {
                            "isSample": false,
                            "updatedAt": "2021-10-14T08:20:31.259Z"
                        },
                        "review": {
                            "status": "Todo"
                        },
                        "answer": {
                            "tools": [
                                {
                                    "schemaId": "258f3a07abdb690af46b879",
                                    "classifications": [
                                        {
                                            "schemaId": "a20942feeaa72bd14d25150",
                                            "answer": "b8135ff7ae3c7ff38347978"
                                        },
                                        {
                                            "schemaId": "195857feb959465d20c8215",
                                            "answer": "fb19996138864f54eb61839"
                                        },
                                        {
                                            "schemaId": "c6403fdb451daad92247100",
                                            "answer": "Ocre"
                                        }
                                    ],
                                    "lock": false,
                                    "objectId": "014273c35ff83e2e19c9392",
                                    "ner": {
                                        "start": 10,
                                        "end": 15
                                    },
                                    "metadata": {
                                        "createdAt": 1634199730392,
                                        "createdBy": "import"
                                    }
                                }
                            ],
                            "classifications": [],
                            "relations": []
                        },
                        "status": "TODO",
                        "isBenchmark": false,
                        "deleted": false,
                        "issues": [],
                        "openIssuesCount": 0,
                        "isPreLabeled": true,
                        "isFlag": false,
                        "isStar": false,
                        "_id": "6167e84f2a810d000e9d3186",
                        "project": "6167dfee2a810d000e9d313f",
                        "asset": {
                            "_id": "6167e84f2a810d000e9d3185",
                            "externalId": "text_file.txt",
                            "data": "https://angohub-public-assets.s3.eu-central-1.amazonaws.com/uploaded-data-d187239d-9fc0-4565-983d-50c7b42b258b.txt"
                        },
                        "organization": "61435781cdb61b0013d05a03",
                        "createdAt": "2021-10-14T08:20:31.259Z"
                    }
                }

                """
        url = "%s/v2/task/%s" % (self.host, task_id)

        payload = {}
        headers = {
            'Content-Type': 'application/json',
            'apikey': self.api_key
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        return response.json()

    def assign_task(self, task, userid=None, email=None):
        """Assing task to specific user with either userid of email.

                Args:
                    task: id of a task.
                    userid: Optional userid.
                    email: Optional email.

                Returns:
                 {"task":
                    {
                        "sample": {
                            "isSample": false,
                            "updatedAt": "2021-10-14T08:20:31.259Z"
                        },
                        "review": {
                            "status": "Todo"
                        },
                        "answer": {
                            "tools": [],
                            "classifications": [],
                            "relations": []
                        },
                        "status": "TODO",
                        "isBenchmark": false,
                        "deleted": false,
                        "issues": [],
                        "openIssuesCount": 0,
                        "isPreLabeled": true,
                        "isFlag": false,
                        "isStar": false,
                        "_id": "6167e84f2a810d000e9d3186",
                        "project": "6167dfee2a810d000e9d313f",
                        "asset": {
                            "_id": "6167e84f2a810d000e9d3185",
                            "externalId": "text_file.txt",
                            "data": "https://angohub-public-assets.s3.eu-central-1.amazonaws.com/uploaded-data-d187239d-9fc0-4565-983d-50c7b42b258b.txt"
                        },
                        "organization": "61435781cdb61b0013d05a03",
                        "createdAt": "2021-10-14T08:20:31.259Z"
                    }
                }
         """
        url = "%s/v2/task/assign" % self.host

        payload = {"task": task}
        if userid:
            payload["user"] = userid
        elif email:
            payload["username"] = email
        else:
            return Exception("userid or email required!")

        payload = json.dumps(payload)
        headers = {
            'Content-Type': 'application/json',
            'apikey': self.api_key
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        return response.json()

    def _get_upload_url(self, fname: str):
        url = "%s/v2/getUploadUrl?name=%s" % (self.host, fname)
        headers = {
            'apikey': self.api_key
        }
        r = requests.request("GET", url, headers=headers).json()
        url = r["data"]["uploadUrl"]
        return url

    def __getTags(self, project_id, tags):
        ptags = self.get_batches(project_id)
        resp = []
        for t1 in tags:
            tag_exist = False
            for t2 in ptags:
                if t1 == t2["_id"] or t1 == t2["name"]:
                    resp.append(t2["_id"])
                    tag_exist = True
            if not tag_exist:
                raise Exception("Tag %s not found" % t1)
        return resp

    def upload_files(self, project_id: str, file_paths: List, integrationId: str = None, batches: List[str] = None):
        assets = []
        for path in tqdm(file_paths):
            uid = uuid.uuid4().hex
            data = ""
            external_id = ""
            if isinstance(path, str):
                data = path
                external_id = uid
            else:
                data = path.get("data")
                external_id = path.get("externalId", uid)
            file = open(data, 'rb')
            fname = uid + '.' + file.name.split('.')[-1]
            url = self._get_upload_url(fname)
            requests.put(url, data=file.read())
            asset = {'data': url.split('?')[0], 'externalId': external_id}
            if integrationId:
                asset['storage'] = integrationId
            assets.append(asset)

        url = "%s/v2/project/%s/cloud" % (self.host, project_id)
        if batches:
            tags = self.__getTags(project_id, batches)
            url += "?tags=%s" % json.dumps(tags)

        payload = json.dumps({"assets": assets})
        headers = {
            'Content-Type': 'application/json',
            'apikey': self.api_key
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        return response.json()

    def upload_files_cloud(self, project_id: str, assets, integrationId: str = None, batches: List[str] = None):
        url = "%s/v2/project/%s/cloud" % (self.host, project_id)
        if batches:
            tags = self.__getTags(project_id, batches)
            url += "?tags=%s" % json.dumps(tags)

        if integrationId:
            for a in assets:
                a['storage'] = integrationId
        payload = json.dumps({"assets": assets})
        headers = {
            'Content-Type': 'application/json',
            'apikey': self.api_key
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        return response.json()

    def create_issue(self, task_id, content, position):
        url = "%s/v2/issues" % self.host

        payload = {
            "content": content,
            "labelTask": str(task_id),
            "position": str(position)
        }
        headers = {
            'apikey': self.api_key
        }

        response = requests.request("POST", url, headers=headers, json=payload)
        return response.json()

    def get_assets(self, project_id, asset_id=None, external_id=None, page=1, limit=10):
        url = "%s/v2/project/%s/assets?page=%s&limit=%s" % (self.host, project_id, page, limit)
        if asset_id:
            url += "?_id=" % asset_id
        if external_id:
            url += "?externalId=" % external_id

        headers = {
            'apikey': self.api_key
        }
        response = requests.request("GET", url, headers=headers)
        return response.json()

    def set_asset_priority(self, project_id: str, priority: int, external_id: str = None, asset_id: str = None):
        if external_id is None and asset_id is None:
            return Exception("External id or Assest Id should be provided!")


        url = "%s/v2/priority/%s" % (self.host, project_id)

        payload = {
            "priority": priority,
            "externalId": external_id,
            "assetId": asset_id
        }
        headers = {
            'apikey': self.api_key
        }

        response = requests.request("POST", url, headers=headers, json=payload)
        return response.json()

    def create_attachment(self, project_id, attachments):

        url = "%s/v2/attachments" % self.host

        payload = {
            "project": project_id,
            "attachments": attachments
        }
        headers = {
            'apikey': self.api_key
        }

        response = requests.request("POST", url, headers=headers, json=payload)
        return response.json()

    def export(self, project_id: str, assignees: List[str] = None, completed_at: List[datetime.datetime] = None,
               updated_at: List[datetime.datetime] = None, batches: List[str] = None):

        url = "%s/v2/export?project=%s&labeledAt=true&reviewedAt=true&completion=true&duration=true&skip=true&" \
              "reviewConf=true&format=json&consensus=true&assetStatus=true&labelDuration=true&updateInfo=true&" \
              "issues=true&mask=true&segmentationPoints=true&annotationMetadata=true&benchmark=true&" \
              "labelStatus=true&sendEmail=false&doNotNotify=true" % (self.host, project_id)
        if type(assignees) == list and len(assignees) > 0:
            url += "&assignee=" + json.dumps(assignees)
        if type(batches) == list and len(batches) > 0:
            url += "&tag=" + json.dumps(batches)
        if type(completed_at) == list and len(completed_at) == 2:
            if completed_at[0] is not None:
                url += "&completedAt[gt]=" + completed_at[0].isoformat()
            if completed_at[1] is not None:
                url += "&completedAt[lt]=" + completed_at[1].isoformat()
        if type(updated_at) == list and len(updated_at) == 2:
            if updated_at[0] is not None:
                url += "&updatedAt[gt]=" + updated_at[0].isoformat()
            if completed_at[1] is not None:
                url += "&updatedAt[lt]=" + updated_at[1].isoformat()

        headers = {
            'apikey': self.api_key
        }
        response = requests.request("GET", url, headers=headers)
        link = response.json()['data']['exportPath']
        filehandle, _ = urllib.request.urlretrieve(link)
        zip_file_object = zipfile.ZipFile(filehandle, 'r')
        first_file = zip_file_object.namelist()[0]
        file = zip_file_object.open(first_file)
        content = file.read()
        json_response = json.loads(content)
        return json_response

    def create_label_set(self, project_id: str, tools: List[ToolCategory] = [],
                         classifications: List[ClassificationCategory] = [],
                         relations: List[RelationCategory] = []):

        url = "%s/v2/project/%s" % (self.host, project_id)
        headers = {
            'apikey': self.api_key
        }
        payload = {
            "categorySchema": {
                "tools": list(map(lambda t: t.toDict(), tools)),
                "classifications": list(map(lambda t: t.toDict(), classifications)),
                "relations": list(map(lambda t: t.toDict(), relations))
            }
        }

        response = requests.request("POST", url, headers=headers, json=payload)
        return response.json()

    def import_labels(self, project_id: str, labels: List[dict]):

        url = "%s/v2/import/labels" % self.host
        headers = {
            'apikey': self.api_key
        }
        payload = {
            "project": project_id,
            "jsonContent": labels
        }

        response = requests.request("POST", url, headers=headers, json=payload)
        return response.json()

    def get_integrations(self, id: str = None):
        url = "%s/v2/integrations" % self.host
        headers = {
            'apikey': self.api_key
        }
        response = requests.request("GET", url, headers=headers)
        if id:
            for i in response.json().get('data', {}).get("integrations", []):
                if i["_id"] == id:
                    return i
        return response.json()

    def get_batches(self, project_id: str, page: int = 1, limit: int = 10):
        p = self.get_project(project_id)
        return p.get("data", []).get("project", []).get("tags", [])

    def create_batch(self, project_id: str, batch_name: str):
        url = "%s/v2/batches/%s" % (self.host, project_id)
        tags = self.get_batches(project_id)
        headers = {
            'apikey': self.api_key
        }
        tags.append({
            'name': batch_name
        })
        payload = {
            "tags": tags,
        }
        response = requests.request("POST", url, headers=headers, json=payload)
        return response.json().get("data", []).get("project", []).get("tags", [])

    def assign_batches(self, project_id: str, asset_ids: List[str], batches: List[str]):
        url = "%s/v2/assignBatches" % self.host
        tags = self.__getTags(project_id, batches)
        headers = {
            'apikey': self.api_key
        }
        payload = {
            "assets": asset_ids,
            "tags": tags,
        }
        response = requests.request("POST", url, headers=headers, json=payload)
        return response.json()

    def create_project(self, name, description=""):
        url = "%s/v2/project" % self.host
        headers = {
            'apikey': self.api_key
        }
        payload = {
            "name": name,
            "description": description,
        }
        response = requests.request("POST", url, headers=headers, json=payload)
        return response.json()