from time import sleep
from typing import Union, Any, List, Dict, Optional, Tuple
from enum import Enum
import json, requests, os

from .utils import sizeOfFmt, getEnvOrDefault, inDeployment, inNotebook, inModelbitCI
from .environment import getInstalledPythonVersion, ALLOWED_PY_VERSIONS, listMissingPackagesFromImports, listMissingPackagesFromPipList
from .ux import COLORS, DifferentPythonVerWarning, MismatchedPackageWarning, MissingPackageFromImportWarning, WarningErrorTip, makeCssStyle, printTemplate
from threading import Thread

pkgVersion: str = ""  # set in __init__
_MAX_DATA_LEN = 50_000_000
_DEFAULT_CLUSTER = "app.modelbit.com"

_cluster = ""
_region = ""
_api_host = ""
_login_host = ""
_api_url = ""
_currentBranch = "main"


def _setUrls(cluster: Optional[str]):
  global _cluster, _region, _api_host, _login_host, _api_url
  if cluster is None:
    return
  _cluster = cluster
  _region = _cluster.split(".")[0]
  if cluster == "localhost":
    _api_host = f'http://web:3000/'
    _login_host = f'http://localhost:3000/'
  else:
    _api_host = f'https://{_cluster}/'
    _login_host = _api_host
  _api_url = f'{_api_host}api/'


class OwnerInfo:

  def __init__(self, data: Dict[str, Any]):
    self.id: Optional[str] = data.get("id", None)
    self.name: Optional[str] = data.get("name", None)
    self.imageUrl: Optional[str] = data.get("imageUrl", None)


class DatasetDesc:

  def __init__(self, data: Dict[str, Any]):
    self.name: str = data["name"]
    self.sqlModifiedAtMs: Optional[int] = data.get("sqlModifiedAtMs", None)
    self.query: str = data["query"]
    self.recentResultMs: Optional[int] = data.get("recentResultMs", None)
    self.numRows: Optional[int] = data.get("numRows", None)
    self.numBytes: Optional[int] = data.get("numBytes", None)
    self.ownerInfo = OwnerInfo(data["ownerInfo"])


class ResultDownloadInfo:

  def __init__(self, data: Dict[str, Any]):
    self.id: str = data["id"]
    self.signedDataUrl: str = data["signedDataUrl"]
    self.key64: str = data["key64"]
    self.iv64: str = data["iv64"]


class ObjectUploadInfo:

  def __init__(self, data: Dict[str, Any]):
    self.signedDataUrl: str = data["signedDataUrl"]
    self.key64: str = data["key64"]
    self.iv64: str = data["iv64"]
    self.objectExists: bool = data["objectExists"]


class WhType(Enum):
  Snowflake = 'Snowflake'
  Redshift = 'Redshift'


class GenericWarehouse:

  def __init__(self, data: Dict[str, Any]):
    self.type: WhType = data["type"]
    self.id: str = data["id"]
    self.displayName: str = data["displayName"]
    self.deployStatusPretty: str = data["deployStatusPretty"]
    self.createdAtMs: int = data["createdAtMs"]


class RuntimeFile:

  def __init__(self, name: str, contents: str):
    self.name = name
    self.contents = contents

  def asDict(self):
    return {"name": self.name, "contents": self.contents}


class RuntimePythonProps:
  excludeFromDict: List[str] = ['errors']

  def __init__(self):
    self.source: Optional[str] = None
    self.name: Optional[str] = None
    self.argNames: Optional[List[str]] = None
    self.argTypes: Optional[Dict[str, str]] = None
    self.namespaceVarsDesc: Optional[Dict[str, str]] = None
    self.namespaceFunctions: Optional[Dict[str, str]] = None
    self.namespaceImports: Optional[Dict[str, str]] = None
    self.namespaceFroms: Optional[Dict[str, str]] = None
    self.namespaceModules: Optional[List[str]] = None
    self.errors: Optional[List[str]] = None
    self.namespaceVars: Optional[Dict[str, Any]] = None
    self.customInitCode: Optional[List[str]] = None
    self.extraDataFiles: Optional[Dict[str, Tuple[Any, bytes]]] = None
    self.jobs: List[JobProps] = []


