import requests

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
        return json_decode(
            requests.put(
                presigned_url,
                data=media_content,
            )
        )
