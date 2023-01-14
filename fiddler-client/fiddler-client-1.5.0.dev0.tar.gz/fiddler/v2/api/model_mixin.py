from http import HTTPStatus
from typing import List, Optional
import os
from deepdiff import DeepDiff

from pydantic import parse_obj_as

from fiddler.libs.http_client import RequestClient
from fiddler.utils import logging
from fiddler.v2.schema.model import Model
from fiddler.v2.utils.exceptions import handle_api_error_response
from fiddler.v2.utils.response_handler import (
    APIResponseHandler,
    PaginatedResponseHandler,
)
from fiddler.v2.api.helpers import multipart_upload_model
from fiddler.core_objects import ModelInfo, ArtifactStatus
from fiddler.utils.general_checks import type_enforce
import yaml
from fiddler.model_info_validator import ModelInfoValidator
from pathlib import Path

logger = logging.getLogger(__name__)


class ModelMixin:
    client: RequestClient
    organization_name: str

    @handle_api_error_response
    def get_models(self, project_name: str) -> List[Model]:
        """
        Get list of all models belonging to a project

        :params project_name: The project for which you want to get the models
        :returns: List containing Model objects
        """
        response = self.client.get(
            url='models',
            params={
                'organization_name': self.organization_name,
                'project_name': project_name,
            },
        )
        _, items = PaginatedResponseHandler(response).get_pagination_details_and_items()
        return parse_obj_as(List[Model], items)

    @handle_api_error_response
    def get_model(self, project_name: str, model_name: str) -> Model:
        """
        Get the details of a model.

        :params project_name: The project to which the model belongs to
        :params model_name: The model name of which you need the details
        :returns: Model object which contains the details
        """
        response = self.client.get(
            url=f'models/{self.organization_name}:{project_name}:{model_name}',
        )
        response_handler = APIResponseHandler(response)
        return Model.deserialize(response_handler)

    @handle_api_error_response
    def add_model(
        self,
        project_name: str,
        model_name: str,
        info: Optional[dict] = None,
        model_type: Optional[str] = None,
        framework: Optional[str] = None,
        requirements: Optional[str] = None,
    ) -> Model:
        """
        Function to add a model to fiddler for monitoring

        :param project_name: project name where the model will be added
        :type project_name: string
        :param model_name: name of the model
        :type model_name: string
        :param info: model related information passed as dictionary from user
        :type info: dictionary
        :param model_type: the type of model e.g. REGRESSION, BINARY CLASSIFICATION
        :type model_type: string
        :return: Model object which contains the model details
        """
        # @TODO: file_list required while setting up model?
        # @TODO: Handle model_deployment_id?
        request_body = Model(
            organization_name=self.organization_name,
            project_name=project_name,
            name=model_name,
            info=info,
            model_type=model_type,
            framework=framework,
            requirements=requirements,
        ).dict()

        # remove id key from POST request, as it will be created by the backend
        if 'id' in request_body:
            request_body.pop('id')

        response = self.client.post(
            url='models',
            data=request_body,
        )
        logger.info(f'{model_name} setup successful')

        return Model.deserialize(APIResponseHandler(response))

    @handle_api_error_response
    def delete_model(self, project_name: str, model_name: str) -> None:
        """
        Delete a model

        :params project_name: Project name to which the model belongs to.
        :params model_name: Model name to be deleted

        :returns: None
        """
        response = self.client.delete(
            url=f'models/{self.organization_name}:{project_name}:{model_name}',
        )
        if response.status_code == HTTPStatus.OK:
            logger.info(f'{model_name} delete request received.')
        else:
            # @TODO: Handle non 200 status response
            logger.info('Delete unsuccessful')

    @handle_api_error_response
    def upload_model_package(
        self,
        project_name: str,
        model_name: str,
        artifact_path: Path,
    ) -> Model:
        artifact_path = type_enforce('artifact_path', artifact_path, Path)

        if not artifact_path.is_dir():
            raise ValueError(f'Not a valid model dir: {artifact_path}')

        yaml_file = artifact_path / 'model.yaml'
        if not yaml_file.is_file():
            raise ValueError(f'Model yaml not found {yaml_file}')

        with yaml_file.open() as f:
            model_info = ModelInfo.from_dict(yaml.safe_load(f))

        miv = ModelInfoValidator(model_info, None)
        miv.validate_categoricals(modify=True)

        response = multipart_upload_model(self.client, self.organization_name, project_name, model_name, artifact_path)

        if response.get('status') == 'SUCCESS':
            file_list = []
            for _, _, files in os.walk(artifact_path):
                for name in files:
                    abs_path = artifact_path / name
                    file_info = {'name': abs_path.name, 'size': abs_path.stat().st_size, 'modified': abs_path.stat().st_mtime}
                    file_list.append(file_info)

            # 2. Create postgres and CH entry
            request_body = Model(
            organization_name=self.organization_name,
            project_name=project_name,
            name=model_name,
            info=model_info.to_dict(),
            file_list={'files':file_list},
            framework='',
            model_type='',
            requirements='',
            ).dict()

            if 'id' in request_body:
                request_body.pop('id')

            response = self.client.post(
                url='models',
                data=request_body,
                params={'blob_uploaded': True}
            )
            logger.info(f'{model_name} setup successful')

            return Model.deserialize(APIResponseHandler(response))


    @handle_api_error_response
    def add_model_surrogate(
        self,
        project_name: str,
        dataset_name: str,
        model_name: str,
        info: dict,
    ) -> Model:
        model_info = ModelInfo.from_dict(info)
        if model_info.artifact_status is None:
            model_info.artifact_status = ArtifactStatus.SURROGATE
        if model_info.artifact_status != ArtifactStatus.SURROGATE:
            raise ValueError(f'Please set model_info.artifact_status to {ArtifactStatus.SURROGATE}')
    
        request_body = Model(
            organization_name=self.organization_name,
            project_name=project_name,
            name=model_name,
            info=model_info.to_dict(),
        ).dict(include={'organization_name', 'project_name', 'info', 'name'})

        request_body.update({'dataset_name': dataset_name})

        response = self.client.post(
           url='model-surrogate',
           data=request_body
        )

        logger.info(f'{model_name} surrogate created successfully!')

        return Model.deserialize(APIResponseHandler(response))

    @handle_api_error_response
    def update_model(
        self,
        project_name: str,
        model_name: str,
        artifact_path: Path,
    ) -> Model:
        artifact_path = type_enforce('artifact_path', artifact_path, Path)

        if not artifact_path.is_dir():
            raise ValueError(f'Not a valid model dir: {artifact_path}')

        yaml_file = artifact_path / 'model.yaml'
        if not yaml_file.is_file():
            raise ValueError(f'Model yaml not found {yaml_file}')

        with yaml_file.open() as f:
            model_info = ModelInfo.from_dict(yaml.safe_load(f))

        if len(model_info.datasets) < 1:
            raise ValueError('Unable to find dataset in model.yaml')

        if len(model_info.datasets) > 1:
            raise ValueError('More than one dataset specified in model.yaml')

        remote_model_info = ModelInfo.from_dict(self.get_model(project_name, model_name).info)

        # Model info should remain exactly the same, expect the following fields can be changed:
        # custom_explanation_names, preferred_explanation_method, display_name, description, framework, algorithm
        # and model_deployment_params
        ddiff = DeepDiff(remote_model_info, model_info, ignore_order=True,
                         exclude_paths=['root.preferred_explanation_method', 'root.custom_explanation_names',
                                        'root.display_name', 'root.description', 'root.framework', 'root.algorithm',
                                        'root.model_deployment_params',  'root.artifact_status'])

        if len(ddiff) > 0:
            raise ValueError(
                f'remote model info, does not match '
                f'local model info: {ddiff}. Updating those fields in model info is '
                f'not currently supported'
            )

        response = multipart_upload_model(self.client, self.organization_name, project_name, model_name, artifact_path, is_update=True)
        if response.get('status') == 'SUCCESS':
            file_list = []
            for _, _, files in os.walk(artifact_path):
                for name in files:
                    abs_path = artifact_path / name
                    file_info = {'name': abs_path.name, 'size': abs_path.stat().st_size, 'modified': abs_path.stat().st_mtime}
                    file_list.append(file_info)

            # 2. Create postgres and CH entry
            request_body = Model(
            organization_name=self.organization_name,
            project_name=project_name,
            name=model_name,
            info=model_info.to_dict(),
            file_list={'files':file_list}
            ).dict(include={'name', 'project_name', 'organization_name', 'info', 'file_list'})

            if 'id' in request_body:
                request_body.pop('id')

            response = self.client.patch(
                url=f'models/{self.organization_name}:{project_name}:{model_name}',
                data=request_body,
            )
            logger.info(f'{model_name} updated successful')

            return Model.deserialize(APIResponseHandler(response))