class JobProps:

  def __init__(self, name: str, outVar: str, rtProps: RuntimePythonProps, schedule: Optional[str],
               redeployOnSuccess: bool):
    self.name = name
    self.outVar = outVar
    self.rtProps = rtProps
    self.schedule = schedule
    self.redeployOnSuccess = redeployOnSuccess


class NamespaceCollection:

  def __init__(self):
    self.functions: Dict[str, str] = {}
    self.vars: Dict[str, Any] = {}
    self.imports: Dict[str, str] = {}
    self.froms: Dict[str, str] = {"*": "typing"}
    self.allModules: List[str] = []
    self.customInitCode: List[str] = []
    self.extraDataFiles: Dict[str, Tuple[Any, bytes]] = {}
    self.jobs: List[JobProps] = []


class RuntimeInfo:

  def __init__(self, data: Dict[str, Any]):
    self.id: str = data["id"]
    self.name: str = data["name"]
    self.version: str = data["version"]
    self.deployedAtMs: int = data["deployedAtMs"]
    self.ownerInfo = OwnerInfo(data["ownerInfo"])


class RuntimeEnvironment:

  def __init__(self, data: Dict[str, Any]):
    self.pythonVersion: str = data.get("pythonVersion", None)
    self.pythonPackages: Optional[List[str]] = data.get("pythonPackages", None)
    self.systemPackages: Optional[List[str]] = data.get("systemPackages", None)


class DeploymentTestError(Enum):
  UnknownFormat = 'UnknownFormat'
  ExpectedNotJson = 'ExpectedNotJson'
  CannotParseArgs = 'CannotParseArgs'


class DeploymentTestDef:

  def __init__(self, data: Dict[str, Any]):
    self.command: str = data.get("command", "")
    self.expectedOutput: Union[str, Dict[Union[str, int, float, bool], Any]] = data.get("expectedOutput", "")
    self.args: Optional[List[Any]] = data.get("args", None)
    self.error: Optional[str] = data.get("error", None)


class NotebookEnv:

  def __init__(self, data: Dict[str, Any]):
    self.userEmail: Optional[str] = data.get("userEmail", None)
    self.signedToken: Optional[str] = data.get("signedToken")
    self.authenticated: bool = data.get("authenticated", False)
    self.workspaceName: Optional[str] = data.get("workspaceName", None)
    self.mostRecentVersion: Optional[str] = data.get("mostRecentVersion", None)
    self.cluster: Optional[str] = data.get("cluster", None)
    self.defaultEnvironment: Optional[RuntimeEnvironment] = None
    if "defaultEnvironment" in data and data["defaultEnvironment"] is not None:
      self.defaultEnvironment = RuntimeEnvironment(data["defaultEnvironment"])


class NotebookResponse:

  def __init__(self, data: Dict[str, Any]):
    self.error: Optional[str] = data.get("error", None)
    self.message: Optional[str] = data.get("message", None)

    self.notebookEnv: Optional[NotebookEnv] = None
    if "notebookEnv" in data:
      self.notebookEnv = NotebookEnv(data["notebookEnv"])

    self.datasets: Optional[List[DatasetDesc]] = None
    if "datasets" in data:
      self.datasets = [DatasetDesc(d) for d in data["datasets"]]

    self.dsrDownloadInfo: Optional[ResultDownloadInfo] = None
    if "dsrDownloadInfo" in data:
      self.dsrDownloadInfo = ResultDownloadInfo(data["dsrDownloadInfo"])

    self.dsrPklDownloadInfo: Optional[ResultDownloadInfo] = None
    if "dsrPklDownloadInfo" in data:
      self.dsrPklDownloadInfo = ResultDownloadInfo(data["dsrPklDownloadInfo"])

    self.warehouses: Optional[List[GenericWarehouse]] = None
    if "warehouses" in data:
      self.warehouses = [GenericWarehouse(w) for w in data["warehouses"]]

    self.runtimeOverviewUrl: Optional[str] = None
    if "runtimeOverviewUrl" in data:
      self.runtimeOverviewUrl = data["runtimeOverviewUrl"]

    self.deployments: Optional[List[RuntimeInfo]] = None
    if "deployments" in data:
      self.deployments = [RuntimeInfo(d) for d in data["deployments"]]

    self.tests: Optional[List[DeploymentTestDef]] = None
    if "tests" in data:
      self.tests = [DeploymentTestDef(d) for d in data["tests"]]

    self.objectUploadInfo: Optional[ObjectUploadInfo] = None
    if "objectUploadInfo" in data:
      self.objectUploadInfo = ObjectUploadInfo(data["objectUploadInfo"])


