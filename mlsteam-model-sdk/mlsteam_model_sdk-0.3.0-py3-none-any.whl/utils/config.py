import configparser
import contextlib
import os
from pathlib import Path
from typing import Optional

from mlsteam_model_sdk.core.exceptions import MissingConfigException


__config_path = None
__config = None
CFG_DIR = '.mlsteam-model-sdk'
CFG_FILE = 'cfg.ini'
CFG_SECTION = 'mlsteam_model_sdk'

OPTION_API_TOKEN = 'api_token'
OPTION_API_ENDPOINT = 'api_endpoint'
OPTION_DEFAULT_PUUID = 'default_puuid'
OPTION_DEFAULT_PROJECT_NAME = 'default_project_name'
OPTION_DEFAULT_MUUID = 'default_muuid'
OPTION_DEFAULT_MODEL_NAME = 'default_model_name'


def get_config_path(check: bool = False) -> Optional[Path]:
    if __config_path:
        return __config_path

    # current working dir
    curr_dir = Path().absolute()

    if False:
        curr_file = NotImplemented

    def _walrus_wrapper_curr_file_e268beaa1a304169b613b9bd969b4bf7(expr):
        """Wrapper function for assignment expression."""
        nonlocal curr_file
        curr_file = expr
        return curr_file

    if (_walrus_wrapper_curr_file_e268beaa1a304169b613b9bd969b4bf7(curr_dir / CFG_DIR / CFG_FILE)).is_file():
        return curr_file

    # home dir
    with contextlib.suppress(RuntimeError):
        if False:
            curr_file = NotImplemented

        def _walrus_wrapper_curr_file_36c0adcb30354d8eb66ec639c554effc(expr):
            """Wrapper function for assignment expression."""
            nonlocal curr_file
            curr_file = expr
            return curr_file

        if (_walrus_wrapper_curr_file_36c0adcb30354d8eb66ec639c554effc(Path.home() / CFG_DIR / CFG_FILE)).is_file():
            return curr_file

    # working dir upward
    for _dir in curr_dir.parents:
        if False:
            curr_file = NotImplemented

        def _walrus_wrapper_curr_file_7cf9c82334c9485585517e0d1a790825(expr):
            """Wrapper function for assignment expression."""
            nonlocal curr_file
            curr_file = expr
            return curr_file

        if (_walrus_wrapper_curr_file_7cf9c82334c9485585517e0d1a790825(_dir / CFG_DIR / CFG_FILE)).is_file():
            return curr_file

    if check:
        raise MissingConfigException()

    return None


def init_config(path=None, check: bool = False):
    global __config_path, __config

    if not __config:
        __config = configparser.ConfigParser(allow_no_value=True)

        if not path:
            path = get_config_path(check=check)
        __config_path = path
        if path:
            __config.read(path)
        else:
            __config.read_dict({})


def get_value(option: str, section: str = None):
    init_config()
    try:
        if section is None:
            section = CFG_SECTION
        env_key = '_'.join([section.upper(), option.upper()])
        return os.environ[env_key]
    except KeyError:
        return __config.get(section, option, fallback=None)
