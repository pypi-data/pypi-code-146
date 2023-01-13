import io
import json
import logging
import os
import tarfile
import tempfile
import time
from typing import Dict, List, Optional, Union

import requests
import yaml
from truss.truss_handle import TrussHandle

from baseten.common import api
from baseten.common.core import raises_api_error
from baseten.common.lib_support import (build_h5_data_object,
                                        coerce_input_to_json, version_gte)

logger = logging.getLogger(__name__)

REQUIREMENTS_INSTALLATION_STATUS_RETRY_INTERVAL_SEC = 3
REQUIREMENTS_INSTALLATION_STATUS_MAX_TRIES = 20


@raises_api_error
def install_requirements(req_filepath: str):
    with open(req_filepath, 'r') as fp:
        requirements_txt = fp.read()
    logger.info('🚀 Sending requirements to BaseTen 🚀')
    resp = api.install_requirements(requirements_txt)
    status = resp['status']
    if status == 'PROCESSING':
        logger.info('🐳 Requirements are being installed 🐳')

        requirement_id = resp['id']
        tries = 0
        while tries < REQUIREMENTS_INSTALLATION_STATUS_MAX_TRIES:
            time.sleep(REQUIREMENTS_INSTALLATION_STATUS_RETRY_INTERVAL_SEC)
            resp = api.requirement_status(requirement_id)
            status = resp['status']
            if status != 'PROCESSING':
                break
            tries += 1
        else:
            logger.info('⌛ Requirements are still being installed. Check the status by running '
                        f'baseten.requirements_status(\'{requirement_id}\') ⌛')
    if status == 'SUCCEEDED':
        logger.info('🖖 Installed requirements successfully 🖖')
    elif status == 'FAILED':
        error_message = resp['error_message']
        logger.info(f'⚠️ Failed to install requirements. Error: "{error_message}" ⚠️')


@raises_api_error
def requirements_status(requirement_id: str):
    return api.requirement_status(requirement_id)


