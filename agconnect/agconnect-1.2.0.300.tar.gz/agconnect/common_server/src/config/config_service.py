# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

import abc
import json
import logging
import os
import stat
from threading import Timer

from agconnect.common_server.src.error import AGCException
from agconnect.common_server.src.error import error_message
from agconnect.common_server.src.utils import utils


class ServiceInterface(metaclass=abc.ABCMeta):
    @staticmethod
    @abc.abstractmethod
    def get_service(service_name=None):
        pass

    @staticmethod
    @abc.abstractmethod
    def get_config_value(cls, key, default_value=None):
        if key in cls.config_map:
            return cls.config_map[key]
        for _, service in ConfigService.INSTANCES.items():
            if key in service.config_map:
                return service.config_map[key]
        return default_value


class DefaultConfigService(ServiceInterface):
    config_map = {}

    def __init__(self, service_name: str, config_map: dict):
        self.service_name = service_name
        self.config_map = config_map

    @staticmethod
    def get_service(service_name=None):
        return service_name if service_name else "default"

    @classmethod
    def get_config_value(cls, key, default_value=None):
        if key in cls.config_map:
            return cls.config_map[key]
        for _, service in ConfigService.INSTANCES.items():
            if key in service.config_map:
                return service.config_map[key]
        return default_value


class ConfigService(ServiceInterface):
    CONFIG_REGEX = r"agconnect_[\\w]+.json"
    POLLING_INTERVAL_IN_MILLISECONDS = 5 * 60 * 1000
    prior_instance = DefaultConfigService(service_name="prior", config_map={})
    INSTANCES = {}
    config_map = {}

    @classmethod
    def initial_load_service_config(cls, service_name: str, config_path: str):
        utils.validate_path(config_path)
        if service_name not in cls.INSTANCES.items():
            conf = ConfigService()
            try:
                with open(config_path) as file:
                    data = json.load(file)
                for key, value in data.items():
                    conf.config_map.update({key: value})
                cls.INSTANCES.update({service_name: conf})
            except Exception as e:
                raise AGCException(error_message.ErrorCodeConstant.LOAD_SERVICE_CONFIG_ERROR) from e

    @classmethod
    def load_custom_config(cls):
        try:
            from pathlib import Path
            project_path = Path(__file__).parent.parent.parent.parent
            files = list(Path(project_path).rglob(r"agconnect_*.json"))
            cls.prior_instance.config_map.clear()
            file_len = len(files)
            file_range = range(file_len)
            for ele in file_range:
                file_path = os.path.join(project_path, files[ele])
                l_stat_result = os.stat(file_path)
                if stat.S_ISREG(l_stat_result.st_mode):
                    with open(file_path) as file:
                        data = json.load(file)
                    for key, value in data.items():
                        cls.prior_instance.config_map.update({key: value})
                else:
                    pass
        except Exception as e:
            logging.error('load custom config failed.', exc_info=e)

    @staticmethod
    def get_service(service_name=None):
        if service_name in ConfigService.INSTANCES:
            return ConfigService.INSTANCES[service_name]
        return ConfigService.prior_instance

    @staticmethod
    def start_polling_task():
        ConfigService.__set_interval(ConfigService.POLLING_INTERVAL_IN_MILLISECONDS,
                                     ConfigService.load_custom_config())

    @classmethod
    def get_config_value(cls, key, default_value=None):
        if key in cls.prior_instance.config_map:
            return cls.prior_instance.config_map[key]
        for _, service in ConfigService.INSTANCES.items():
            if key in service.config_map:
                return service.config_map[key]
        return default_value

    @staticmethod
    def __set_interval(timer, task):
        if task is None:
            return
        is_stop = task()
        if not is_stop:
            Timer(timer, ConfigService.__set_interval, [timer, task]).start()
