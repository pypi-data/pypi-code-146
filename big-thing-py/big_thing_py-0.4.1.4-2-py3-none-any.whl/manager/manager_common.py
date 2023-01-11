from big_thing_py.utils import *
from enum import Enum


class SoPManagerMode(Enum):
    UNDEFINED = 'UNDEFINED'
    JOIN = 'JOIN'
    SPLIT = 'SPLIT'

    @classmethod
    def get(cls, name: str):
        try:
            return cls[name.upper()]
        except Exception:
            return cls.UNDEFINED


class SoPStaffThingInfo:
    def __init__(self, device_id: str) -> None:
        self.device_id = device_id


class StaffRegisterResult:
    def __init__(self, staff_thing_name: str, device_id: str, assigned_device_id: str) -> None:
        self.staff_thing_name = staff_thing_name
        self.device_id = device_id
        self.assigned_device_id = assigned_device_id


class SoPNewStaffThingLevel(Enum):
    NEW = 0
    DUPLICATE = 1
