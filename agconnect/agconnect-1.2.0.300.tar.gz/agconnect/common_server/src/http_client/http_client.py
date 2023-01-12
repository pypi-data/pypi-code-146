# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Union, AsyncIterator

from agconnect.common_server.src.error import AGCException
from agconnect.common_server.src.http_client.http_client_api import HttpClientCfg, HttpClientApiImpl
from agconnect.common_server.src.log_config.common_log import logger


def get_http_client(cfg: Union[HttpClientCfg, dict] = None):
    if type(cfg) is dict:
        return Root(HttpClientCfg(dictionary=cfg)).client()
    logger.info('step into getHttpClient method ')
    return Root(cfg).client()


@dataclass(frozen=True)
class Root:
    cfg: Union[HttpClientCfg, dict]

    @asynccontextmanager
    async def client(self) -> AsyncIterator[HttpClientApiImpl]:
        client = HttpClientApiImpl(self.cfg)
        try:
            yield client
        except AGCException as e:
            raise e
        finally:
            await client.close()
