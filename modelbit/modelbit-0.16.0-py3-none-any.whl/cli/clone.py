import logging
import os
import subprocess
import sys
from typing import Tuple

from .api import MbApi
from .login import CloneInfo, loginAndPickWorkspace
from .ui import chooseOption, output

logger = logging.getLogger(__name__)


def pickGitOrigin(cloneInfo: CloneInfo) -> Tuple[str, bool]:
  if cloneInfo.forgeRepoUrl is None:
    return (cloneInfo.mbRepoUrl, True)

  forgeHost = cloneInfo.forgeRepoUrl.split(":")[0]
  forgeHost = forgeHost.split("@")[1] if forgeHost.index("@") else forgeHost
  action = chooseOption("Choose a remote",
                        [f"Modelbit: {cloneInfo.mbRepoUrl}", f"{forgeHost}: {cloneInfo.forgeRepoUrl}"], 0)
  if action is None:
    output("Nothing chosen")
    exit(1)
  if action.startswith("Modelbit"):
    return (cloneInfo.mbRepoUrl, True)
  return cloneInfo.forgeRepoUrl, False


def doGitClone(workspaceId: str, apiHost: str, gitUrl: str, targetDir: str) -> None:
  cloneConfig = [
      "--config", f"modelbit.restendpoint={apiHost}api/format", "--config",
      "filter.modelbit.process=modelbit gitfilter process", "--config", "filter.modelbit.required",
      "--config", "merge.renormalize=true"
  ]

  env = dict(os.environ.items())
  env["MB_WORKSPACE_ID"] = workspaceId
  logger.info(f"Cloning {gitUrl} into {targetDir} for {workspaceId}")
  try:
    subprocess.run(["git", "clone", *cloneConfig, gitUrl, targetDir],
                   stdin=sys.stdin,
                   stdout=sys.stdout,
                   stderr=sys.stderr,
                   check=True,
                   env=env)
  except subprocess.CalledProcessError:
    output(
        "There was an error cloning your repository. Some large files may not have been restored. Please contact support."
    )


def clone(targetDir: str = "modelbit") -> None:
  if targetDir and os.path.exists(targetDir):
    output(f"Error: Unable to clone repository. The target directory '{targetDir}' already exists.")
    exit(1)

  mbApi = MbApi()
  cloneInfo = loginAndPickWorkspace(mbApi)
  if not cloneInfo:
    raise Exception("Failed to authenticate. Please try again.")

  gitUrl, _ = pickGitOrigin(cloneInfo)
  doGitClone(cloneInfo.workspaceId, mbApi.getApiHost(), gitUrl, targetDir)
