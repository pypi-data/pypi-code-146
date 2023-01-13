"""Settings management
"""
import os

import mflog
from pydantic import BaseSettings
from pathlib import Path

from mfire.settings.constants import CUR_DIR, SETTINGS_DIR


class Settings(BaseSettings):
    """Settings management object

    Args:
        BaseSettings : pydanctic's settings management
    """

    # general
    altitudes_dirname: Path = SETTINGS_DIR / "geos" / "altitudes"
    alternate_max: int = 2
    language: str = "fr"
    # working directory
    #   configs
    config_filename: Path = CUR_DIR / "configs" / "global_config.tgz"
    mask_config_filename: Path = CUR_DIR / "configs" / "mask_task_config.json"
    data_config_filename: Path = CUR_DIR / "configs" / "data_task_config.json"
    prod_config_filename: Path = CUR_DIR / "configs" / "prod_task_config.json"
    version_config_filename: Path = CUR_DIR / "configs" / "version_config.json"
    #   data
    data_dirname: Path = CUR_DIR / "data"
    #   mask
    mask_dirname: Path = CUR_DIR / "mask"
    #   output
    output_dirname: Path = CUR_DIR / "output"
    #   cache
    cache_dirname: Path = CUR_DIR / "cache"
    save_cache: bool = False
    # logs
    log_level: str = "WARNING"
    log_file_name: Path = None
    log_file_level: str = "WARNING"
    # vortex related
    vapp: str = "promethee"
    vconf: str = "msb"
    experiment: str = "TEST"
    # timeout
    timeout: int = 600

    class Config:
        """Config class pydantic"""

        env_prefix = "mfire_"

    @classmethod
    def set_full_working_dir(cls, working_dir: Path = CUR_DIR):
        working_dir = Path(working_dir)
        configs_dir = working_dir / "configs"
        os.environ["mfire_config_filename"] = str(configs_dir / "global_config.tgz")
        os.environ["mfire_mask_config_filename"] = str(
            configs_dir / "mask_task_config.json"
        )
        os.environ["mfire_data_config_filename"] = str(
            configs_dir / "data_task_config.json"
        )
        os.environ["mfire_prod_config_filename"] = str(
            configs_dir / "prod_task_config.json"
        )
        os.environ["mfire_version_config_filename"] = str(
            configs_dir / "version_config.json"
        )
        os.environ["mfire_data_dirname"] = str(working_dir / "data")
        os.environ["mfire_mask_dirname"] = str(working_dir / "mask")
        os.environ["mfire_output_dirname"] = str(working_dir / "output")
        os.environ["mfire_cache_dirname"] = str(working_dir / "cache")

    @classmethod
    def set(cls, **kwargs):
        """Class method for setting everything in the os.environ"""
        settings_obj = cls()
        for key, value in kwargs.items():
            if hasattr(settings_obj, key) and value is not None:
                os.environ[f"mfire_{key}"] = str(value)
        mflog.set_config(
            json_file=kwargs.get("log_file_name", None),
            json_minimal_level=kwargs.get("log_file_level", "WARNING"),
            minimal_level=kwargs.get("log_level", "WARNING"),
        )

    @classmethod
    def clean(cls):
        for key in os.environ:
            if key.startswith("mfire_"):
                del os.environ[key]
