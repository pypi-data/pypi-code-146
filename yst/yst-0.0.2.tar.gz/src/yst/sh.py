from typing import List
import os


def ls(path='.') -> List[str]:
    return os.listdir(path)


def pwd() -> str:
    os.getcwd()


def cd(path: os._FdOrAnyPath):
    os.chdir(path)
