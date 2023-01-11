#!/usr/bin/env python3

import logging
import os
import subprocess

logger = logging.getLogger(__name__)


def findWorkspace() -> str:
  workspaceId = None
  if "MB_WORKSPACE_ID" in os.environ:
    workspaceId = os.environ["MB_WORKSPACE_ID"]
    logger.info(f"Found workspace {workspaceId} in ENV")
  else:
    wsPath = ".workspace"
    if not os.path.exists(wsPath):
      topLevelDir = subprocess.getoutput('git rev-parse --show-toplevel')
      wsPath = os.path.join(topLevelDir, wsPath)
    if os.path.exists(wsPath):
      with open(wsPath, "r") as f:
        workspaceId = f.read().strip()
        logger.info(f"Found workspace {workspaceId} in {wsPath} file")
  if workspaceId:
    return workspaceId
  raise KeyError("Workspace not found")


def findCurrentBranch() -> str:
  return subprocess.getoutput('git branch --show-current')
