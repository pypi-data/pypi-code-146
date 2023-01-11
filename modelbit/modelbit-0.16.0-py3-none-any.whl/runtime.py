from typing import Union, List, Dict, Any, Callable, Tuple, Optional, cast
import re, json, pandas, pickle

from .environment import ALLOWED_PY_VERSIONS, getInstalledPythonVersion
from .helpers import DeploymentTestDef, DeploymentTestError, RuntimePythonProps, getJson, getJsonOrPrintError, getMissingPackageWarningsFromEnvironment, getMissingPackageWarningsFromImportedModules, isAuthenticated, getDefaultPythonVersion, getDefaultPythonPackages, getDefaultSystemPackages
from .ux import COLORS, DifferentPythonVerWarning, GenericError, GenericTip, WarningErrorTip, makeCssStyle, TableHeader, printTemplate, renderTemplate
from .secure_storage import uploadRuntimeObject
from .collect_dependencies import getFuncSource, getRuntimePythonProps, getFuncArgNames
from .source_generation import makeSourceFile, makeCreateJobRequest


class RuntimeStatusNotes:

  def __init__(self, tips: List[WarningErrorTip], warnings: List[WarningErrorTip],
               errors: List[WarningErrorTip]):
    self.tips = tips
    self.warnings = warnings
    self.errors = errors
    self.deployable = len(errors) == 0

  def statusMsg(self):
    if self.deployable:
      return 'Ready'
    return 'Not Ready'

  def statusStyle(self):
    if self.deployable:
      return "color:green; font-weight: bold;"
    return "color:gray; font-weight: bold;"


