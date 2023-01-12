# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

import json
import os
from typing import Callable, Any

from agconnect.common_server.src.credential_service.client_id_credential import ClientIdCredential
from agconnect.common_server.src.credential_service.credential_service import CredentialService
from agconnect.common_server.src.credential_service.credential_type import CredentialType
from agconnect.common_server.src.error.error import AGCException
from agconnect.common_server.src.error.error_message import ErrorCodeConstant
from agconnect.common_server.src.utils.utils import validate_path

UserDefinedGetClientSecret = Callable[[Any], str]


class CredentialParser:
    __AGC_CONFIG_ENV_VAR = 'AGC_CONFIG'

    @staticmethod
    def to_credential(file_path=None, func: UserDefinedGetClientSecret = None) -> CredentialService:
        if file_path:
            CredentialParser.check_json_file(file_path)
            with open(file_path) as file:
                data = json.load(file)
        else:
            try:
                env_path = os.environ.get(CredentialParser.__AGC_CONFIG_ENV_VAR)
            except TypeError as e:
                raise AGCException(ErrorCodeConstant.CREDENTIAL_ENV_NOT_SET) from e
            else:
                if env_path is None or not os.path.exists(env_path):
                    raise AGCException(ErrorCodeConstant.CREDENTIAL_ENV_NOT_SET)
                CredentialParser.check_json_file(env_path)
                with open(env_path) as file:
                    data = json.load(file)
        return CredentialParser.to_credential_with_contents(json.dumps(data), func)

    @staticmethod
    def to_credential_with_contents(contents: str, func: UserDefinedGetClientSecret = None) -> CredentialService:
        obj = json.loads(contents)
        if obj is None:
            raise AGCException(ErrorCodeConstant.GET_CREDENTIAL_NULL)
        client_secret = None
        if "type" in obj:
            if obj["type"] == CredentialType.TEAM_CLIENT_ID.value:
                if func is not None:
                    client_secret = func()
                else:
                    client_secret = obj["client_secret"]
                    obj["type"] = CredentialType.TEAM_CLIENT_ID
                client_team = ClientIdCredential(project_id='', region='', developer_id=obj['developer_id'],
                                                 project_type=obj['type'], client_id=obj['client_id'],
                                                 client_sec=client_secret,
                                                 configuration_version=obj['configuration_version'])
                return client_team

            elif obj["type"] == CredentialType.PROJECT_CLIENT_ID.value:
                if func is not None:
                    client_secret = func()
                else:
                    client_secret = obj["client_secret"]
                    obj["type"] = CredentialType.PROJECT_CLIENT_ID
                client_project = ClientIdCredential(project_id=obj['project_id'], region=obj['region'],
                                                    developer_id=obj['developer_id'], project_type=obj['type'],
                                                    client_id=obj['client_id'], client_sec=client_secret,
                                                    configuration_version=obj['configuration_version'])
                return client_project
            else:
                raise AGCException(ErrorCodeConstant.CREDENTIAL_PARSER)
        else:
            raise AGCException(ErrorCodeConstant.CREDENTIAL_PARSER)

    @staticmethod
    def check_json_file(file_path: str):
        try:
            validate_path(file_path)
        except Exception as e:
            raise AGCException(ErrorCodeConstant.AGC_CLIENT_CREDENTIAL) from e
