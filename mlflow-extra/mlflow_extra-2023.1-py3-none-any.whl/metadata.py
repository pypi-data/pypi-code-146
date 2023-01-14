#!/usr/bin/env python3
'''
Find and manipulate MLflow metadata files.
'''

import logging
import os
import pathlib
import shutil
import tempfile

import yaml

from mlflow_extra.uri import URITransformer

LOGGER = logging.getLogger(__name__)


class Metadata():
    '''
    Metadata wrapper.
    '''
    FILENAME = 'meta.yaml'

    FIELD_ARTIFACT_LOCATION = 'artifact_location'  # experiment metadata
    FIELD_ARTIFACT_URI = 'artifact_uri'  # run metadata
    FIELD_CREATION_TIME = 'creation_time'
    FIELD_EXPERIMENT_ID = 'experiment_id'
    FIELD_LAST_UPDATE_TIME = 'last_update_time'
    FIELD_LIFECYCLE_STAGE = 'lifecycle_stage'
    FIELD_NAME = 'name'

    def __init__(self, path=None, data=None):
        '''
        Args:
            path:
                The path to a metadata file, or a directory that contains one.
                If not None, then the data will be loaded from the path unless
                data is also passed via the data parameter.

            data:
                The data. If not None, then the path will not be loaded.
        '''
        if path is not None:
            path = pathlib.Path(path).resolve()
            if path.is_dir():
                path /= self.FILENAME
        self.path = path

        self.data = {} if data is None else data

        if self.path and data is None:
            self.load()

    def load(self, path=None):
        '''
        Load data from a YAML file.

        Args:
            path:
                The filepath. If None, the current path will be used.
        '''
        path = self.path if path is None else pathlib.Path(path).resolve()
        if path is None:
            raise ValueError('no path set')
        if self.path is None:
            self.path = path
        with path.open('rb') as handle:
            self.data = yaml.safe_load(handle)

    def save(self, path=None):
        '''
        Save data to a YAML file.

        Args:
            path:
                The filepath. If None, the current path will be used.
        '''
        # Attempt to write to a temporary file first to ensure that the metadata
        # file is not destroyed if the data cannot be converted to YAML.
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_dir = pathlib.Path(tmp_dir)
            tmp_path = tmp_dir / self.FILENAME
            with tmp_path.open('w', encoding='utf-8') as handle:
                yaml.dump(self.data, handle)
            path = self.path if path is None else pathlib.Path(path).resolve()
            path.parent.mkdir(parents=True, exist_ok=True)
            LOGGER.debug('Saving data to %s', path)
            shutil.move(tmp_path, path)

    @staticmethod
    def non_negative_int(value):
        '''
        Check that the given value is a non-negative integer.

        Args:
            value:
                The value to check.

        Returns:
            The value as an int.

        Raises:
            ValueError:
                The value could not be converted to a non-negative int.
        '''
        value = int(value)
        if value < 0:
            raise ValueError('negative value')
        return value

    def _get_experiment_id(self):
        return self.data.get(self.FIELD_EXPERIMENT_ID)

    def _set_experiment_id(self, value):
        self.data[self.FIELD_EXPERIMENT_ID] = self.non_negative_int(value)

    experiment_id = property(
        fget=_get_experiment_id,
        fset=_set_experiment_id,
        doc='The experiment ID'
    )

    def _get_name(self):
        return self.data.get(self.FIELD_NAME)

    def _set_name(self, value):
        value = str(value)
        if not value:
            raise ValueError('empty name')
        self.data[self.FIELD_NAME] = value

    name = property(
        fget=_get_name,
        fset=_set_name,
        doc='The name'
    )

    def _get_creation_time(self):
        return self.data.get(self.FIELD_CREATION_TIME)

    def _set_creation_time(self, value):
        self.data[self.FIELD_CREATION_TIME] = self.non_negative_int(value)

    creation_time = property(
        fget=_get_creation_time,
        fset=_set_creation_time,
        doc='The creation time'
    )

    def _get_last_update_time(self):
        return self.data.get(self.FIELD_LAST_UPDATE_TIME)

    def _set_last_update_time(self, value):
        self.data[self.FIELD_LAST_UPDATE_TIME] = self.non_negative_int(value)

    last_update_time = property(
        fget=_get_last_update_time,
        fset=_set_last_update_time,
        doc='The last update time'
    )

    def _get_lifecycle_stage(self):
        return self.data.get(self.FIELD_LIFECYCLE_STAGE)

    def _set_lifecycle_stage(self, value):
        value = str(value)
        if not value:
            raise ValueError('empty lifecycle_stage')
        self.data[self.FIELD_LIFECYCLE_STAGE] = value

    lifecycle_stage = property(
        fget=_get_lifecycle_stage,
        fset=_set_lifecycle_stage,
        doc='The lifecycle stage'
    )

    @property
    def is_experiment(self):
        '''
        True if the current metadata appears to be for an experiment and not a
        run.
        '''
        return self.FIELD_ARTIFACT_LOCATION in self.data

    @property
    def _artifact_uri_field(self):
        '''
        Get the artifact URI field or equivalent depending on the type of file.
        '''
        return self.FIELD_ARTIFACT_LOCATION \
            if self.FIELD_ARTIFACT_LOCATION in self.data \
            else self.FIELD_ARTIFACT_URI

    def _get_artifact_uri(self):
        return URITransformer(self.data.get(self._artifact_uri_field))

    def _set_artifact_uri(self, value):
        if not isinstance(value, URITransformer):
            value = URITransformer(value)
        if not value.parts[2]:
            raise ValueError('empty artifact path')
        self.data[self._artifact_uri_field] = str(value)

    artifact_uri = property(
        fget=_get_artifact_uri,
        fset=_set_artifact_uri,
        doc='The artifact URI or equivalent'
    )

    def find_meta(self, path):
        '''
        Find all MLflow metadata files in the given directory.

        Args:
            path:
                The directory path.

        Returns:
            A generator over the metadata file paths as pathlib.Path objects.
        '''
        path = pathlib.Path(path).resolve()
        for root, _dirs, files in os.walk(path):
            if self.FILENAME in files:
                yield self.__class__(path=root)
