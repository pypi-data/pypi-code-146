# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

from typing import Callable, Any

from agconnect.common_server.src.agc_client.agc_client import AGCClient
from agconnect.common_server.src.config.config_service import ConfigService
from agconnect.common_server.src.service.agc_service import AGCService


class ServiceFactory:
    SERVICE_INSTANCE_MAP = {str: [AGCService]}
    SERVICES = []
    FactoryAlias = Callable[[Any], AGCService]

    @staticmethod
    def initialize_service(client: AGCClient, service_name: str, fact: FactoryAlias,
                           config_path: str, *args):
        if not client:
            client = AGCClient.get_instance()
        if ServiceFactory.SERVICE_INSTANCE_MAP.get(client.get_name()):
            service_array = ServiceFactory.SERVICE_INSTANCE_MAP.get(client.get_name())
            for service_item in service_array:
                if service_item.get_service_name() == service_name:
                    return service_item
            ConfigService.initial_load_service_config(service_name, config_path)
            service_item = fact(*args)
            service_item.initialize(client)
            service_array.append(service_item)
            return service_item
        else:
            ConfigService.initial_load_service_config(service_name, config_path)
            service_item = fact(*args)
            service_item.initialize(client)
            ServiceFactory.SERVICES.append(service_item)
            ServiceFactory.SERVICE_INSTANCE_MAP.update({client.get_name(): ServiceFactory.SERVICES})
            return service_item
