from typing import Optional, Any, Dict

from .api import MbApi
from .local_config import saveWorkspaceConfig
from .ui import output
from time import sleep
import logging

logger = logging.getLogger(__name__)


class CloneInfo:

  def __init__(self, data: Dict[str, Any]):
    self.workspaceId: str = data["workspaceId"]
    self.cluster: str = data["cluster"]
    self.gitUserAuthToken: str = data["gitUserAuthToken"]
    self.mbRepoUrl: str = data["mbRepoUrl"]
    self.forgeRepoUrl: Optional[str] = data.get("forgeRepoUrl", None)

  def __str__(self) -> str:
    return str(vars(self))


def loginAndPickWorkspace(mbApi: MbApi) -> Optional[CloneInfo]:
  try:
    linkUrl = mbApi.getLoginLink()
  except Exception as e:
    logger.info("Error getting login link", exc_info=e)
    output(f"Failed to reach login servers for {mbApi.getCluster()}. Please contact support.")
    exit(1)

  output(f"Authenticate with modelbit: {linkUrl}")

  cloneInfo = None
  triesLeft = 150
  while triesLeft > 0:
    cloneInfo = checkAuthentication(mbApi)
    if cloneInfo:
      break
    triesLeft -= 1
    sleep(3)
  if cloneInfo:
    saveWorkspaceConfig(cloneInfo.workspaceId, cloneInfo.cluster, cloneInfo.gitUserAuthToken)
  else:
    output("Authentication timed out")

  return cloneInfo


def checkAuthentication(api: MbApi) -> Optional[CloneInfo]:
  resp = api.getJson("api/cli/v1/login")
  if "errorCode" in resp:
    logger.info(f"Got response {resp}")
    return None
  if isClusterRedirectResponse(resp):
    api.setUrls(resp["cluster"])
    return None
  return CloneInfo(resp)


def isClusterRedirectResponse(resp: Dict[str, Any]) -> bool:
  return "cluster" in resp and not "workspaceId" in resp
