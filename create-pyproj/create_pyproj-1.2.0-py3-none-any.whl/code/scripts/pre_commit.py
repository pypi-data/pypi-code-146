"""
Module Description.

pre-commit after running semantic_release
"""
import logging
import sys
from configparser import ConfigParser, NoOptionError
from pathlib import Path
from typing import Union

import tomli

logger = logging.getLogger(__name__)

DIR = Path(__file__).parent
ROOT = DIR.parent


def read_version(ROOTPATH: Path) -> str:
    with open(ROOTPATH / 'VERSION', 'r') as f:
        VERSION = f.read().strip()
    return VERSION


def write_version(version: str, ROOTPATH: Path) -> None:
    with open(ROOTPATH / 'VERSION', 'w') as f:
        f.write(version)


def read_config(ROOTPATH: Path):
    config = ConfigParser()
    config.read(ROOTPATH / 'setup.cfg')
    return config


def write_config(ROOTPATH: Union[Path, str], config: ConfigParser):
    with open(ROOTPATH / 'setup.cfg', 'w') as f:
        config.write(f)


def read_pipfile(ROOTPATH: Path):
    with open(ROOTPATH / "Pipfile", "rb") as f:
        pipfile = tomli.load(f)
    return pipfile


def set_install_requires(packages: dict, config: ConfigParser) -> ConfigParser:
    install_requires_raw = config.get('options', 'install_requires').replace('\n', ',').split(',')
    install_requires = set(x for x in install_requires_raw if x)

    for package in packages:
        install_requires.add(package)

    newline = '\n'
    config.set('options', 'install_requires', f'\n{newline.join(install_requires)}')

    return config


def set_python_version(python_version: str, config: ConfigParser) -> ConfigParser:
    python_major = python_version.split(".")[0]
    python_minor = int(python_version.split(".")[1])
    python_version_string = f"{python_major}.{python_minor}"

    config.set('options', 'python_requires', f'>={python_version_string}')
    return config


def update_config(version: str, ROOTPATH: Path) -> None:
    """
    Add dependencies from Pipfile to setup.cfg 'install_requires'.
    """
    config = read_config(ROOTPATH)
    config.set('metadata', 'version', version)

    pipfile = read_pipfile(ROOTPATH)
    try:
        config = set_install_requires(pipfile["packages"], config)
        config = set_python_version(pipfile["requires"]["python_version"], config)
    except NoOptionError:
        logger.warning("Could not find 'install_requires' in setup.cfg.")

    write_config(ROOTPATH, config)


def resolve_path():
    ROOTPATH = Path.cwd()
    if not (ROOTPATH / 'Pipfile').exists():
        if not (ROOTPATH.parent / 'Pipfile').exists():
            raise FileNotFoundError(f'Could not find Pipfile file in {ROOTPATH}')
        ROOTPATH = ROOTPATH.parent
    return ROOTPATH


def update_commit_files(version: str, ROOTPATH: Path = None):
    if not ROOTPATH:
        ROOTPATH = resolve_path()

    write_version(version, ROOTPATH)

    # If there is a setup.cfg, update it
    has_setup = (ROOTPATH / 'setup.cfg').exists()
    if has_setup:
        update_config(version, ROOTPATH)


if __name__ == '__main__':
    version = sys.argv[1]
    update_commit_files(version)
