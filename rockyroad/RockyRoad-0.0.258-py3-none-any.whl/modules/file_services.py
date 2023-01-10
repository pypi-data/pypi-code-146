from pickle import FALSE
from .module_imports import *


@headers({"Ocp-Apim-Subscription-Key": key})
class File_Services(Consumer):
    """Inteface to Inspection resource for the RockyRoad API."""

    def __init__(self, Resource, *args, **kw):
        self._base_url = Resource._base_url
        super().__init__(base_url=Resource._base_url, *args, **kw)

    @returns.json
    @multipart
    @post("services/files/upload-files/{container_name}")
    def uploadFile(
        self,
        container_name: str,
        file: Part,
        directory: Query(type=str),
        overwrite: Query(type=bool) = False,
        storage_account: Query(type=str) = None,
    ):
        """This call will upload a file."""

    @returns.json
    @http_get("services/files/list-files/{container_name}")
    def listFiles(
        self,
        container_name: str,
        directory: Query(type=str),
        recursive: Query(type=bool) = True,
        storage_account: Query(type=str) = None,
    ):
        """This call will return a list of the files by args."""

    @http_get("services/files/download-files/{container_name}/{file_name}")
    def downloadFile(
        self,
        container_name: str,
        file_name: str,
        directory: Query(type=str),
        storage_account: Query(type=str) = None,
    ):
        """This call will download the file associated with the params."""

    @delete("serices/files/delete-directory/{container_name}")
    def deleteDirectory(
        self,
        container_name: str,
        directory: Query(type=str),
        storage_account: Query(type=str) = None,
    ):
        """This call will delete a directory and all the files in it"""

    @delete("serices/files/delete-file/{container_name}/{file_name}")
    def deleteFile(
        self,
        container_name: str,
        file_name: str,
        directory: Query(type=str),
        storage_account: Query(type=str) = None,
    ):
        """This call will delete a file"""
