#!/usr/bin/env python
# -*- coding=utf-8 -*-
from __future__ import annotations
from typing import Dict, List


class JsonSchema(dict):
    def __init__(self, json: Dict):
        super().__init__(json)

    @staticmethod
    def parse(json: Dict) -> JsonSchema:
        if json is None:
            return None
        if "$ref" in json:
            return ReferenceSchema(json)
        if "allOf" in json:
            return CombineAllofSchema(json)
        if "anyOf" in json:
            return CombineAnyofSchema(json)
        if "oneOf" in json:
            return CombineOneofSchema(json)
        if json.get("type") == "string":
            return StringSchema(json)
        elif json.get("type") == "integer":
            return IntegerSchema(json)
        elif json.get("type") == "boolean":
            return BooleanSchema(json)
        elif json.get("type") == "number":
            return NumberSchema(json)
        elif json.get("type") == "array":
            return ArraySchema(json)
        elif json.get("type") == "object":
            return ObjectSchema(json)
        elif json.get("type") == "file":
            return ObjectSchema(json)
        else:
            return JsonSchema(json)

    @property
    def type(self):
        return self.get("type")

    @property
    def title(self):
        return self.get("title")

    @property
    def default(self):
        return self.get("default")

    @property
    def examples(self):
        return self.get("examples")

    @property
    def description(self):
        return self.get("description")

    def get_py_type_name(self) -> str:
        if self.type is not None:
            return self.type
        raise Exception("Unkown schema type: {}".format(self))


class ReferenceSchema(JsonSchema):

    @property
    def value(self) -> str:
        return self.get("$ref")

    def evaluate(self, root):
        map = root
        for key in self.value.split("/")[1:]:
            map = map[key]
        return JsonSchema.parse(map)

    def get_py_type_name(self):
        if self.get("$ref"):
            return self.value.split("/")[-1]


class StringSchema(JsonSchema):

    def is_enum(self):
        return "enum" in self

    @property
    def enum(self):
        return self.get("enum")

    def get_py_type_name(self):
        return "str"


class IntegerSchema(JsonSchema):

    def get_py_type_name(self):
        return "int"


class BooleanSchema(JsonSchema):

    def get_py_type_name(self):
        return "bool"


class NumberSchema(JsonSchema):

    def get_py_type_name(self):
        return "float"


class ArraySchema(JsonSchema):

    @property
    def items(self):
        return JsonSchema.parse(self.get("items"))

    def get_py_type_name(self):
        return "List[{}]".format(self.items.get_py_type_name())


class FileSchema(JsonSchema):

    def get_py_type_name(self):
        return "bytes"


class ObjectSchema(JsonSchema):

    @property
    def properties(self):
        if self.get("properties") is None:
            return None
        return {k: JsonSchema.parse(self.get("properties")[k]) for k in self.get("properties")}

    @property
    def additionalProperties(self):
        if self.get("additionalProperties") is None:
            return None
        return JsonSchema.parse(self.get("additionalProperties"))

    def get_py_type_name(self):
        if self.get("additionalProperties") is not None:
            if self.get("additionalProperties").get("$ref"):
                return self.additionalProperties.get_py_type_name()
            else:
                return "Dict[str, {}]".format(self.additionalProperties.get_py_type_name())
        return "Dict"


class CombineAllofSchema(JsonSchema):

    def get_py_type_name(self):
        if isinstance(self.get("allOf"), list) and len(self.get("allOf")) == 1:
            return JsonSchema.parse(self.get("allOf")[0]).get_py_type_name()


class CombineAnyofSchema(JsonSchema):

    def get_py_type_name(self):
        if isinstance(self.get("anyOf"), list) and len(self.get("anyOf")) == 1:
            return JsonSchema.parse(self.get("anyOf")[0]).get_py_type_name()


class CombineOneofSchema(JsonSchema):

    def get_py_type_name(self):
        if isinstance(self.get("oneOf"), list) and len(self.get("oneOf")) == 1:
            return JsonSchema.parse(self.get("oneOf")[0]).get_py_type_name()