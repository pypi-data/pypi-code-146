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

import logging
from typing import TYPE_CHECKING, Any, Callable, Optional, TypeVar

from pydantic import BaseSettings, PositiveInt, ValidationError

from .logging_messages import INVALID_SETTING_DEFAULT_FALLBACK

if TYPE_CHECKING:
    from pydantic.typing import CallableGenerator  # pragma: no cover

    # Make mypy happy, https://github.com/samuelcolvin/pydantic/issues/1490#issuecomment-630131270
    AnyHttpUrl = str  # pragma: no cover
else:
    from pydantic import AnyHttpUrl

LOGGER = logging.getLogger(__name__)


def log_level_validator(value: Any) -> int:
    if isinstance(value, int):
        if value not in logging._levelToName.keys():
            raise ValueError("Invalid logging level %r" % value)
        return value
    elif not isinstance(value, str):
        raise ValueError("Invalid logging level name %r" % value)
    else:
        level = logging._nameToLevel.get(value.upper(), None)
        if level is None:
            raise ValueError("Invalid logging level name %r" % value)
        return level


class LogLevel(int):
    @classmethod
    def __get_validators__(cls) -> "CallableGenerator":
        yield log_level_validator


class LogSettings(BaseSettings):
    mpm_logging_console: LogLevel = LogLevel(logging.INFO)
    mpm_logging_propagate: bool = False
    mpm_logging_file: Optional[str] = None
    mpm_logging_file_level: Optional[LogLevel] = None
    mpm_logging_file_overwrite: bool = False

    class Config:
        env_prefix = "comet_"


class MPMSettings(BaseSettings):
    # Use same names as the Python SDK to ease configuration
    api_key: str
    url: AnyHttpUrl = "https://www.comet-ml.com/"

    mpm_workspace_name: str
    mpm_model_name: str
    mpm_model_version: str

    mpm_max_batch_size: PositiveInt = 1000
    mpm_max_batch_time: PositiveInt = 60
    mpm_join_timeout: PositiveInt = 30
    mpm_batch_sending_timeout: PositiveInt = 5 * 60  # 5 minutes

    class Config:
        env_prefix = "comet_"


MODEL = TypeVar("MODEL", bound="BaseSettings")


def get_model(m: Callable[..., MODEL], **kwargs: Any) -> MODEL:
    try:
        return m(**kwargs)
    except ValidationError as e:
        for error in e.errors():
            # This should always be a str when dealing with non-nested fields
            error_loc = error["loc"][0]
            assert isinstance(error_loc, str)
            # TODO: Display better error
            # Use the default value instead

            # This is either an extra field or something else that we cannot handle so re-raise original exception
            if error_loc not in m.__fields__:  # type: ignore
                raise

            # The __fields__ attribute is not officially documented
            kwargs[error_loc] = m.__fields__[error_loc].get_default()  # type: ignore

        LOGGER.warning(
            INVALID_SETTING_DEFAULT_FALLBACK,
            exc_info=True,
        )

        return m(**kwargs)
