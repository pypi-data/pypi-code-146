#!/usr/bin/env python3

'''
Path management.
'''

import logging
import os
import pathlib
import sys


from hydronaut.types import Path


LOGGER = logging.getLogger(__name__)


class PathManager():
    '''
    Path manager. This provides methods to retrieve common paths.
    '''
    HYDRONAUT_CONFIG_ENV_VAR = 'HYDRONAUT_CONFIG'

    def __init__(self, base_dir: Path = None) -> None:
        '''
        Args:
            base_dir:
                The directory relative to which to interpret paths. If None, the
                current working directory is used.
        '''
        self.base_dir = pathlib.Path.cwd() if base_dir is None else pathlib.Path(base_dir).resolve()
        LOGGER.debug('PathManager base directory: %s', self.base_dir)

    def add_python_paths(self, paths: list[Path]) -> None:
        '''
        Add Paths to the Python system paths list. The resulting list will be the
        equivalent of concatenating the input paths with the current system paths.

        Args:
            paths:
                The paths to add. If relative, they are interpreted relative to the
                path given by relative_to.
        '''
        if not paths:
            return
        paths = [str(self.base_dir.joinpath(path)) for path in paths]
        for path in paths:
            LOGGER.debug('adding %s to Python system path', path)
        sys.path[:] = [*paths, *sys.path]

    @property
    def config_dir(self) -> pathlib.Path:
        '''
        Returns:
            The resolved path to the current configuration directory as a
            pathlib.Path object.
        '''
        return (self.base_dir / 'conf').resolve()

    def get_config_path(self, subpath: Path = None) -> pathlib.Path:
        '''
        Get the path to a configuration file.

        subpath:
            The subpath relative to the configuration directory. If None,
            defaults to config.yaml.

        Returns:
            The resolved path to the configuration file as a pathlib.Path
            object.
        '''
        if subpath is None:
            subpath = os.getenv(self.HYDRONAUT_CONFIG_ENV_VAR, default='config.yaml')
        return self.config_dir / subpath

    def get_src_path(self, subpath: Path) -> pathlib.Path:
        '''
        Get the path to a Python source file in the default source directory.

        subpath:
            The subpath relative to the source directory.

        Returns:
            The resolved path to the source file as a pathlib.Path object.
        '''
        return self.base_dir / 'src' / subpath