class BasetenDeployedModel:
    """A model backed by baseten serving. Provide either the model_id or the model_version_id."""

    @raises_api_error
    def __init__(self, model_id: Optional[str] = None,
                 model_version_id: Optional[str] = None,
                 external_model_version_id: Optional[str] = None,
                 model_name: Optional[str] = None,
                 model_zoo_name: Optional[str] = None,
                 truss_handle: Optional[TrussHandle] = None,
                 truss_spec_version: Optional[str] = None):
        if not model_id and not model_version_id and not external_model_version_id:
            raise ValueError('Either model_id, model_version_id, or external_model_version_id must be provided.')

        if (
            model_id
            and (model_version_id or external_model_version_id)
            or (external_model_version_id and model_version_id)
        ):
            raise ValueError(
                'Must provide only one of model_id, model_version_id, or external_model_version_id; not more.')

        self._model_id = model_id
        self._model_version_id = model_version_id
        self._external_model_version_id = external_model_version_id
        if self._external_model_version_id:
            self._model_version_id = api.model_version_external_id_get_version(self._external_model_version_id)

        self._model_name = model_name
        self._truss_spec_version = truss_spec_version
        self.model_zoo_name = model_zoo_name
        self.truss_handle = truss_handle

    @property
    def model_version_id(self):
        return self._model_version_id

    @raises_api_error
    def predict(self,
                inputs,
                metadata=None,
                prediction_only: bool = True) -> Union[List[List], Dict]:
        """Invokes the model given the input dataframe.

        Args:
            inputs: The data representing one or more inputs to call the model with.
                Accepted types are: list, pandas.DataFrame, and numpy.ndarray
            metadata (Union[pd.DataFrame, List[Dict]]): Metadata key/value pairs (e.g. name, url), one for each input.
            prediction_only (bool): set to `False` for the full response (including probablities).

        Returns:
            A list of inferences for each given input; e.g.: [[3], [9]] would indicate the prediction for the
            first input in inputs_df is [3], and the prediction for the second is [9].

        Raises:
            TypeError: If the provided inputs is not of a supported type.
            ApiError: If there was an error communicating with the server.
        """
        if self._truss_spec_version is None:
            self._truss_spec_version = self.get_truss_spec_version()

        if version_gte(self._truss_spec_version, "2.0"):
            if self._model_version_id:
                return api.predict_for_model_version(
                    self._model_version_id, inputs, v2=True
                )
            return api.predict_for_model(self._model_id, inputs, v2=True)

        inputs_list, metadata = coerce_input_to_json(inputs, metadata)

        if self._model_version_id:
            return api.predict_for_model_version(self._model_version_id, inputs_list, metadata, prediction_only)
        return api.predict_for_model(self._model_id, inputs_list, metadata, prediction_only)

    @raises_api_error
    def update_model_features(self, model_config_file_path: str):
        """Update the model's feature names and output class labels (if any) based on the config
        found at `model_config_file_path`

        Args:
            model_config_file_path (str): The path to the model config file
        """
        config_yaml = yaml.safe_load(open(model_config_file_path, 'r'))
        feature_names = list(config_yaml['model_features']['features'])
        class_labels = config_yaml.get('model_class_labels', [])
        api.update_model_features(self._model_version_id, feature_names, class_labels)

    @raises_api_error
    def set_primary(self):
        """Promote this version of the model as the primary version.
        Raises:
            ApiError: If there was an error communicating with the server.
        """
        if not self._model_version_id:
            raise ValueError('Only a BasetenDeployedModel backed by a model_version can be set as primary.')
        return api.set_primary(self._model_version_id)

    @raises_api_error
    def deactivate(self):
        """Deactivate this version of the model.
        Raises:
            ApiError: If there was an error communicating with the server.
        """
        if not self._model_version_id:
            raise ValueError('Only a BasetenDeployedModel backed by a model_version can be set as primary.')
        return api.deactivate_model_version(self._model_version_id)

    @raises_api_error
    def activate(self):
        """Activate this version of the model.
        Raises:
            ApiError: If there was an error communicating with the server.
        """
        if not self._model_version_id:
            raise ValueError('Only a BasetenDeployedModel backed by a model_version can be set as primary.')
        return api.activate_model_version(self._model_version_id)

    @raises_api_error
    def upload_sample_data(self,
                           feature_data,
                           target_data=None,
                           metadata: Optional[List[Dict]] = None,
                           data_name: str = 'validation_data',
                           ) -> Dict:
        """Upload a subset of the training/validation data to be used for
            - Summary statistics for the model
            - To detect model drift
            - To use as baseline data for model interpretability
            - To seed new data in the client.

        Training and validation data with targets must be uploaded with the targets separate.

        Args:
            feature_data (Union[np.ndarray, pd.DataFrame, List[List]]): The feature data to upload.
            target_data (Union[np.ndarray, pd.DataFrame, List[List]]): The target data to upload.
            metadata (List[Dict]): Metadata key/value pairs for the dataset.
            data_name (str): The name of the data set.

        Returns:
            Dict: The status of the upload.
        """
        if not self._model_version_id:
            raise ValueError('Please use on a BasetenDeployedModel instantiated with a model_version_id.')

        signed_s3_upload_post = api.signed_s3_upload_post(data_name)
        logger.debug(f'Signed s3 upload post:\n{json.dumps(signed_s3_upload_post, indent=4)}')

        with tempfile.TemporaryDirectory() as data_temp_directory:
            data_temp_file = build_h5_data_object(feature_data, target_data, metadata, data_temp_directory)
            files = {'file': (f'{data_name}.h5', open(data_temp_file, 'rb'))}
            form_fields = signed_s3_upload_post['form_fields']
            form_fields['AWSAccessKeyId'] = form_fields.pop('aws_access_key_id')
            s3_key = form_fields['key']
            requests.post(signed_s3_upload_post['url'], data=form_fields, files=files)
        return api.register_data_for_model(s3_key, self.model_version_id, data_name)

    @raises_api_error
    def artifacts(self):
        from baseten.baseten_artifact import BasetenArtifact
        if self._model_version_id:
            return [
                BasetenArtifact(**instance) for instance in api.model_version_linked_artifacts(self._model_version_id)
            ]
        return [BasetenArtifact(**instance) for instance in api.model_linked_artifacts(self._model_id)]

    def __repr__(self):
        attr_info = []
        if self._model_id:
            attr_info.append(f'model_id={self._model_id}')
        if self._model_version_id:
            attr_info.append(f'model_version_id={self._model_version_id}')
        if self._model_name:
            attr_info.append(f'name={self._model_name}')
        info_str = '\n  '.join(attr_info)
        return f'BasetenDeployedModel<\n  {info_str}\n>'

    @raises_api_error
    def log_metrics(self, metrics: dict) -> None:
        if not metrics:
            raise ValueError('metrics must be provided.')
        if not self._model_version_id and not self._model_id:
            raise ValueError('Please use on a BasetenDeployedModel instantiated with a model_version_id or model_id.')

        if self._model_id:
            api.create_model_metrics(metric_data=metrics, model_id=self._model_id)
        elif self._model_version_id:
            api.create_model_metrics(metric_data=metrics, model_version_id=self._model_version_id)
        logger.info('✅ Metrics logged successfully ✅')

    @raises_api_error
    def get_metrics(self) -> dict:
        if self._model_id:
            return api.model_metrics(self._model_id)
        elif self._model_version_id:
            return api.model_version_metrics(self._model_version_id)

        raise ValueError('Please use on a BasetenDeployedModel instantiated with a model_version_id or model_id.')

    @raises_api_error
    def log_config(self, config: dict) -> None:
        if not config:
            raise ValueError('config must be provided.')
        if not self._model_version_id and not self._model_id:
            raise ValueError('Please use on a BasetenDeployedModel instantiated with a model_version_id or model_id.')

        if self._model_id:
            api.create_model_configuration(configuration=config, model_id=self._model_id)
        elif self._model_version_id:
            api.create_model_configuration(configuration=config, model_version_id=self._model_version_id)
        logger.info('✅ Config logged successfully ✅')

    @raises_api_error
    def get_config(self) -> dict:
        if self._model_id:
            return api.model_configuration(self._model_id)
        elif self._model_version_id:
            return api.model_version_configuration(self._model_version_id)

        raise ValueError('Please use on a BasetenDeployedModel instantiated with a model_version_id or model_id.')

    @raises_api_error
    def get_truss_spec_version(self) -> dict:
        if self._model_id:
            return api.model_truss_spec_version(self._model_id)
        elif self._model_version_id:
            return api.model_version_truss_spec_version(self._model_version_id)
        elif self._external_model_version_id:
            return api.model_version_external_id_get_version(self._external_model_version_id)

        raise ValueError("Please use on a BasetenDeployedModel instantiated with a model_version_id or model_id.")

    @raises_api_error
    def add_artifact(
        self,
        name: str,
        list_of_files: List[str],
        description: Optional[str] = None,
    ):
        """Create an artifact in the BaseTen backend to track

            Args:
                name (str): The name of the artifact to be created.
                list_of_files (List[str]): A list of files to be uploaded.
                description (str, optional): An optional description of the artifact
                model_id (str, optional): A model_id to associate with the artifact
                model_version_id (str, optional): A model_version_id to associate with the artifact
            Returns:
                BasetenArtifact

            Raises:
                ApiError: If there was an error communicating with the server.
            """
        from baseten.baseten_artifact import create_artifact
        if self._model_version_id:
            artifact = create_artifact(
                name, list_of_files, description=description, model_version_id=self._model_version_id
            )
        else:
            artifact = create_artifact(
                name, list_of_files, description=description, model_id=self._model_id
            )
        return artifact

    @raises_api_error
    def pull(self, directory="."):
        response = requests.get(api.get_model_s3_download_url(self.model_version_id))
        with tarfile.open(name=None, fileobj=io.BytesIO(response.content)) as t:
            t.extractall(os.path.join(directory, self.model_version_id))
        return response

    @property
    def truss(self) -> Optional[TrussHandle]:
        return self.truss_handle


@raises_api_error
def models_summary():
    return api.models_summary()
