import logging
import os
import re
from typing import Union

import tomli
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel

LOG = logging.getLogger(__name__)


router = APIRouter(
    prefix="/api/v1/version",
    tags=["version"],
)


def get_current_version() -> Union[str, None]:
    current_version = None
    try:
        current_file_dir = os.path.dirname(os.path.realpath("__file__"))
        version_file = os.path.join(current_file_dir, "pyproject.toml")
        LOG.info(f"version file path: {version_file}")
        pyproject = {}
        with open(version_file, mode="rb") as f:
            pyproject = tomli.load(f)

        version_maybe = pyproject.get("tool", {}).get("poetry", {}).get("version", "")
        pattern = re.compile(r"([0-9]+\.){2}([0-9]+)")
        m = re.match(pattern, version_maybe)
        if m is None:
            LOG.error("Could not read version file")
            return None

        current_version = m.group(0)
        LOG.info(f"Version file has been read and version is set to {current_version}")
        return current_version
    except Exception as ex:
        LOG.error(f"Could not read version file {ex}")
        return None


class Version(BaseModel):
    version: str


@router.get("", response_model=Version)
async def get_version():
    current_version = get_current_version()
    LOG.info(f"The current version is {current_version}")
    return JSONResponse(content={"version": current_version})
