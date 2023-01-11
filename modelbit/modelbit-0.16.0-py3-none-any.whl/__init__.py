__version__ = "0.16.0"
__author__ = 'Modelbit'

import os, sys, yaml, pickle, pandas
from typing import cast, Union, Callable, Any, Dict, List, Optional

# aliasing since some of these overlap with functions we want to expose to users
from . import datasets as m_datasets
from . import warehouses as m_warehouses
from . import deployments as m_deployments
from . import runtime as m_runtime
from . import utils as m_utils
from . import helpers as m_helpers
from . import model_wrappers as m_model_wrappers
from . import email as m_email
from . import jobs as m_jobs
from . import special_handling as m_special_handling

m_helpers.pkgVersion = __version__


# Nicer UX for customers: from modelbit import Deployment
class Deployment(m_runtime.Deployment):
  ...


def __str__():
  return "Modelbit Client"


def _repr_html_():  # type: ignore
  return __str__()


datasets = m_datasets.list

get_dataset = m_datasets.get

warehouses = m_warehouses.list

deployments = m_deployments.list

job = m_jobs.jobDecorator


def deploy(deployableObj: Union[Callable[..., Any], m_runtime.Deployment],
           name: Optional[str] = None,
           python_version: Optional[str] = None,
           python_packages: Optional[List[str]] = None,
           system_packages: Optional[List[str]] = None,
           dataframe_mode: bool = False,
           example_dataframe: Optional[pandas.DataFrame] = None):
  m_helpers.refreshAuthentication()  # Refreshes default environment
  if _objIsDeployment(deployableObj):
    deployableObj = cast(Deployment, deployableObj)
    return deployableObj.deploy()
  elif callable(deployableObj):
    dep = Deployment(name=name,
                     deploy_function=deployableObj,
                     python_version=python_version,
                     python_packages=python_packages,
                     system_packages=system_packages,
                     dataframe_mode=dataframe_mode,
                     example_dataframe=example_dataframe)
    return dep.deploy()
  elif hasattr(deployableObj, "__module__") and "sklearn" in deployableObj.__module__ and hasattr(
      deployableObj, "predict"):
    return m_model_wrappers.SklearnPredictor(deployableObj,
                                             name=name,
                                             python_version=python_version,
                                             python_packages=python_packages,
                                             system_packages=system_packages,
                                             dataframe_mode=dataframe_mode,
                                             example_dataframe=example_dataframe).makeDeployment().deploy()
  else:
    raise Exception("First argument must be a function or Deployment object.")


def login(region: Optional[str] = None):
  m_helpers.performLogin(refreshAuth=True, region=region)
  return sys.modules['modelbit']


def switch_branch(branch: str):
  m_helpers.setCurrentBranch(branch)


isAuthenticated = m_helpers.isAuthenticated


def load_value(name: str):
  if name.endswith(".pkl"):
    import __main__ as main_package
    # Support finding files relative to source location
    # This doesn't work from lambda, so only use when not in a deployment
    if not os.path.exists(name):
      name = os.path.join(os.path.dirname(main_package.__file__), name)

    with open(name, "rb") as f:
      return pickle.load(f)
  extractPath = os.environ['MB_EXTRACT_PATH']
  objPath = os.environ['MB_RUNTIME_OBJ_DIR']
  if not extractPath or not objPath:
    raise Exception("Missing extractPath/objPath")
  with open(f"{extractPath}/metadata.yaml", "r") as f:
    yamlData = cast(Dict[str, Any], yaml.load(f, Loader=yaml.SafeLoader))  # type: ignore
  data: Dict[str, Dict[str, str]] = yamlData["data"]
  contentHash = data[name]["contentHash"]
  with open(f"{objPath}/{contentHash}.pkl.gz", "rb") as f:
    return m_utils.deserializeGzip(contentHash, f.read)


def save_value(obj: Any, filepath: str):
  if not m_special_handling.savedSpecialObj(obj, filepath):
    with open(filepath, "wb") as f:
      pickle.dump(obj, f)


def send_email(subject: str, to: List[str], msg: str):
  m_email.sendEmail(subject=subject, to=to, msg=msg)


def _objIsDeployment(obj: Any):
  try:
    if type(obj) in [Deployment, m_runtime.Deployment]:
      return True
    # catch modelbit._reload() class differences
    if obj.__class__.__name__ in ['Deployment']:
      return True
  except:
    return False
  return False


def parseArg(s: str) -> Any:
  import json
  try:
    return json.loads(s)
  except json.decoder.JSONDecodeError:
    return s
