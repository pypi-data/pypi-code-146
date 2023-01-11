#
#  Copyright (c) 2022 Russell Smiley
#
#  This file is part of click_logging_parameters.
#
#  You should have received a copy of the MIT License along with click_logging_parameters.
#  If not, see <https://opensource.org/licenses/MIT>.
#

import copy
import typing

import click
import pytest

import click_logging_config._logging
from click_logging_config import LoggingConfiguration, logging_parameters


@pytest.fixture()
def mock_file_handler(mocker):
    mocker.patch(
        "click_logging_config._logging.logging.handlers.RotatingFileHandler"
    )
    mocker.patch.object(click_logging_config._logging.logging, "getLogger")


CallbackCallable = typing.Callable[[click.Context], None]


@pytest.fixture()
def mock_main() -> typing.Callable[[CallbackCallable], click.BaseCommand]:
    def _apply(
        callback: CallbackCallable,
        user_defaults: typing.Optional[LoggingConfiguration] = None,
    ) -> click.BaseCommand:
        @click.command()
        @click.option("--p", default=None, type=str)
        @logging_parameters(user_defaults)
        def this_main(p: typing.Optional[str]) -> None:
            c = click.get_current_context()
            c.obj["p"] = p
            callback(c)

        return this_main

    return _apply
