from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod


class ExpireOptions:
    NX = "NX"
    XX = "XX"
    GT = "GT"
    LT = "LT"
