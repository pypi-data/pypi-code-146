import json
from typing import Any

from ..interfaces.deserializer import Deserializer
from ..interfaces.serializer import Serializer

JSONText = str
JSONObject = Any


class JSONSerializer(Serializer[JSONObject, JSONText]):
    def serialize(self, value: JSONObject) -> JSONText:
        return json.dumps(value)


class JSONDeserializer(Deserializer[JSONText, JSONObject]):
    def deserialize(self, value: JSONText) -> JSONObject:
        return json.loads(value)
