import io
import logging
import pickle
import pprint
from typing import Any, Dict, Optional

import yaml

logger = logging.getLogger(__name__)

SCHEMA_VERSION = 1
MAX_DESCRIPTION_SIZE = 5000
NULL_BYTE = b"\x00"


def repr_str(dumper: yaml.Dumper, data: str):
  if '\n' in data:
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
  return dumper.represent_scalar('tag:yaml.org,2002:str', data)


def toYaml(contentHash: str, fileSize: int, objDesc: Dict[str, Any]) -> str:
  metadata: Dict[str, Any] = {"file_size": fileSize, "object": objDesc}

  obj = toFileStubDict(contentHash, metadata)
  yaml.add_representer(str, repr_str)
  return yaml.dump(obj, width=1000)


def toFileStubDict(contentHash: str, objDesc: Dict[str, Any]) -> Dict[str, Any]:
  return {"_": "MBFileStub", "contentHash": contentHash, "metadata": objDesc, "schemaVersion": SCHEMA_VERSION}


def describeFile(content: bytes, maxDepth: int = 1) -> Dict[str, Any]:
  pickleDetails = getPickleInfo(content, maxDepth)
  if pickleDetails:
    return pickleDetails
  else:
    return describeObject(content, maxDepth)


def decodeString(b: bytes) -> str:
  for encoding in ('ascii', 'utf8', 'latin1'):
    try:
      return b.decode(encoding)
    except UnicodeDecodeError:
      pass
  return b.decode('ascii', 'ignore')


def describeObject(obj: Any, maxDepth: int, remainingCharacters=MAX_DESCRIPTION_SIZE) -> Dict[str, Any]:
  objT = type(obj)
  if objT is dict and maxDepth > 0:
    ret = {}
    for k, v in obj.items():
      ret[k] = describeObject(v, maxDepth - 1, max(0, remainingCharacters))
      remainingCharacters -= len(str(ret[k]))
    return ret
  elif objT is bytes:
    if isBinaryFile(obj):
      obj = "Unknown binary file"
    else:
      obj = decodeString(obj)
      objT = type(obj)
  description = obj[:remainingCharacters].strip() if type(obj) is str else pprint.pformat(
      obj, depth=1, width=100, compact=True)[:remainingCharacters].strip()
  return {
      "module": objT.__module__,
      "class": objT.__name__,
      "description": description,
  }


def getPickleInfo(content: bytes, maxDepth: int) -> Optional[Dict[str, Any]]:
  try:
    import joblib
    obj = joblib.load(io.BytesIO(content))
    return describeObject(obj, maxDepth)
  except Exception as e:
    logger.debug("Failed to parse as joblib", exc_info=e)
    pass

  try:
    obj = pickle.loads(content)
    return describeObject(obj, maxDepth)
  except Exception as e:
    logger.debug("Failed to parse as pickle", exc_info=e)
    return {}


def isBinaryFile(content: bytes) -> bool:
  return NULL_BYTE in content


def describeCmd(filepath=None, depth="1"):
  import sys

  from .secure_storage import calcHash

  if filepath is not None:
    with open(filepath, "rb") as f:
      content = f.read()
  else:
    content = sys.stdin.buffer.read()

  print(toYaml(calcHash(content), len(content), describeFile(content, int(depth))))
