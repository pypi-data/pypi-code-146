from typing import List, Optional
import requests
import uuid
import base64
import aiohttp
import asyncio
import traceback
import mimetypes
from canner.payloads import DeleteFilesPayload
from canner.request import CannerRequest
from .csv_wrapper import CsvWrapper
from .json_wrapper import JsonWrapper
from .image_wrapper import ImageWrapper
from io import BytesIO

__all__ = ["File"]

BLOCK_SIZE = 10485760  # 10MB


class File(object):
    def __init__(
        self,
        request: CannerRequest,
        workspace_id: str,
        replaceLocalhostString: Optional[str] = None,
    ):
        self.workspace_id = workspace_id
        self.request = request
        self.replaceLocalhostString = replaceLocalhostString

    def _create_block_id(self):
        id = str(uuid.uuid4())
        return base64.b64encode(id.encode()).decode()

    def list_file_objects(self, workspace_id: str, recursive: bool = True):
        # The file could indicate in 3th level, so we need indicate 2 level children field
        query_statement = """
            query files($where: FileWhereInput!, $recursive: Boolean) {
                files(where: $where, recursive: $recursive) {
                    name
                    absolutePath
                    size
                    isFolder
                    lastModified
                    children {
                        name
                        absolutePath
                        size
                        isFolder
                        lastModified
                        children {
                            name
                            absolutePath
                            size
                            isFolder
                            lastModified
                        }
                    }
                }
            }"""
        # run graphql
        data = self.request.graphql_exec(
            {
                "operationName": "files",
                "query": query_statement,
                "variables": {
                    "where": {"workspaceId": workspace_id},
                    "recursive": recursive,
                },
            }
        ).get("files")

        return data

    def list_absolute_path(self, recursive: bool):
        file_objects = self.list_file_objects(self.workspace_id, recursive)
        return self._build_absolute_path(file_objects)

    def _build_absolute_path(self, file_objects: List[dict]):
        absolute_paths = []
        for file_object in file_objects:
            # The object is folder and has children field
            if file_object["isFolder"] and "children" in file_object:
                sub_absolute_paths = self._build_absolute_path(file_object["children"])
                absolute_paths.extend(sub_absolute_paths)
            # if the object is file
            if not file_object["isFolder"]:
                absolute_path = "/" + file_object["absolutePath"]
                absolute_paths.append(absolute_path)

        return absolute_paths

    def _replace_localhost(self, url):
        if self.replaceLocalhostString is not None:
            return url.replace("localhost", self.replaceLocalhostString).replace(
                "127.0.0.1", self.replaceLocalhostString
            )
        return url

    def _get_download_signed_url(self, absolute_path):
        object_name = absolute_path
        if absolute_path[0] == "/":
            object_name = absolute_path[1:]
        data = self.request.get(
            f"api/getSignedUrl?workspaceId={self.workspace_id}&objectName={object_name}"
        )
        return data

    def _get_upload_signed_url(self, absolute_path):
        object_name = absolute_path
        if absolute_path[0] == "/":
            object_name = absolute_path[1:]
        data = self.request.get(
            f"api/putSignedUrl?workspaceId={self.workspace_id}&objectName={object_name}"
        )
        return data

    def _get(self, absolute_path):
        data = self._get_download_signed_url(absolute_path)
        # quick fix: in notebook we can't get minio data from localhost
        url = self._replace_localhost(data["signedUrl"])
        http_response = {}
        try:
            http_response = requests.get(url)
            http_response.raise_for_status()
        except Exception as err:
            content = http_response.get("content")
            print(f"Error occurred: {err}, {content}")
        else:
            return http_response

    def get_content(self, absolute_path):
        r = self._get(absolute_path)
        return r.content

    def delete(self, absolute_path):
        object_name = absolute_path
        if absolute_path[0] == "/":
            object_name = absolute_path[1:]
        # prepare delete files payload
        payload = DeleteFilesPayload().build(self.workspace_id, object_name)
        data = self.request.graphql_exec(payload)
        return data

    def get_text(self, absolute_path, encoding="utf-8"):
        r = self._get(absolute_path)
        r.encoding = encoding
        return r.text

    def get_csv_wrapper(self, absolute_path, encoding="utf-8"):
        content = self.get_content(absolute_path)
        csv_wrapper = CsvWrapper(content=content, encoding=encoding)
        return csv_wrapper

    def get_json_wrapper(self, absolute_path, encoding="utf-8"):
        content = self.get_content(absolute_path)
        json_wrapper = JsonWrapper(content=content, encoding=encoding)
        return json_wrapper

    def get_image_wrapper(self, absolute_path):
        content = self.get_content(absolute_path)
        image_wrapper = ImageWrapper(content=content)
        return image_wrapper

    async def _put_azure_block(self, url, file):
        block_id = self._create_block_id()
        async with aiohttp.ClientSession() as session:
            async with session.put(
                url=f"{url}&comp=block&blockId={block_id}", data=file
            ) as response:
                response.raise_for_status()
        return block_id

    def _put_azure_block_list(self, url, block_ids, headers):
        id_map = map(lambda id: f"<Latest>{id}</Latest>", block_ids)
        content = "\n".join(id_map)
        xml = """<?xml version="1.0" encoding="utf-8"?>
<BlockList>
  {}
</BlockList>""".format(
            content
        )
        headers["Content-Type"] = "application/xml"
        http_response = requests.put(f"{url}&comp=blocklist", data=xml, headers=headers)
        return http_response

    async def _put_azure(self, url, data, headers):
        blocks = [data[i : i + BLOCK_SIZE] for i in range(0, len(data), BLOCK_SIZE)]
        block_ids = await asyncio.gather(
            *[self._put_azure_block(url=url, file=BytesIO(block)) for block in blocks]
        )
        http_response = self._put_azure_block_list(
            url=url, block_ids=block_ids, headers=headers
        )
        return http_response

    def _put(self, url, data, headers):
        return requests.put(url, data=data, headers=headers)

    def put(self, absolute_path, data):
        res = self._get_upload_signed_url(absolute_path)
        # quick fix: in notebook we can't get minio data from localhost
        url: str = self._replace_localhost(res["signedUrl"])
        info_id = res["fileInfoId"]
        http_response = {}
        headers = {}
        try:
            if url.find(".blob.core.windows.net") != -1:
                headers["x-ms-meta-file_info_id"] = info_id
                loop = asyncio.get_event_loop()
                http_response = loop.run_until_complete(
                    self._put_azure(url=url, data=data, headers=headers)
                )
            else:
                content_type = mimetypes.guess_type(absolute_path)[0]
                headers["x-amz-meta-file_info_id"] = info_id
                headers["Content-Type"] = content_type
                http_response = self._put(url=url, data=data, headers=headers)
            http_response.raise_for_status()
        except Exception as err:
            content = http_response.content
            print(
                f"Error occurred when put object: {err}, {content}, {traceback.format_exc()}"
            )
            return False
        return True
