from typing import Callable, Any, List, Dict, Optional
from .helpers import NamespaceCollection, RuntimePythonProps, JobProps
import inspect, re
from .special_handling import collectedSpecialObj, collectPipelineModules
from .jobs import ModelbitJobResult, stripJobDecorators
from .utils import unindent


def getRuntimePythonProps(func: Optional[Callable[..., Any]], sourceOverride: Optional[str] = None):
  props: RuntimePythonProps = RuntimePythonProps()
  if not callable(func):
    raise Exception('The deploy function parameter does not appear to be a function.')
  else:
    props.name = func.__name__
    props.source = sourceOverride if sourceOverride is not None else getFuncSource(func)
    props.argNames = getFuncArgNames(func)
    props.argTypes = annotationsToTypeStr(func.__annotations__)
    nsCollection = NamespaceCollection()
    collectNamespaceDeps(func, nsCollection)
    props.namespaceFunctions = nsCollection.functions
    props.namespaceVars = nsCollection.vars
    props.namespaceVarsDesc = _strValues(nsCollection.vars)
    props.namespaceImports = nsCollection.imports
    props.namespaceFroms = nsCollection.froms
    props.namespaceModules = list(set(nsCollection.allModules))
    props.customInitCode = nsCollection.customInitCode
    props.extraDataFiles = nsCollection.extraDataFiles
    props.jobs = nsCollection.jobs

    # Add modules from jobs to inference code so warnings fire if job includes extra packages
    for j in props.jobs:
      if j.rtProps.namespaceModules is not None:
        for nMod in j.rtProps.namespaceModules:
          if nMod not in props.namespaceModules:
            props.namespaceModules.append(nMod)
  return props


def getFuncSource(func: Callable[..., Any]):
  if not callable(func):
    return None
  return stripJobDecorators(unindent(inspect.getsource(func)))


def getFuncArgNames(func: Optional[Callable[..., Any]]):
  noArgs: List[str] = []
  if func is None:
    return noArgs
  argSpec = inspect.getfullargspec(func)
  if argSpec.varargs:
    return ['...']
  if argSpec.args:
    return argSpec.args
  return noArgs


def annotationsToTypeStr(annotations: Dict[str, Any]):
  annoStrs: Dict[str, str] = {}
  for name, tClass in annotations.items():
    try:
      if tClass == Any:
        annoStrs[name] = "Any"
      else:
        annoStrs[name] = tClass.__name__
    except:
      pass
  return annoStrs


def _strValues(args: Dict[str, Any]):
  newDict: Dict[str, str] = {}
  for k, v in args.items():
    strVal = re.sub(r'\s+', " ", str(v))
    if type(v) is bytes:
      strVal = "Binary data"
    elif len(strVal) > 200:
      strVal = strVal[0:200] + "..."
    newDict[k] = strVal
  return newDict


def collectNamespaceDeps(func: Callable[..., Any], collection: NamespaceCollection):
  if not callable(func):
    return collection
  _collectArgTypes(func, collection)
  globalsDict = func.__globals__
  allNames = _extractAllNames(func)
  for maybeFuncVarName in allNames:
    if maybeFuncVarName in globalsDict:
      maybeFuncVar = globalsDict[maybeFuncVarName]
      if callable(maybeFuncVar) and maybeFuncVar == func:
        continue
      if type(maybeFuncVar) is ModelbitJobResult:
        jr = maybeFuncVar
        collection.jobs.append(
            JobProps(name=jr.mb_func.__name__,
                     outVar=maybeFuncVarName,
                     rtProps=getRuntimePythonProps(jr.mb_func),
                     schedule=jr.mb_schedule,
                     redeployOnSuccess=jr.mb_redeployOnSuccess))
        maybeFuncVar = jr.mb_obj
      if "__module__" in dir(maybeFuncVar):
        if _isMainModuleFunction(maybeFuncVar):  # the user's functions
          _collectFunction(maybeFuncVar, collection)
        else:  # functions imported by the user from elsewhere
          if inspect.isclass(maybeFuncVar):
            collection.froms[maybeFuncVarName] = maybeFuncVar.__module__  #
            collection.allModules.append(maybeFuncVar.__module__)
          elif callable(maybeFuncVar) and not _hasState(maybeFuncVar):
            collection.froms[maybeFuncVarName] = maybeFuncVar.__module__  #
            collection.allModules.append(maybeFuncVar.__module__)
          elif collectedSpecialObj(maybeFuncVar, maybeFuncVarName, collection):
            pass
          elif isinstance(maybeFuncVar, object):
            collection.froms[maybeFuncVar.__class__.__name__] = maybeFuncVar.__module__
            collection.allModules.append(maybeFuncVar.__module__)
            collectPipelineModules(maybeFuncVar, collection)
            collection.vars[maybeFuncVarName] = maybeFuncVar
          else:
            collection.froms[maybeFuncVarName] = f"NYI: {maybeFuncVar.__module__}"
      elif str(maybeFuncVar).startswith('<module'):
        collection.imports[maybeFuncVarName] = maybeFuncVar.__name__
        collection.allModules.append(maybeFuncVar.__name__)
      elif inspect.isclass(maybeFuncVar):
        collection.froms[maybeFuncVarName] = maybeFuncVar.__module__  #
        collection.allModules.append(maybeFuncVar.__module__)
      else:
        collection.vars[maybeFuncVarName] = maybeFuncVar


def _collectArgTypes(func: Callable[..., Any], collection: NamespaceCollection):
  try:
    import ast

    def parseAstNameToId(astName: Any):
      if hasattr(astName, "attr"):
        return astName.value.id
      else:
        return astName.id

    def collectModName(modName: str):
      if modName in func.__globals__:
        gMod = func.__globals__[modName]
        if hasattr(gMod, "__module__"):
          collection.froms[modName] = gMod.__module__
        else:
          collection.imports[modName] = gMod.__name__
        collection.allModules.append(func.__globals__[modName].__name__)

    sigAst = ast.parse(inspect.getsource(func)).body[0]  # type: ignore

    for a in sigAst.args.args:  # type: ignore
      if a.annotation is None:  # type: ignore
        continue
      collectModName(parseAstNameToId(a.annotation))  # type: ignore
    if sigAst.returns is not None:  # type: ignore
      collectModName(parseAstNameToId(sigAst.returns))  # type: ignore
  except Exception as err:
    strErr = f"{err}"
    if (strErr != "could not get source code"):  # triggers when deploying pure sklearn model
      print(f"Warning: failed parsing type annotations: {err}")


def _extractAllNames(func: Callable[..., Any]):
  code = func.__code__
  return list(code.co_names) + list(code.co_freevars) + _extractListCompNames(func)


def _extractListCompNames(func: Callable[..., Any]):
  names: List[str] = []
  for const in func.__code__.co_consts:
    if hasattr(const, "co_names"):
      for name in list(const.co_names):
        names.append(name)
  return names


def _collectFunction(func: Callable[..., Any], collection: NamespaceCollection):
  argNames = list(func.__code__.co_varnames or [])
  funcSig = f"{func.__name__}({', '.join(argNames)})"
  if funcSig not in collection.functions:
    collection.functions[funcSig] = inspect.getsource(func)
    collectNamespaceDeps(func, collection)


def _hasState(obj: Any) -> bool:
  try:
    return len(obj.__dict__) > 0
  except:
    return False


def _isMainModuleFunction(func: Any) -> bool:
  return callable(func) and hasattr(func, "__module__") and func.__module__ == "__main__"
