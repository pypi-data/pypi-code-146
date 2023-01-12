# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

import os
from abc import ABCMeta
from enum import Enum, auto

from agconnect.common_server.src.config.config_service import ConfigService
from agconnect.common_server.src.credential_service.credential_parser import CredentialParser
from agconnect.common_server.src.credential_service.credential_service import CredentialService
from agconnect.common_server.src.error.error import AGCException
from agconnect.common_server.src.error.error_message import ErrorCodeConstant
from agconnect.common_server.src.log_config.common_log import logger

path = os.path.normpath(os.path.join(os.path.dirname(__file__), './../../agconnect_common.json'))
ConfigService.load_custom_config()
ConfigService.initial_load_service_config('COMMON', path)
ConfigService.start_polling_task()


class Region(Enum):
    CN = auto()
    RU = auto()
    SG = auto()
    DE = auto()


class AGCClientService(metaclass=ABCMeta):
    def __init__(self, name: str, credential: CredentialService):
        self.name = name
        self.credential = credential

    def get_name(self) -> str:
        return self.name

    def get_credential(self) -> CredentialService:
        return self.credential


class AGCClient(AGCClientService):
    INSTANCES = {}
    __DEFAULT_INSTANCE_NAME = "default"
    __REGIONS = [Region.CN.name, Region.DE.name, Region.RU.name, Region.SG.name]
    __credential = CredentialService

    def __init__(self, name: str, credential: CredentialService):
        super().__init__(name, credential)

    def get_name(self) -> str:
        return super(AGCClient, self).get_name()

    def get_credential(self) -> CredentialService:
        return self.__credential

    @classmethod
    def __set_credential(cls, credential: CredentialService):
        cls.__credential = credential

    @staticmethod
    def initialize(name: str = None, credential: CredentialService = None, region: str = None):
        logger.info('start to initialize AgcClient')
        if region:
            if region not in AGCClient.__REGIONS:
                logger.error(f"invalid region: {region}")
                raise AGCException(ErrorCodeConstant.INVALID_REGION)
        if isinstance(name, str):
            name = name.strip()
        if name is None or len(name) < 1:
            name = AGCClient.__DEFAULT_INSTANCE_NAME
        if name in AGCClient.INSTANCES:
            logger.error(f"instance already exists: {name}")
            raise AGCException(ErrorCodeConstant.AGC_CLIENT_EXIST)
        inner_credential = credential
        if inner_credential is None:
            logger.info("credential is undefined so use default")
            inner_credential = CredentialParser.to_credential()
        else:
            if not isinstance(credential, CredentialService):
                logger.info("credential is invalid")
                raise Exception(ErrorCodeConstant.AGC_CLIENT_CREDENTIAL)
        logger.info(f"add instance : {name}")
        AGCClient.INSTANCES.update({name: AGCClientService(name, inner_credential)})
        if region:
            AGCClient.__override_region(name, region)

    @staticmethod
    def get_instance(name: str = __DEFAULT_INSTANCE_NAME):
        if name is None:
            name = AGCClient.__DEFAULT_INSTANCE_NAME
            if name not in AGCClient.INSTANCES:
                AGCClient.initialize()
        if name not in AGCClient.INSTANCES:
            logger.error(f"{ErrorCodeConstant.AGC_CLIENT_NOT_EXIST} | name: {name}")
            raise AGCException(ErrorCodeConstant.AGC_CLIENT_NOT_EXIST)
        return AGCClient.INSTANCES[name]

    @staticmethod
    def __override_region(name, region):
        AGCClient.get_instance(name).get_credential().set_region(region)
