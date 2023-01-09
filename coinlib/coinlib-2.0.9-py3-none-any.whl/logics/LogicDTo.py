from enum import Enum

from coinlib.helper import Serializable


class CollectionFieldTypes(Enum):
    string = "string"
    timestamp = "timestamp"
    number = "number"

class CollectionField(Serializable):
    name: str
    unique: bool
    type: CollectionFieldTypes
