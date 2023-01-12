# -*- coding: utf-8 -*-
# *******************************************************
#   ____                     _               _
#  / ___|___  _ __ ___   ___| |_   _ __ ___ | |
# | |   / _ \| '_ ` _ \ / _ \ __| | '_ ` _ \| |
# | |__| (_) | | | | | |  __/ |_ _| | | | | | |
#  \____\___/|_| |_| |_|\___|\__(_)_| |_| |_|_|
#
#  Sign up for free at http://www.comet.ml
#  Copyright (C) 2021 Comet ML INC
#  This file can not be copied and/or distributed without the express
#  permission of Comet ML Inc.
# *******************************************************

from abc import ABCMeta
from typing import Any, Awaitable, Dict, Optional
from urllib.parse import urljoin


def batch_endpoint_url(server_address: str) -> str:
    # TODO: Check that server_address finishes with a "/"
    return urljoin(server_address, "events/batch")


CLOSE_MESSAGE = object()


class BaseSender(metaclass=ABCMeta):
    def connect(self) -> None:
        ...  # pragma: no cover

    def put(self, item: Any) -> Optional[Awaitable[None]]:
        ...  # pragma: no cover

    def close(self) -> None:
        ...  # pragma: no cover

    def join(self, timeout: int) -> Optional[Awaitable[None]]:
        ...  # pragma: no cover


def model_base_event(model_name: str, model_version: str) -> Dict[str, str]:
    return {"modelName": model_name, "modelVersion": model_version}
