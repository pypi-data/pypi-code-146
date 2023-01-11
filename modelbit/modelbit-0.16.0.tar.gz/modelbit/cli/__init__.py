#!/usr/bin/env python3

import glob
import logging
import os
import shutil
import stat
import sys
from typing import NoReturn

LOGLEVEL = os.environ.get('LOGLEVEL', 'WARNING').upper()
logging.basicConfig(level=LOGLEVEL)
logger = logging.getLogger(__name__)


def printUsageAndExit() -> NoReturn:
  print("usage:")
  print("modelbit clone [target_folder]")
  exit(1)


def gitfilter(command, path=None) -> None:
  from .filter import GitApi
  from .git_protocol import GitProtocol
  from .workspace import findWorkspace

  if command == "process":
    workspaceId = findWorkspace()
    gitApi = GitApi(workspaceId)
    protocol = GitProtocol(clean=gitApi.clean, smudge=gitApi.smudge)
    protocol.filterProcess()
  else:
    # TODO: Support clean/smudge by file to help debugging
    raise Exception("clean/smudge only supported via process")


def cacheMenu(action: str) -> None:
  from .local_config import AppDirs
  if action == "clean":
    shutil.rmtree(AppDirs.user_cache_dir)
  elif action == "list":
    if not os.path.exists(AppDirs.user_cache_dir):
      print("Cache empty")
      return
    for filepath in glob.iglob(os.path.join(AppDirs.user_cache_dir, "**"), recursive=True):
      statinfo = os.stat(filepath)
      if not stat.S_ISDIR(statinfo.st_mode):
        relpath = os.path.relpath(filepath, AppDirs.user_cache_dir)
        print(f"{statinfo[stat.ST_SIZE]}\t{relpath}")


def main() -> None:
  if len(sys.argv) < 2:
    printUsageAndExit()
  cmd = sys.argv[1]
  args = sys.argv[2:]
  try:
    if cmd == "clone":
      from .clone import clone
      return clone(*args)
    elif cmd == "gitfilter":
      return gitfilter(*args)
    elif cmd == "cache":
      return cacheMenu(*args)
    elif cmd == "describe":
      from .describe import describeCmd
      return describeCmd(*args)
    elif cmd == "version":
      from modelbit import __version__
      print(__version__)
      exit(0)
  except TypeError as e:
    # Catch wrong number of args
    logger.info("Bad command line", exc_info=e)
    printUsageAndExit()
  except KeyboardInterrupt:
    exit(1)
  except Exception as e:
    raise
  printUsageAndExit()


if __name__ == '__main__':
  main()