class Runtime:

  MAX_REQUIREMENTS_TXT = 20_000
  LAMBDA_RAM_MAX_MB = 10_240
  LAMBDA_RAM_MIN_MB = 128

  def __init__(self,
               name: Optional[str] = None,
               main_function: Optional[Callable[..., Any]] = None,
               python_version: Optional[str] = None,
               requirements_txt_filepath: Optional[str] = None,
               requirements_txt_contents: Optional[List[str]] = None,
               python_packages: Optional[List[str]] = None,
               system_packages: Optional[List[str]] = None,
               docker_run: Optional[str] = None,
               source_override: Optional[str] = None,
               dataframe_mode: bool = False,
               example_dataframe: Optional[pandas.DataFrame] = None):
    self._pythonPackages: Optional[List[str]] = None
    self._systemPackages: Optional[List[str]] = None
    self._dockerRun: Optional[str] = None
    self._deployName: Optional[str] = None
    self._deployFunc: Optional[Callable[..., Any]] = None
    self._sourceOverride = source_override
    self._testOutputs: List[Tuple[bool, DeploymentTestDef, Dict[str, str]]] = []
    self._dataframeMode = dataframe_mode
    self._dataframe_mode_columns: Optional[List[Dict[str, str]]] = None

    self._pythonVersion = getDefaultPythonVersion()
    self.set_python_packages(getDefaultPythonPackages())
    self.set_system_packages(getDefaultSystemPackages())

    if name:
      self.set_name(name)
    if main_function:
      self._set_main_function(main_function)
    if python_version:
      self.set_python_version(python_version)
    if requirements_txt_filepath:
      self.set_requirements_txt(filepath=requirements_txt_filepath)
    if requirements_txt_contents:
      self.set_requirements_txt(contents=requirements_txt_contents)
    if python_packages is not None:
      self.set_python_packages(python_packages)
    if system_packages is not None:
      self.set_system_packages(system_packages)
    if docker_run:
      self.set_docker_run(docker_run)

    if dataframe_mode and example_dataframe is not None:
      self._dataframe_mode_columns = self._collectDataFrameModeColumns(example_dataframe)
    elif dataframe_mode and example_dataframe is None:
      raise Exception("The example_dataframe parameter is required when passing dataframe_mode=True")
    elif not dataframe_mode and example_dataframe is not None:
      raise Exception("Setting dataframe_mode=True is required when passing the example_dataframe parameter")

    self._prepEnvironment()

  def _repr_html_(self):
    return self._describeHtml()

  def __repr__(self):
    return self._describeHtml()

  def set_name(self, name: str):
    if not re.match('^[a-zA-Z0-9_]+$', name):
      raise Exception("Names should be alphanumeric with underscores.")
    self._deployName = name
    return self

  def set_python_version(self, version: str):
    if version not in ALLOWED_PY_VERSIONS:
      return self._selfError(f'Python version should be one of {ALLOWED_PY_VERSIONS}.')
    self._pythonVersion = version
    return self

  def set_requirements_txt(self, filepath: Optional[str] = None, contents: Optional[List[str]] = None):
    lines: List[str] = []
    if filepath != None and type(filepath) == str:
      f = open(filepath, "r")
      lines = [n.strip() for n in f.readlines()]
      return self.set_python_packages(lines)
    elif contents != None:
      return self.set_python_packages(contents)
    return self

  def set_python_packages(self, packages: Optional[List[str]]):
    if packages is None:
      self._pythonPackages = None
      return
    if type(packages) != list:
      raise Exception("The python_packages parameter must be a list of strings.")
    for pkg in packages:
      if type(pkg) != str:
        raise Exception("The python_packages parameters must be a list of strings.")
      if "\n" in pkg or "\r" in pkg:
        raise Exception("The python_packages parameters cannot contain newlines")
      if "==" not in pkg:
        raise Exception(
            f"The python_packages parameter '{pkg}' is formatted incorrectly. It should look like 'package-name==X.Y.Z'"
        )
    self._pythonPackages = packages

  def set_system_packages(self, packages: Optional[List[str]]):
    if packages is None:
      self._systemPackages = None
      return
    if type(packages) != list:
      raise Exception("The system_packages parameter must be a list of strings.")
    for pkg in packages:
      if type(pkg) != str:
        raise Exception("The system_packages parameters must be a list of strings.")
      if "\n" in pkg or "\r" in pkg:
        raise Exception("The system_packages parameters cannot contain newlines.")
    self._systemPackages = packages

  def set_docker_run(self, commands: Optional[str]):
    if commands is None:
      self._dockerRun = None
      return
    if type(commands) != str:
      raise Exception("The docker_run parameter must be a string.")
    if "\n" in commands or "\r" in commands:
      raise Exception("The docker_run parameter cannot contain newlines.")
    self._dockerRun = commands

  def _set_main_function(self, func: Callable[..., Any]):
    self._deployFunc = func
    if callable(func) and self._deployName == None:
      self.set_name(func.__name__)
    tests = self._getTests()
    if tests == None:
      self._testOutputs = []
    elif len(tests) > 0 and self._dataframeMode:
      raise Exception("Unit tests are not supported in dataframe_mode")
    else:
      self._testOutputs = self._getTestOutputs(tests)
    return self

  def _getRequirementsTxt(self):
    if self._pythonPackages:
      return "\n".join(self._pythonPackages)
    else:
      return None

  def _prepEnvironment(self):
    getJson(
        "jupyter/v1/runtimes/prep_environment", {
            "environment": {
                "requirementsTxt": self._getRequirementsTxt(),
                "pythonVersion": self._pythonVersion,
                "systemPackages": self._systemPackages,
                "dockerRun": self._dockerRun,
            }
        })

  def _getRuntimePythonProps(self):
    props: Optional[RuntimePythonProps] = None
    error: Optional[GenericError] = None
    try:
      props = getRuntimePythonProps(self._deployFunc, sourceOverride=self._sourceOverride)
    except Exception as err:
      error = GenericError(str(err))
    return props, error

  def deploy(self):
    printTemplate("runtime-pre-deploy", None, deploymentName=self._deployName)

    status = self._getStatusNotes()
    if not status.deployable:
      printTemplate("error", None, errorText="Unable to deploy.")
      return self

    rtProps, error = self._getRuntimePythonProps()
    if error is not None or rtProps is None:
      printTemplate("error", None, errorText="Unable to continue because errors are present.")
      return self

    printTemplate("runtime-deploying",
                  None,
                  deploymentName=self._deployName,
                  warningsList=status.warnings,
                  tipsList=status.tips,
                  errorsList=status.errors)

    dataFiles = self._makeAndUploadDataFiles(rtProps)
    resp = getJsonOrPrintError(
        "jupyter/v1/runtimes/create", {
            "runtime": {
                "name": self._deployName,
                "dataFiles": dataFiles,
                "pyState": {
                    "sourceFile": makeSourceFile(rtProps, self._sourceFileName()).asDict(),
                    "valueFiles": {},
                    "name": rtProps.name,
                    "module": self._sourceFileName(),
                    "argNames": rtProps.argNames,
                    "argTypes": rtProps.argTypes,
                    "requirementsTxt": self._getRequirementsTxt(),
                    "pythonVersion": self._pythonVersion,
                    "systemPackages": self._systemPackages,
                    "dockerRun": self._dockerRun,
                    "dataframeModeColumns": self._dataframe_mode_columns,
                },
                "jobs": [makeCreateJobRequest(j) for j in rtProps.jobs]
            }
        })
    if not isAuthenticated():
      return None
    if not resp:
      printTemplate("error", None, errorText='Error processing request: no response from server.')
    elif resp.error:
      printTemplate("error", None, errorText=f'Error processing request: {resp.error}')
    elif resp.runtimeOverviewUrl:
      printTemplate("runtime-deployed",
                    None,
                    deploymentName=self._deployName,
                    deployMessage=resp.message,
                    deployTimeWords=self._parseTimeFromDeployMessage(resp.message),
                    runtimeOverviewUrl=resp.runtimeOverviewUrl)
    else:
      printTemplate(
          "error",
          None,
          errorText="Unknown error while processing request (server response in unexpected format).")
    return None

  # a bit of a hack for now
  def _parseTimeFromDeployMessage(self, message: Optional[str]):
    if not message:
      return None
    if "will be ready in" in message:
      return message.split("will be ready in")[1]
    return None

  def _sourceFileName(self):
    return "source"

  def _makeAndUploadDataFiles(self, pyState: RuntimePythonProps):
    dataFiles: Dict[str, str] = {}
    if pyState.namespaceVars:
      for nName, nVal in pyState.namespaceVars.items():
        dataFiles[f"data/{nName}.pkl"] = uploadRuntimeObject(nVal, pickle.dumps(nVal), nName)
    if pyState.extraDataFiles is not None:
      for nName, nObjBytes in pyState.extraDataFiles.items():
        dataFiles[f"data/{nName}.pkl"] = uploadRuntimeObject(nObjBytes[0], nObjBytes[1], nName)
    for job in pyState.jobs:
      dataFiles.update(self._makeAndUploadDataFiles(job.rtProps))
    return dataFiles

  def _selfError(self, txt: str):
    printTemplate("error", None, errorText=txt)
    return None

  def _describeHtml(self):
    customStyles = {
        "readyStyle": makeCssStyle({"color": COLORS["success"]}),
        "errorStyle": makeCssStyle({"color": COLORS["error"]}),
        "passStyle": makeCssStyle({
            "color": COLORS["success"],
            "font-weight": "bold"
        }),
        "failStyle": makeCssStyle({
            "color": COLORS["error"],
            "font-weight": "bold"
        }),
    }
    status = self._getStatusNotes()
    funcProps, error = self._getRuntimePythonProps()
    if funcProps is None:
      if error is not None:
        raise Exception(f"Unable to capture deployment function: {error.errorText}")
      else:
        raise Exception(f"Unable to capture deployment function")

    propHeaders = [
        TableHeader("Property", TableHeader.LEFT),
        TableHeader("Value", TableHeader.LEFT, isCode=True),
    ]
    propRows: List[List[str]] = []

    funcSig = '(None)'
    if funcProps.name and funcProps.argNames:
      funcSig = f"{funcProps.name}({', '.join(funcProps.argNames)})"
    propRows.append(["Function", funcSig])

    if funcProps.namespaceFunctions and len(funcProps.namespaceFunctions) > 0:
      nsFuncs = "\n".join([k for k, _ in funcProps.namespaceFunctions.items()])
      propRows.append(["Helpers", nsFuncs])

    if funcProps.namespaceVarsDesc and len(funcProps.namespaceVarsDesc) > 0:
      nsVars = "\n".join([f'{k}: {v}' for k, v in funcProps.namespaceVarsDesc.items()])
      propRows.append(["Values", nsVars])

    nsImports: List[str] = []
    if funcProps.namespaceFroms and len(funcProps.namespaceFroms) > 0:
      for k, v in funcProps.namespaceFroms.items():
        nsImports.append(f'from {v} import {k}')
    if funcProps.namespaceImports and len(funcProps.namespaceImports) > 0:
      for k, v in funcProps.namespaceImports.items():
        nsImports.append(f'import {v} as {k}')
    if len(nsImports) > 0:
      propRows.append(["Imports", '\n'.join(nsImports)])

    propRows.append(["Python Version", self._pythonVersion])

    if self._pythonPackages and len(self._pythonPackages) > 0:
      maxDepsShown = 7
      if len(self._pythonPackages) > maxDepsShown:
        deps = "\n".join([d for d in self._pythonPackages[:maxDepsShown]])
        numLeft = len(self._pythonPackages) - maxDepsShown
        deps += f'\n...and {numLeft} more.'
      else:
        deps = "\n".join([d for d in self._pythonPackages])
      propRows.append(["Python packages", deps])

    if self._systemPackages:
      propRows.append(["System packages", ", ".join(self._systemPackages)])

    if self._dockerRun:
      propRows.append(["Docker RUN", self._dockerRun])

    testHeaders = [
        TableHeader("Status", TableHeader.LEFT, isPassFail=True),
        TableHeader("Command", TableHeader.LEFT, isCode=True),
        TableHeader("Result", TableHeader.LEFT, isCode=True),
    ]
    testRows: List[List[Union[str, bool]]] = []
    for tOut in self._testOutputs:
      result: List[str] = []
      metadata = tOut[2]
      if "error" in metadata:
        result.append(f'Error: {metadata["error"]}')
      if "expected" in metadata:
        result.append(f'Expected: {metadata["expected"]}')
      if "received" in metadata:
        result.append(f'Received: {metadata["received"]}')
      testRows.append([tOut[0], tOut[1].command, " ".join(result)])

    return renderTemplate("runtime-description",
                          styles=customStyles,
                          runtimeName=self._deployName,
                          deployable=status.deployable,
                          warningsList=status.warnings,
                          tipsList=status.tips,
                          errorsList=status.errors,
                          properties={
                              "headers": propHeaders,
                              "rows": propRows
                          },
                          tests={
                              "headers": testHeaders,
                              "rows": testRows
                          })

  def _getStatusNotes(self):
    tips: List[WarningErrorTip] = []
    warnings: List[WarningErrorTip] = []
    errors: List[WarningErrorTip] = []
    rtPyProps: Optional[RuntimePythonProps] = None

    # Errors
    if not self._deployName:
      errors.append(GenericError("This deployment needs a name."))
    if not self._deployFunc:
      errors.append(GenericError("This deployment needs a deploy_function."))
    else:
      rtPyProps, propError = self._getRuntimePythonProps()
      if propError is not None:
        errors.append(propError)
    for tOut in self._testOutputs:
      if tOut[0] == False:  # failed test
        errors.append(GenericError("This deployment has failing tests."))
        break
    if not isAuthenticated():
      errors.append(GenericError("You are not logged in to Modelbit. Please log in, then deploy."))

    # Tips
    if len(self._testOutputs) == 0 and not self._dataframeMode:
      tips.append(
          GenericTip("Add unit tests to improve this deployment.",
                     "https://doc.modelbit.com/#/deployments/unit-tests"))

    # Warnings
    depPackages = self._pythonPackages
    if depPackages is None:
      depPackages = getDefaultPythonPackages()
    warnings += getMissingPackageWarningsFromEnvironment(depPackages)
    if (rtPyProps is not None):
      warnings += getMissingPackageWarningsFromImportedModules(rtPyProps.namespaceModules, depPackages)

    localPyVersion = getInstalledPythonVersion()
    if self._pythonVersion != localPyVersion:
      warnings.append(DifferentPythonVerWarning(self._pythonVersion, localPyVersion))

    return RuntimeStatusNotes(tips, warnings, errors)

  def _getTests(self):
    if not callable(self._deployFunc) or self._deployFunc.__doc__ is None:
      return None
    funcName = self._deployFunc.__name__
    funcSource = self._sourceOverride if self._sourceOverride is not None else getFuncSource(self._deployFunc)
    resp = getJsonOrPrintError("jupyter/v1/runtimes/parse_tests", {
        "funcName": funcName,
        "funcSource": funcSource,
    })
    if resp:
      return resp.tests
    return None

  def _runTest(self, test: DeploymentTestDef):
    if not callable(self._deployFunc):
      return False
    if test.args == None:
      return self._deployFunc()
    return self._deployFunc(*test.args)  # type: ignore

  def _getTestOutputs(self,
                      tests: List[DeploymentTestDef]) -> List[Tuple[bool, DeploymentTestDef, Dict[str, str]]]:
    return [self._getTestOutput(t) for t in tests]

  def _getTestOutput(self, test: DeploymentTestDef) -> Tuple[bool, DeploymentTestDef, Dict[str, str]]:

    if test.error:
      errorMessage = "Unable to run test."
      if test.error == DeploymentTestError.UnknownFormat.value:
        errorMessage = "Unknown test format"
      if test.error == DeploymentTestError.ExpectedNotJson.value:
        errorMessage = "Expected value must be JSON serializable"
      if test.error == DeploymentTestError.CannotParseArgs.value:
        errorMessage = "Unable to parse function arguments."
      return (False, test, {"error": errorMessage})

    result = self._runTest(test)
    try:
      jResult = json.loads(json.dumps(result))  # dump+load helps clean up numbers like 2.00000000001
      if jResult != test.expectedOutput:
        return (False, test, {"expected": json.dumps(test.expectedOutput), "received": json.dumps(jResult)})
    except:
      return (False, test, {"error": "Output must be JSON serializable.", "received": type(result).__name__})
    return (True, test, {"expected": json.dumps(test.expectedOutput)})

  def _collectDataFrameModeColumns(self, df: pandas.DataFrame) -> List[Dict[str, Union[str, Any]]]:
    if len(getFuncArgNames(self._deployFunc)) != 1:
      raise Exception("When using dataframe_mode, the deploy function can only have one input argument.")
    config: List[Dict[str, Any]] = []
    examples: Optional[Dict[str, Any]] = None
    if len(df) > 0:
      examples = cast(Dict[str, Any], json.loads(df.head(1).to_json(orient="records"))[0])  # type: ignore
    for col in cast(List[str], list(df.columns)):
      cf = {"name": col, "dtype": str(df[col].dtype)}
      if examples is not None:
        cf["example"] = examples[col]
      config.append(cf)
    return config


class Deployment(Runtime):

  def __init__(self,
               name: Optional[str] = None,
               deploy_function: Optional[Callable[..., Any]] = None,
               python_version: Optional[str] = None,
               requirements_txt_filepath: Optional[str] = None,
               requirements_txt_contents: Optional[List[str]] = None,
               python_packages: Optional[List[str]] = None,
               system_packages: Optional[List[str]] = None,
               docker_run: Optional[str] = None,
               source_override: Optional[str] = None,
               dataframe_mode: bool = False,
               example_dataframe: Optional[pandas.DataFrame] = None):
    Runtime.__init__(self,
                     name=name,
                     main_function=deploy_function,
                     python_version=python_version,
                     requirements_txt_filepath=requirements_txt_filepath,
                     requirements_txt_contents=requirements_txt_contents,
                     python_packages=python_packages,
                     system_packages=system_packages,
                     docker_run=docker_run,
                     source_override=source_override,
                     dataframe_mode=dataframe_mode,
                     example_dataframe=example_dataframe)

  def set_deploy_function(self, func: Callable[..., Any]):
    self._set_main_function(func)
