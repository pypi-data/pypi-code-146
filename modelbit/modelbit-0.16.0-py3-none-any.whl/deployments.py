from typing import List, Dict, Union

from .utils import timeago
from .helpers import RuntimeInfo, getJsonOrPrintError, isAuthenticated
from .ux import TableHeader, renderTemplate, UserImage, renderTextTable


class DeploymentsList:

  def __init__(self):
    self._deployments: List[RuntimeInfo] = []
    resp = getJsonOrPrintError("jupyter/v1/runtimes/list")
    if resp and resp.deployments:
      self._deployments = resp.deployments

  def __repr__(self):
    if not isAuthenticated():
      return ""
    return self._makeDeploymentsTable(plainText=True)

  def _repr_html_(self):
    if not isAuthenticated():
      return ""
    return self._makeDeploymentsTable()

  def _makeDeploymentsTable(self, plainText: bool = False):
    if len(self._deployments) == 0:
      return "There are no deployments to show."
    headers, rows = self._makeTable()
    if plainText:
      return renderTextTable(headers, rows)
    return renderTemplate("table", headers=headers, rows=rows)

  def _makeTable(self):
    from collections import defaultdict
    deploymentsByName: Dict[str, List[RuntimeInfo]] = defaultdict(lambda: [])
    for d in self._deployments:
      deploymentsByName[d.name].append(d)

    headers = [
        TableHeader("Name", TableHeader.LEFT, isCode=True),
        TableHeader("Owner", TableHeader.CENTER),
        TableHeader("Version", TableHeader.RIGHT),
        TableHeader("Deployed", TableHeader.LEFT),
    ]
    rows: List[List[Union[str, UserImage]]] = []
    for dList in deploymentsByName.values():
      ld = dList[0]
      connectedAgo = timeago(ld.deployedAtMs)
      rows.append([ld.name, UserImage(ld.ownerInfo.imageUrl, ld.ownerInfo.name), ld.version, connectedAgo])
    return (headers, rows)


def list():
  return DeploymentsList()
