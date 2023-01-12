import dataclasses
import json
import logging
import sys
from enum import Enum
from typing import List, Dict, Iterable

import requests

from datetime import datetime

from tcsoa.config import TcSoaConfig
from tcsoa.exceptions import InvalidCredentialsException, InternalServerException, ServiceException, Severity, \
    InnerException
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBoClass


class RestBackend:
    def __init__(self, host: str):
        """
        Initializes the REST Backend. Should be useable for all Teamcenter Backends which have AWC installed.

        @param host: The address to your web server - for example: http://webserver:7001/tc
        """
        self.host = host
        self.base_url = f'{self.host}/RestServices'
        self.policy = {
            "useRefCount": False,
            "types": list()
        }
        self.state = {
            "stateless": True,
            "unloadObjects": True,
            "enableServerStateHeaders": True,
            "formatProperties": True,
            "clientID": "TcSoaClient"
        }
        self.session = requests.session()
        self.session.trust_env = False
        self.session.proxies = {
            "http": None,
            "https": None,
        }

    def _get_object_load_policy_for_bo(self, bo_name):
        types_list = self.policy['types']
        matching_type = list(t for t in types_list if t['name'] == bo_name)
        if matching_type:
            object_policy = matching_type[0]
        else:
            object_policy = {
                'name': bo_name
            }
            types_list.append(object_policy)
        return object_policy

    def set_object_load_policy(self, bo_name, properties: List[str]):
        object_policy = self._get_object_load_policy_for_bo(bo_name)
        object_policy['properties'] = [{'name': p} for p in properties]

    def add_object_load_policy(self, bo_name, properties: List[str]):
        object_policy = self._get_object_load_policy_for_bo(bo_name)
        objs_props = object_policy.setdefault('properties', [])
        for prop in properties:
            if not any(p for p in objs_props if p['name'] == prop):
                objs_props.append({'name': prop})

    def clear_object_load_policy(self, bo_name):
        self.policy['types'] = list(t for t in self.policy['types'] if t['name'] != bo_name)

    def clear_all_object_load_policies(self):
        self.policy['types'] = list()

    def input_obj_to_json(self, input_obj):
        if input_obj is None:
            return ''
        if type(input_obj) in (str, int, float, bool):
            return input_obj
        if isinstance(input_obj, TcBoClass):
            return {k: self.input_obj_to_json(v) for k, v in input_obj.__dict__.items() if k != 'props'}
        if dataclasses.is_dataclass(input_obj):
            return {k[:-1] if k.endswith('_') else k: self.input_obj_to_json(v) for k, v in input_obj.__dict__.items()}
        if isinstance(input_obj, datetime):
            return input_obj.strftime(TcSoaConfig.date_format)
        if isinstance(input_obj, Enum):
            return input_obj.value
        if isinstance(input_obj, dict):
            return {k: self.input_obj_to_json(v) for k, v in input_obj.items()}
        if type(input_obj) in (list, set, tuple) or isinstance(input_obj, Iterable):
            return [self.input_obj_to_json(o) for o in input_obj]
        raise NotImplementedError()

    def response_to_output_obj(self, response_cls, response):
        try:
            response_data: Dict[str: any] = response.json()
            qname = response_data.pop('.QName')
            if qname == 'http://teamcenter.com/Schemas/Soa/2006-03/Exceptions.InvalidCredentialsException':
                raise InvalidCredentialsException(**self._data_to_exception(response_data))
            if qname == 'http://teamcenter.com/Schemas/Soa/2006-03/Exceptions.ServiceException':
                raise ServiceException(**self._data_to_exception(response_data))
            if qname == 'http://teamcenter.com/Schemas/Soa/2006-03/Exceptions.InternalServerException':
                raise InternalServerException(**self._data_to_exception(response_data))

            if response_cls:
                response_data = self.dataclass_from_dict(response_cls, response_data)
            return response_data
        except ValueError:
            # note to self: when XML is returned, you dont have a valid cookie
            return response.content  # todo: handle this better

    def _data_to_exception(self, data):
        messages = data.get('messages', None)
        inner_exs = ()
        if messages:
            data = messages[0]
            inner_exs = [InnerException(**self._data_to_exception(m)) for m in messages[1:]]
        return dict(message=data['message'], code=data['code'], level=Severity(data['level']), inner_exceptions=inner_exs)

    @staticmethod
    def eval_str_type(cls, field):
        """ Black Magic - Evaluates the type annotation in context of the class """
        return eval(field, globals(), sys.modules[cls.__module__].__dict__)

    @staticmethod
    def dataclass_from_dict(cls, from_dict):
        try:
            fieldtypes = cls.__annotations__
        except AttributeError:
            if dataclasses.is_dataclass(cls):
                fieldtypes = dict()     # __annotations__ is only set to data classes with attributes
            elif getattr(cls, '__origin__', None) == dict and isinstance(from_dict, list):
                # special case: from_dict is a tuple, containing 2 lists, where the first list contains keys, and
                # the second list contains the values
                return {
                    RestBackend.dataclass_from_dict(cls.__args__[0], key):
                        RestBackend.dataclass_from_dict(cls.__args__[1], from_dict[1][idx])
                    for idx, key in enumerate(from_dict[0])}
            elif isinstance(from_dict, (tuple, list)):
                return [RestBackend.dataclass_from_dict(cls.__args__[0], f) for f in from_dict]
            elif isinstance(from_dict, dict):
                return {
                    RestBackend.dataclass_from_dict(cls.__args__[0], k):
                        RestBackend.dataclass_from_dict(cls.__args__[1], v)
                    for k, v in from_dict.items()
                }
            else:
                # logging.warning(f'Warning! Expected attribute class {str(cls)} but received {from_dict} !')
                return from_dict

        instance = cls()
        # if isinstance(from_dict, list) and len(from_dict) == 1 and isinstance(from_dict[0], dict):
        #     from_dict = from_dict[0]    # HACK! can't believe I have to do this! mainly for class `FileTicketsResponse`
        for f in from_dict:
            dest_f = f
            if f == 'ServiceData' and 'serviceData' in fieldtypes:
                dest_f = 'serviceData'

            if dest_f in fieldtypes:
                field = fieldtypes[dest_f]
            else:
                logging.debug(f'Warning! unregistered attribute "{f}" is tried to be set on class "{cls.__name__}"!')
                setattr(instance, dest_f, from_dict[f])
                continue

            if isinstance(field, str):  # black magic incoming
                field = RestBackend.eval_str_type(cls, field)
            setattr(instance, dest_f, RestBackend.dataclass_from_dict(field, from_dict[f]))
        if TcSoaConfig.global_obj_cache_enabled:
            if isinstance(instance, ServiceData):
                TcSoaConfig.internal_handle_sd(instance)
        return instance

    def execute(self, service_id, method_name, input_obj, response_cls):
        json_body = dict(
            header=dict(
                state=self.state,
                policy=self.policy,
            ),
            body=self.input_obj_to_json(input_obj)
        )
        url = f'{self.base_url}/{service_id}/{method_name}'
        data = json.dumps(json_body, ensure_ascii=False).encode('utf8')
        response = self.session.post(url, data=data, headers={
            'Operation-Name': method_name,
            'App-Xml': 'application/json',
            'Content-Type': 'application/json',
        })
        response.encoding = "utf-8"
        response_obj = self.response_to_output_obj(response_cls, response)
        return response_obj
