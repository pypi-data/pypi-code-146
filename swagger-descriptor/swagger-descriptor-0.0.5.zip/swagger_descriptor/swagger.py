#!/usr/bin/env python
# -*- coding=utf-8 -*-
from typing import Dict, List, Optional

from .json_schema import JsonSchema


class Swagger(dict):
    def __init__(self, swagger: Dict):
        super().__init__(swagger)
        self._definitions = swagger.get("definitions", {})
        self._apis: List[APIDescriptor] = []
        for url, url_info in swagger.get("paths", {}).items():
            for method, method_info in url_info.items():
                self._apis.append(self._parse_api(method, url, method_info))

    @property
    def apis(self):
        return self._apis

    @property
    def definitions(self):
        return self._definitions

    def get_definition_by_ref(self, ref):
        map = self._swagger
        for key in ref.split("/")[1:]:
            map = map[key]
        return JsonSchema(map)

    def _parse_api(self, method: str, url: str, descriptor: Dict):
        return APIDescriptor(method, url, descriptor)


class APIDescriptor(object):
    def __init__(self, method, url, descriptor):
        self.__method: str = method
        self.__url: str = url
        self.__summary: str = descriptor.get("summary", "")
        self.__operation_id: str = descriptor.get("operationId", "")
        self.__tags: List[str] = descriptor.get("tags", [])
        self.__description: str = descriptor.get("description", "")
        self.__parameters: List[ParameterDescriptor] = []
        self.__response: Dict = descriptor["responses"]["200"]
        for param in descriptor.get("parameters", []):
            self.__parameters.append(ParameterDescriptor(param))

    @property
    def method(self):
        return self.__method

    @property
    def url(self):
        return self.__url

    @property
    def summary(self):
        return self.__summary

    @property
    def operation_id(self):
        return self.__operation_id

    @property
    def tags(self):
        return self.__tags

    @property
    def description(self):
        return self.__description

    @property
    def parameters(self):
        return self.__parameters

    @property
    def response(self):
        return self.__response


class ParameterDescriptor(dict):

    @property
    def name(self) -> str:
        return self.get("name")

    @property
    def _in(self) -> str:
        return self.get("in")

    @property
    def description(self) -> Optional[str]:
        return self.get("description")

    @property
    def schema(self):
        return self.get("schema")