import asyncio
import logging
import os

import pytest
from fhempy.lib.pkg_installer import check_and_install_dependencies
from tests.utils import mock_fhem


@pytest.mark.asyncio
async def test_everything(mocker):
    # prepare
    mock_fhem.mock_module(mocker)
    testhash = {"NAME": "testdevice", "FHEMPYTYPE": "volvo"}
    await check_and_install_dependencies("volvo")
    from fhempy.lib.volvo.volvo import volvo

    fhempy_device = volvo(logging.getLogger(__name__))
    await fhempy_device.Define(
        testhash,
        [
            "testdevice",
            "fhempy",
            "volvo",
            os.environ["VOLVO_API_KEY"],
            os.environ["VOLVO_ACCESS_TOKEN"],
        ],
        {},
    )

    # send command
    # await fhempy_device.Set(
    #    testhash,
    #    ["testdevice", "lock"],
    #    {},
    # )
    await asyncio.sleep(30)
