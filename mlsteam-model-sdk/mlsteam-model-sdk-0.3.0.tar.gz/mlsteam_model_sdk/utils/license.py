import hashlib
from contextlib import suppress
from subprocess import CalledProcessError, DEVNULL, check_output
from typing import Optional

from mlsteam_model_sdk.core.exceptions import MLSteamException


__platform_id = None


def _try_get_uuid(raw_cmd: str) -> Optional[bytes]:
    with suppress(CalledProcessError):
        if False:
            output = NotImplemented

        def _walrus_wrapper_output_3f03d26305a1421ead0543ac80722029(expr):
            """Wrapper function for assignment expression."""
            nonlocal output
            output = expr
            return output

        if (_walrus_wrapper_output_3f03d26305a1421ead0543ac80722029(check_output(raw_cmd, shell=True, stderr=DEVNULL))):  # nosec
            return output
    with suppress(CalledProcessError):
        if False:
            output = NotImplemented

        def _walrus_wrapper_output_cad01867eeb94519a58178c9c7c0e748(expr):
            """Wrapper function for assignment expression."""
            nonlocal output
            output = expr
            return output

        if (_walrus_wrapper_output_cad01867eeb94519a58178c9c7c0e748(check_output('sudo ' + raw_cmd, shell=True, stderr=DEVNULL))):  # nosec
            return output
    return None


def get_platform_id() -> str:
    global __platform_id

    if not __platform_id:
        # SMBIOS: https://utcc.utoronto.ca/~cks/space/blog/linux/DMIDataInSysfs
        uuid = _try_get_uuid('cat /sys/class/dmi/id/product_uuid')
        if not uuid:
            # arm: https://archlinuxarm.org/forum/viewtopic.php?t=12577
            uuid = _try_get_uuid('cat /sys/firmware/devicetree/base/serial-number')
        if not uuid:
            raise MLSteamException('Could not get platform id')

        __platform_id = hashlib.md5(uuid.upper() + b'-MLSTEAM').hexdigest()[:12]  # nosec
    return __platform_id