def getJson(path: str, body: Dict[str, Any] = {}) -> NotebookResponse:
  global _state
  requestToken = _state.signedToken
  if requestToken == None:
    requestToken = os.getenv('MB_RUNTIME_TOKEN')
  data: Dict[str, Any] = {"requestToken": requestToken, "version": pkgVersion, "branch": _currentBranch}
  data.update(body)
  dataLen = len(json.dumps(data))
  if (dataLen > _MAX_DATA_LEN):
    return NotebookResponse({
        "error":
            f'API Error: Request is too large. (Request is {sizeOfFmt(dataLen)} Limit is {sizeOfFmt(_MAX_DATA_LEN)})'
    })
  with requests.post(f'{_api_url}{path}', json=data) as url:
    nbResp = NotebookResponse(url.json())
    if nbResp.notebookEnv:
      _state = nbResp.notebookEnv
    return nbResp


def getJsonOrPrintError(path: str, body: Dict[str, Any] = {}):
  nbResp = getJson(path, body)
  if not isAuthenticated():
    performLogin()
    nbResp = getJson(path, body)  #return False
    if not isAuthenticated():
      return False
  if nbResp.error:
    printTemplate("error", None, errorText=nbResp.error)
    return False
  return nbResp


def refreshAuthentication() -> bool:
  if inDeployment():
    return True
  global _state
  nbResp = getJson("jupyter/v1/login")
  if nbResp.error:
    printTemplate("error", None, errorText=nbResp.error)
    return False
  if nbResp.notebookEnv:
    _state = nbResp.notebookEnv
    _setUrls(_state.cluster)
  return isAuthenticated()


def isAuthenticated() -> bool:
  return _state.authenticated


def performLogin(refreshAuth: bool = False, region: Optional[str] = None):
  if inDeployment():
    return
  elif inNotebook() or inModelbitCI():
    return performNotebookLogin(refreshAuth, region)
  else:
    if not performCLILogin():
      performNotebookLogin(refreshAuth, region, waitForResponse=True)


def performCLILogin():
  if isAuthenticated():
    return

  from .cli.workspace import findWorkspace, findCurrentBranch
  from .cli.local_config import getWorkspaceConfig
  global _state
  try:
    config = getWorkspaceConfig(findWorkspace())
    if not config:
      raise KeyError("Workspace credentials not found")
  except KeyError:
    return False

  _setUrls(config.cluster)
  _state.signedToken = config.gitUserAuthToken.replace("mbpat-", "")
  return setCurrentBranch(findCurrentBranch())


def performNotebookLogin(refreshAuth: bool = False,
                         region: Optional[str] = None,
                         waitForResponse: bool = False):
  if region is not None:
    _setUrls(f"{region}.modelbit.com")
  if (refreshAuth):
    refreshAuthentication()
  if isAuthenticated():
    printAuthenticatedMessage()
    return
  displayId = "mbLogin"
  printLoginMessage(displayId)

  def pollForLoggedIn():
    triesLeft = 150
    while not isAuthenticated() and triesLeft > 0:
      triesLeft -= 1
      sleep(3)
      refreshAuthentication()
    if isAuthenticated():
      printAuthenticatedMessage(displayId)
    else:
      printTemplate("login-timeout", displayId)

  if waitForResponse:
    pollForLoggedIn()
  else:
    loginThread = Thread(target=pollForLoggedIn)
    if not inModelbitCI():
      loginThread.start()


