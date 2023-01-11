from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod


class AssetsActions:
    Mkdir = "mkdir"
    Remove = "remove"
    Get = "get"
    Link = "link"
    Binary = "binary"
    Download = "download"
    Copy = "copy"
    List = "list"
