import os
import typing as T
from pathlib import Path
import tempfile

import validators

BITIA_MAIN_SCRIPT_NAME: T.Final[str] = "__main__.bitia.sh"


_config = {"server": "https://public.bitia.link/api/v1"}


def set_config(key, val):
    global _config
    _config[key] = val


def get_config(key, *, strict: bool = True, default=None):
    return _config[key] if strict else _config.get(key, default)


def bitia_dir() -> Path:
    """CLI cache directory"""
    bdir = Path(tempfile.gettempdir()) / "bitia"
    bdir.mkdir(parents=True, exist_ok=True)
    return bdir


def get_server(use_env: bool = True) -> str:
    """Server to use"""
    if use_env and os.environ.get("BITIA_SERVER") is not None:
        return os.environ["BITIA_SERVER"]
    return get_config("server")


def set_server(server: str):
    """set bitia server"""
    assert validators.url(server), f"{server} is not a valid url"
    set_config("server", server)