def _pipUpgradeInfo():
  if os.getenv('MB_RUNTIME_TOKEN'):
    return None  # runtime environments don't get upgraded
  latestVer = _state.mostRecentVersion

  def ver2ints(ver: str):
    return [int(v) for v in ver.split(".")]

  nbVer = pkgVersion
  if latestVer and ver2ints(latestVer) > ver2ints(nbVer):
    return {"installed": nbVer, "latest": latestVer}
  return None


def _environmentConflicts():
  warnings: List[WarningErrorTip] = []

  de = _state.defaultEnvironment
  if de is None:
    return warnings

  installedPythonVer = getInstalledPythonVersion()
  if getInstalledPythonVersion() != de.pythonVersion:
    warnings.append(DifferentPythonVerWarning(de.pythonVersion, installedPythonVer))
  warnings += getMissingPackageWarningsFromEnvironment(de.pythonPackages)
  return warnings


def getMissingPackageWarningsFromEnvironment(pyPackages: Optional[List[str]]):
  warnings: List[WarningErrorTip] = []
  missingPackages = listMissingPackagesFromPipList(pyPackages)
  if len(missingPackages) > 0:
    for mp in missingPackages:
      desiredPackage, similarPackage = mp
      if similarPackage is not None:
        warnings.append(MismatchedPackageWarning(desiredPackage, similarPackage))
  return warnings


def getMissingPackageWarningsFromImportedModules(importedModules: Optional[List[str]],
                                                 pyPackages: Optional[List[str]]):
  warnings: List[WarningErrorTip] = []
  missingPackages = listMissingPackagesFromImports(importedModules, pyPackages)
  for mp in missingPackages:
    importedModule, pipPackageInstalled = mp
    warnings.append(MissingPackageFromImportWarning(importedModule, pipPackageInstalled))
  return warnings


def printAuthenticatedMessage(displayId: Optional[str] = None):
  inRegion: Optional[str] = None
  if _cluster != _DEFAULT_CLUSTER:
    inRegion = _region
  styles = {
      "connected": makeCssStyle({
          "color": COLORS["success"],
          "font-weight": "bold",
      }),
      "info": makeCssStyle({
          "font-family": "monospace",
          "font-weight": "bold",
          "color": COLORS["brand"],
      })
  }
  printTemplate("authenticated",
                displayId,
                updateDisplayId=True,
                styles=styles,
                email=_state.userEmail,
                workspace=_state.workspaceName,
                inRegion=inRegion,
                currentBranch=getCurrentBranch(),
                needsUpgrade=_pipUpgradeInfo(),
                warningsList=_environmentConflicts())


def printLoginMessage(displayId: Optional[str] = None):
  if (_state.signedToken == None or type(_state.signedToken) != str):
    raise Exception("Signed token missing, cannot authenticate.")
  displayUrl = f'modelbit.com/t/{_state.signedToken[0:10]}...'
  source = "notebook" if inNotebook() else "terminal"
  linkUrl = f'{_login_host}t/{_state.signedToken}?source={source}'
  printTemplate("login", displayId, displayUrl=displayUrl, linkUrl=linkUrl, needsUpgrade=_pipUpgradeInfo())


def _runtimeToken():  # type: ignore
  return _state.signedToken


def setCurrentBranch(branch: str):
  global _currentBranch
  if type(branch) != str:
    raise Exception("Branch must be a string.")
  oldBranch = _currentBranch
  _currentBranch = branch
  if not refreshAuthentication():
    _currentBranch = oldBranch


def getCurrentBranch():
  return _currentBranch


def getDefaultPythonVersion():
  if _state.defaultEnvironment is None:
    installedVersion = getInstalledPythonVersion()
    if installedVersion in ALLOWED_PY_VERSIONS:
      return installedVersion
    return "3.8"
  else:
    return _state.defaultEnvironment.pythonVersion


def getDefaultPythonPackages() -> Optional[List[str]]:
  if _state.defaultEnvironment is None:
    return []
  return _state.defaultEnvironment.pythonPackages


def getDefaultSystemPackages() -> Optional[List[str]]:
  if _state.defaultEnvironment is None:
    return []
  return _state.defaultEnvironment.systemPackages


# set defaults
_setUrls(getEnvOrDefault("MB_JUPYTER_CLUSTER", _DEFAULT_CLUSTER))
_state = NotebookEnv({})
