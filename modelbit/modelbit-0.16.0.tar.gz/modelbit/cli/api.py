import logging
import os
from typing import Any, Dict, Optional

import requests

from .. import __version__
from .local_config import getWorkspaceConfig
from .secure_storage import EncryptedObjectInfo, getSecureData, putSecureData

logger = logging.getLogger(__name__)


class MbApi:

  _DEFAULT_CLUSTER = "app.modelbit.com"

  _cluster = ""
  _region = ""
  _api_host = ""
  _login_host = ""

  def __init__(self, authToken: Optional[str] = None, cluster: Optional[str] = None):
    self.setUrls(os.getenv("MB_JUPYTER_CLUSTER", cluster or self._DEFAULT_CLUSTER))
    self.pkgVersion = __version__
    self.authToken = authToken

  def getToken(self) -> None:
    resp = self.getJson("api/cli/v1/get_token")
    if not "signedUuid" in resp:
      raise Exception("Invalid respones from server.")
    self.authToken = resp["signedUuid"]

  def getLoginLink(self, source: str = "clone") -> str:
    if not self.authToken:
      self.getToken()
    return f'{self._login_host}t/{self.authToken}?source={source}'

  def getJson(self, path: str, body: Dict[str, Any] = {}) -> Dict[str, Any]:
    data: Dict[str, Any] = {"version": self.pkgVersion}
    data.update(body)
    hdrs: Dict[str, str] = {}
    if self.authToken is not None:
      hdrs["Authorization"] = self.authToken
    logger.info(f"Making request with{'out' if not self.authToken else '' } auth to {path}")
    with requests.post(f'{self._api_host}{path}', headers=hdrs, json=data) as url:  # type: ignore
      resp = url.json()  # type: ignore
      return resp

  def setUrls(self, cluster: Optional[str]) -> None:
    logger.info(f"Setting cluster to {cluster}")
    if cluster is None:
      return
    self._cluster = cluster
    self._region = self._cluster.split(".")[0]
    if cluster == "localhost":
      self._api_host = f'http://localhost:3000/'
      self._login_host = f'http://localhost:3000/'
    else:
      self._api_host = f'https://{self._cluster}/'
      self._login_host = self._api_host

  def getApiHost(self):
    return self._api_host

  def getCluster(self):
    return self._cluster

  def runtimeObjectUploadUrl(self, contentHash: str) -> EncryptedObjectInfo:
    resp = self.getJson("api/cli/v1/runtime_object_upload_url", {
        "contentHash": contentHash,
    })
    return EncryptedObjectInfo(**resp)

  def runtimeObjectDownloadUrl(self, contentHash: str) -> EncryptedObjectInfo:
    resp = self.getJson("api/cli/v1/runtime_object_download_url", {
        "contentHash": contentHash,
    })
    return EncryptedObjectInfo(**resp)


class ObjectApi:

  def __init__(self, workspaceId: str):
    self.workspaceId = workspaceId
    config = getWorkspaceConfig(workspaceId)
    # TODO: Do auth dance if config not found
    if not config:
      raise KeyError("workspace config not found")
    self.api = MbApi(config.gitUserAuthToken, config.cluster)

  def uploadRuntimeObject(self, obj: bytes, contentHash: str, desc: str) -> str:
    resp = self.api.runtimeObjectUploadUrl(contentHash)
    if resp and not resp.objectExists:
      putSecureData(resp, obj, desc)
    return contentHash

  def downloadRuntimeObject(self, contentHash: str, desc: str) -> bytes:
    resp = self.api.runtimeObjectDownloadUrl(contentHash)
    if not resp or not resp.objectExists:
      raise Exception("Failed to get file URL")
    data = getSecureData(self.workspaceId, resp, desc)
    if not data:
      raise Exception(f"Failed to download and decrypt")
    return data
