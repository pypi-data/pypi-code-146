from dataclasses import dataclass, field, asdict
from typing import Dict, List, Generic, TypeVar
from abc import ABC, abstractmethod


class SchedulerActions:
    Create = "create"
    Cancel = "cancel"
    List = "list"
    Get = "get"
