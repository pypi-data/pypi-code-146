import requests
import io

from ai_dashboard import __version__
from ai_dashboard.types import Credentials

from typing import Optional, Dict, Any, List


def json_decode(request):
    try:
        decoded = request.json()
    except:
        decoded = request.content
    return decoded


class Endpoints:
    def __init__(self, credentials: Credentials) -> None:
        self._credentials = credentials
        self._base_url = (
            f"https://api-{self._credentials.region}.stack.tryrelevance.com/latest"
        )
        self._headers = dict(
            Authorization=f"{self._credentials.project}:{self._credentials.api_key}",
        )

    def _create_deployable(
        self, dataset_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None
    ):
        return json_decode(
            requests.post(
                url=self._base_url + "/deployables/create",
                headers=self._headers,
                json=dict(
                    dataset_id=dataset_id,
                    configuration={} if config is None else config,
                ),
            )
        )

    def _share_deployable(self, deployable_id: str):
        return json_decode(
            requests.post(
                url=self._base_url + f"/deployables/{deployable_id}/share",
                headers=self._headers,
            )
        )

    def _unshare_deployable(self, deployable_id: str):
        return json_decode(
            requests.post(
                url=self._base_url + f"/deployables/{deployable_id}/private",
                headers=self._headers,
            )
        )

    def _update_deployable(
        self,
        deployable_id: str,
        dataset_id: str,
        configuration: Optional[Dict] = None,
        overwrite: bool = True,
        upsert: bool = True,
    ):
        return json_decode(
            requests.post(
                url=self._base_url + f"/deployables/{deployable_id}/update",
                headers=self._headers,
                json=dict(
                    dataset_id=dataset_id,
                    configuration=configuration,
                    overwrite=overwrite,
                    upsert=upsert,
                ),
            )
        )

    def _share_dashboard(self, deployable_id: str):
        return json_decode(
            requests.post(
                url=self._base_url + f"/deployablegroups/{deployable_id}/share",
                headers=self._headers,
            )
        )

    def _unshare_dashboard(self, deployable_id: str):
        return json_decode(
            requests.post(
                url=self._base_url + f"/deployablegroups/{deployable_id}/private",
                headers=self._headers,
            )
        )

    def _get_deployable(self, deployable_id: str):
        return json_decode(
            requests.get(
                url=self._base_url + f"/deployables/{deployable_id}/get",
                headers=self._headers,
            )
        )

    def _delete_deployable(self, deployable_id: str):
        return json_decode(
            requests.post(
                url=self._base_url + f"/deployables/delete",
                headers=self._headers,
                json=dict(
                    id=deployable_id,
                ),
            )
        )

    def _list_deployables(self, page_size: int):
        return json_decode(
            requests.get(
                url=self._base_url + "/deployables/list",
                headers=self._headers,
                params=dict(
                    page_size=page_size,
                ),
            )
        )

    def _get_file_upload_urls(self, dataset_id: str, files: List[str]):
        return json_decode(
            requests.post(
                url=self._base_url + f"/datasets/{dataset_id}/get_file_upload_urls",
                headers=self._headers,
                json=dict(files=files),
            )
        )

    def _upload_media(self, presigned_url: str, media_content: bytes):
        if not isinstance(media_content, bytes):
            raise ValueError(
                f"media needs to be in a bytes format. Currently in {type(media_content)}"
            )
        return requests.put(
            presigned_url,
            data=media_content,
        )

    ##Below are the functions that are not part of the API
    def _get_content_bytes(self, content):
        if isinstance(content, str):
            if "http" in content and "/":
                # online image
                content_bytes = io.BytesIO(requests.get(content).content).getvalue()
            else:
                # local filepath
                content_bytes = io.BytesIO(open(content, "rb").read()).getvalue()
        elif isinstance(content, bytes):
            content_bytes = content
        elif isinstance(content, io.BytesIO):
            content_bytes = content.getvalue()
        else:
            raise TypeError("'content' needs to be of type str, bytes or io.BytesIO.")
        return content_bytes

    def _upload_file(self, dataset_id: str, data, filename: str):
        data_bytes = self._get_content_bytes(data)
        presigned_response = self._get_file_upload_urls(
            dataset_id=dataset_id, files=[filename]
        )
        response = self._upload_media(
            presigned_url=presigned_response["files"][0]["upload_url"],
            media_content=data_bytes,
        )
        assert response.status_code == 200
        return presigned_response["files"][0]["url"]

    def _upload_local_files(self, dataset_id: str, paths: List[str]):
        presigned_response = self._get_file_upload_urls(
            dataset_id=dataset_id, files=paths
        )
        urls = []
        for index, path in enumerate(paths):
            url = presigned_response["files"][index]["url"]
            upload_url = presigned_response["files"][index]["upload_url"]
            with open(path, "rb") as fn_byte:
                media_content = bytes(fn_byte.read())
            urls.append(url)
            response = self._upload_media(
                presigned_url=upload_url,
                media_content=media_content,
            )
            assert response.status_code == 200
        return urls
