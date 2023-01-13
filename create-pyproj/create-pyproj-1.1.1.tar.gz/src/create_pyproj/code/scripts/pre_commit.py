"""
Module Description.

pre-commit after running semantic_release
"""
import configparser
import logging
import sys
from pathlib import Path
from typing import Union

logger = logging.getLogger(__name__)


def read_version(VERSIONPATH: Path) -> str:
    with open(VERSIONPATH / 'VERSION', 'r') as f:
        VERSION = f.read().strip()
    return VERSION


def write_version(version: str, VERSIONPATH: Path) -> None:
    with open(VERSIONPATH / 'VERSION', 'w') as f:
        f.write(version)


def read_config(VERSIONPATH: Path):
    config = configparser.ConfigParser()
    config.read(VERSIONPATH / 'setup.cfg')
    return config


def write_config(VERSIONPATH: Union[Path, str], config: configparser.ConfigParser):
    with open(VERSIONPATH / 'setup.cfg', 'w') as f:
        config.write(f)


def resolve_path():
    VERSIONPATH = Path.cwd()
    if not (VERSIONPATH / 'VERSION').exists():
        if not (VERSIONPATH.parent / 'VERSION').exists():
            raise FileNotFoundError(f'Could not find VERSION file in {VERSIONPATH}')
        VERSIONPATH = VERSIONPATH.parent
    return VERSIONPATH


def update_version_files(version: str, VERSIONPATH: Path = None):
    if not VERSIONPATH:
        VERSIONPATH = resolve_path()

    write_version(version, VERSIONPATH)

    # If there is a setup.cfg, update it
    has_setup = (VERSIONPATH / 'setup.cfg').exists()
    if has_setup:
        config = read_config(VERSIONPATH)
        config.set('metadata', 'version', version)
        write_config(VERSIONPATH, config)


if __name__ == '__main__':
    version = sys.argv[1]
    update_version_files(version)
