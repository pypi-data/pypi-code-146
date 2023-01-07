from enum import Enum


class StorageType(Enum):
    PICKLE = "pickle"
    JSON = "json"
    REDIS = "redis"
