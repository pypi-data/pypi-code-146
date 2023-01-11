from typing import List, Tuple, Dict, Optional
import os, sys, json

ALLOWED_PY_VERSIONS = ['3.6', '3.7', '3.8', '3.9', '3.10']


def listInstalledPackages():
  return [f'{p["name"]}=={p["version"]}' for p in getPipList()]


# Returns List[(desiredPackage, installedPackage|None)]
def listMissingPackagesFromPipList(
    deploymentPythonPackages: Optional[List[str]]) -> List[Tuple[str, Optional[str]]]:
  missingPackages: List[Tuple[str, Optional[str]]] = []

  if deploymentPythonPackages is None or len(deploymentPythonPackages) == 0:
    return missingPackages

  installedPackages = listInstalledPackages()
  for dpp in deploymentPythonPackages:
    if dpp not in installedPackages:
      similarPackage: Optional[str] = None
      dppNoVersion = dpp.split("=")[0].lower()
      for ip in installedPackages:
        if ip.split("=")[0].lower() == dppNoVersion:
          similarPackage = ip
      missingPackages.append((dpp, similarPackage))

  return missingPackages


def getInstalledPythonVersion():
  installedVer = f"{sys.version_info.major}.{sys.version_info.minor}"
  return installedVer


def packagesToIgnoreFromImportCheck(deploymentPythonPackages: Optional[List[str]]) -> List[str]:
  ignorablePackages: List[str] = ["modelbit"]
  if deploymentPythonPackages is None:
    return ignorablePackages

  missingPackages = listMissingPackagesFromPipList(deploymentPythonPackages)
  for mp in missingPackages:
    if mp[1] is not None:
      ignorablePackages.append(mp[1].split("=")[0])

  return ignorablePackages


# Returns List[(importedModule, pipPackageInstalled)]
def listMissingPackagesFromImports(importedModules: Optional[List[str]],
                                   deploymentPythonPackages: Optional[List[str]]) -> List[Tuple[str, str]]:
  missingPackages: List[Tuple[str, str]] = []
  ignorablePackages = packagesToIgnoreFromImportCheck(deploymentPythonPackages)
  if importedModules is None:
    return missingPackages
  if deploymentPythonPackages is None:
    deploymentPythonPackages = []

  installedModules = listInstalledPackagesByModule()
  for im in importedModules:
    baseModule = im.split(".")[0]
    if baseModule not in installedModules:
      continue  # module is likely a system module, e.g. json
    pipInstalls = installedModules[baseModule]
    missingPip = True
    for pipInstall in pipInstalls:
      pipPackage = pipInstall.split("=")[0]
      if pipInstall in deploymentPythonPackages or pipPackage in ignorablePackages:
        missingPip = False
    if missingPip:
      missingPackages.append((im, guessRecommendedPackage(baseModule, pipInstalls)))

  return missingPackages


def guessRecommendedPackage(baseModule: str, pipInstalls: List[str]):
  if len(pipInstalls) == 0:
    return pipInstalls[0]

  # pandas-stubs==1.2.0.19 adds itself to the pandas module (other type packages seem to have their own base module)
  for pi in pipInstalls:
    if "types" not in pi.lower() and "stubs" not in pi.lower():
      return pi

  return pipInstalls[0]


def getModuleNames(distInfoPath: str) -> List[str]:
  moduleNames: List[str] = []
  try:
    topLevelPath = os.path.join(distInfoPath, "top_level.txt")
    metadataPath = os.path.join(distInfoPath, "METADATA")
    if os.path.exists(topLevelPath):
      with open(topLevelPath) as f:
        moduleNames = f.read().strip().split("\n")
    elif os.path.exists(metadataPath):
      with open(metadataPath) as f:
        lines = f.read().strip().split("\n")
        for line in lines:
          if line.startswith("Name: "):
            moduleNames.append(line.split(":")[1].strip())
            break
  except:
    pass
  return moduleNames


def getPipInstallAndModuleFromDistInfo(distInfoPath: str) -> Dict[str, List[str]]:
  try:
    moduleNames = getModuleNames(distInfoPath)
    if len(moduleNames) == 0:
      return {}

    mPath = os.path.join(distInfoPath, "METADATA")
    if not os.path.exists(mPath):
      return {}

    pipName = None
    pipVersion = None
    with open(mPath) as f:
      metadata = f.read().split("\n")
      for mLine in metadata:
        if mLine.startswith("Name: "):
          pipName = mLine.split(":")[1].strip()
        if mLine.startswith("Version: "):
          pipVersion = mLine.split(":")[1].strip()
        if pipName is not None and pipVersion is not None:
          break

    if pipName is None or pipVersion is None:
      return {}

    modulesToPipVersions: Dict[str, List[str]] = {}
    for moduleName in moduleNames:
      if moduleName not in modulesToPipVersions:
        modulesToPipVersions[moduleName] = []
      modulesToPipVersions[moduleName].append(f"{pipName}=={pipVersion}")
    return modulesToPipVersions
  except Exception as err:
    print(f"Warning, unable to check module '{distInfoPath}': {err}")
    return {}


def listInstalledPackagesByModule() -> Dict[str, List[str]]:
  packages = getPipList()
  installPaths: Dict[str, int] = {}
  for package in packages:
    installPaths[package["location"]] = 1

  modulesToPipVersions: Dict[str, List[str]] = {}
  for installPath in installPaths.keys():
    try:
      for fileOrDir in os.listdir(installPath):
        if fileOrDir.endswith("dist-info"):
          dPath = os.path.join(installPath, fileOrDir)
          newModuleInfo = getPipInstallAndModuleFromDistInfo(dPath)
          for mod, pips in newModuleInfo.items():
            if mod not in modulesToPipVersions:
              modulesToPipVersions[mod] = []
            for pip in pips:
              modulesToPipVersions[mod].append(pip)
    except Exception as err:
      # See https://gitlab.com/modelbit/modelbit/-/issues/241
      print(f"Warning, skipping module '{installPath}': {err}")
      pass

  return modulesToPipVersions


def getPipList() -> List[Dict[str, str]]:
  try:
    packages: List[Dict[str, str]] = []
    import pkg_resources
    from importlib.metadata import version
    for r in pkg_resources.working_set:
      # r.version is available but can be wrong if the package was re-installed during the session, hence using importlib's version
      packages.append({"name": r.key, "version": version(r.key), "location": r.location})
    return packages
  except:
    # Some of the above isn't supported on Python 3.7, so fall back to good ol'pip
    return json.loads(os.popen("pip list -v --format json --disable-pip-version-check").read().strip())
