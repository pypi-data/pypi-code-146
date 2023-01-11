from .helpers import RuntimePythonProps, RuntimeFile, JobProps
from typing import List, Optional


def _addSpacer(strList: List[str]):
  if len(strList) > 0 and strList[-1] != "":
    strList.append("")


def makeSourceFile(pyProps: RuntimePythonProps, sourceFileName: str, pickleOut: Optional[str] = None):

  sourceParts: List[str] = ["import modelbit, sys"]

  if pyProps.namespaceFroms:
    for iAs, iModule in pyProps.namespaceFroms.items():
      sourceParts.append(f"from {iModule} import {iAs}")
  if pyProps.namespaceImports:
    for iAs, iModule in pyProps.namespaceImports.items():
      if iModule == iAs:
        sourceParts.append(f"import {iModule}")
      else:
        sourceParts.append(f"import {iModule} as {iAs}")
  _addSpacer(sourceParts)

  if pyProps.namespaceVars and pyProps.namespaceVarsDesc:
    for nName, _ in pyProps.namespaceVars.items():
      sourceParts.append(
          f'{nName} = modelbit.load_value("data/{nName}.pkl") # {pyProps.namespaceVarsDesc[nName]}')

  if pyProps.customInitCode:
    sourceParts.append("\n" + "\n\n".join(pyProps.customInitCode))

  _addSpacer(sourceParts)
  if pyProps.namespaceFunctions:
    for _, fSource in pyProps.namespaceFunctions.items():
      sourceParts.append(fSource)
      _addSpacer(sourceParts)

  _addSpacer(sourceParts)
  if pyProps.source:
    sourceParts.append("# main function")
    sourceParts.append(pyProps.source)

  sourceParts.append("# to run locally via git & terminal")
  sourceParts.append('if __name__ == "__main__":')
  cmdArgs = "*(modelbit.parseArg(v) for v in sys.argv[1:])"
  if pickleOut is None:
    sourceParts.append(f"  print({pyProps.name}({cmdArgs}))")
  else:
    sourceParts.append("\n".join([
        f"  {pickleOut} = {pyProps.name}({cmdArgs})",
        f"  modelbit.save_value({pickleOut}, 'data/{pickleOut}.pkl')",
    ]))
  return RuntimeFile(f"{sourceFileName}.py", "\n".join(sourceParts))


def makeCreateJobRequest(job: JobProps):
  return {
      "name": job.name,
      "schedule": job.schedule,
      "redeployOnSuccess": job.redeployOnSuccess,
      "sourceFile": makeSourceFile(job.rtProps, job.name, pickleOut=job.outVar).asDict()
  }
