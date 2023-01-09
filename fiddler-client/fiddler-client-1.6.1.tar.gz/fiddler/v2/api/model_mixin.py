import os
import shutil
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional

from pydantic import parse_obj_as

from fiddler import ModelInfo
from fiddler.libs.http_client import RequestClient
from fiddler.utils import logging
from fiddler.v2.api.model_artifact_deploy import (
    ModelArtifactDeployer,
    MultiPartModelArtifactDeployer,
)
from fiddler.v2.constants import MULTI_PART_CHUNK_SIZE
from fiddler.v2.schema.model import Model
from fiddler.v2.schema.model_deployment import ArtifactType, DeploymentParams
from fiddler.v2.utils.exceptions import handle_api_error_response
from fiddler.v2.utils.helpers import get_model_artifact_info, read_model_yaml
from fiddler.v2.utils.response_handler import (
    APIResponseHandler,
    PaginatedResponseHandler,
)
from fiddler.v2.utils.validations import validate_artifact_dir

logger = logging.getLogger(__name__)


class ModelMixin:
    ADD_SURROGATE_MODEL_API_VERSION = '>=22.12.0'
    ADD_MODEL_ARTIFACT_API_VERSION = '>=22.12.0'
    DELETE_MODEL_API_VERSION = '>=22.12.0'

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
        info: ModelInfo,
    ) -> Model:
        """
        Function to add a model to fiddler for monitoring

        :param project_name: project name where the model will be added
        :type project_name: string
        :param model_name: name of the model
        :type model_name: string
        :param info: model related information
        :type info: ModelInfo

        :return: Model object which contains the model details
        """
        request_body = {
            'name': model_name,
            'project_name': project_name,
            'organization_name': self.organization_name,
            'info': info.to_dict(),
            'model_type': None,
            'file_list': None,
        }

        response = self.client.post(
            url='models',
            data=request_body,
        )
        logger.info('Model %s added to %s project', model_name, project_name)

        return Model.deserialize(APIResponseHandler(response))

    @handle_api_error_response
    def update_model(
        self,
        model_name: str,
        project_name: str,
        info: Optional[ModelInfo] = None,
        file_list: Optional[List[Dict[str, Any]]] = None,
        framework: Optional[str] = None,
        requirements: Optional[str] = None,
    ) -> Model:
        """
        Update model metadata like model info, file

        :param project_name: project name where the model will be added
        :type project_name: string
        :param model_name: name of the model
        :type model_name: string
        :param info: model related information passed as dictionary from user
        :type info: ModelInfo object
        :param file_list: Artifact file list
        :type info: List of dictionaries
        :param framework: Model framework name
        :type framework: string
        :param requirements: Requirements
        :type requirements: string
        :return: Model object which contains the model details
        """
        body = {}

        if info:
            body['info'] = info.to_dict()

        if file_list:
            body['file_list'] = file_list

        if framework:
            body['framework'] = framework

        if requirements:
            body['requirements'] = requirements

        response = self.client.patch(
            url=f'models/{self.organization_name}:{project_name}:{model_name}',
            data=body,
        )
        logger.info('Model[%s/%s] - Updated model', project_name, model_name)

        return Model.deserialize(APIResponseHandler(response))

    @handle_api_error_response
    def delete_model(self, model_name: str, project_name: str) -> None:
        """
        Delete a model

        :params model_name: Model name to be deleted
        :params project_name: Project name to which the model belongs to.

        :returns: None
        """
        logger.info('Deleting model %s from %s project', model_name, project_name)
        self.client.delete(
            url=f'models/{self.organization_name}:{project_name}:{model_name}',
        )
        logger.info('Deleted model %s from %s project', model_name, project_name)

    @handle_api_error_response
    def add_model_surrogate(
        self, model_name: str, project_name: str, wait: bool = True
    ) -> str:
        """
        Add surrogate model to an existing model
        :param model_name: Model name
        :param project_name: Project name
        :param wait: Whether to wait for job to complete or return after submitting
            the job
        :return: Async job uuid
        """
        payload = {
            'model_name': model_name,
            'project_name': project_name,
            'organization_name': self.organization_name,
        }

        model_id = f'{self.organization_name}:{project_name}:{model_name}'
        url = f'models/{model_id}/deploy-surrogate'
        response = self.client.post(url=url, data=payload)

        data = APIResponseHandler(response).get_data()
        job_uuid = data['job_uuid']

        logger.info(
            'Model[%s/%s] - Submitted job (%s) for deploying a surrogate model',
            project_name,
            model_name,
            job_uuid,
        )

        if wait:
            job_name = f'Model[{project_name}/{model_name}] - Deploy a surrogate model'
            self.wait_for_job(uuid=job_uuid, job_name=job_name)  # noqa

        return job_uuid

    def _deploy_model_artifact(
        self,
        project_name: str,
        model_name: str,
        artifact_dir: str,
        deployment_params: Optional[DeploymentParams] = None,
        wait: bool = True,
        update: bool = False,
    ) -> str:
        """
        Upload and deploy model artifact for an existing model
        :param model_name: Model name
        :param project_name: Project name
        :param artifact_dir: Model artifact directory
        :param deployment_params: Model deployment parameters
        :param wait: Whether to wait for async job to finish or return
        :param update: Set True for updating artifact, False for adding artifact
        :return: Async job uuid
        """
        artifact_dir = Path(artifact_dir)
        validate_artifact_dir(artifact_dir)

        if (
            deployment_params
            and deployment_params.artifact_type == ArtifactType.SURROGATE
        ):
            raise ValueError(
                f'{ArtifactType.SURROGATE} artifact_type is an invalid value for this '
                f'method. Use {ArtifactType.PYTHON_PACKAGE} instead.'
            )

        self._update_model_on_artifact_upload(
            model_name=model_name, project_name=project_name, artifact_dir=artifact_dir
        )

        with tempfile.TemporaryDirectory() as tmp:
            # Archive model artifact directory
            logger.info(
                'Model[%s/%s] - Tarring model artifact directory - %s',
                project_name,
                model_name,
                artifact_dir,
            )
            file_path = shutil.make_archive(
                base_name=str(Path(tmp) / 'files'),
                format='tar',
                root_dir=str(artifact_dir),
                base_dir='.',
            )

            logger.info(
                'Model[%s/%s] - Model artifact tar file created at %s',
                project_name,
                model_name,
                file_path,
            )

            # Choose deployer based on archive file size
            if os.path.getsize(file_path) < MULTI_PART_CHUNK_SIZE:
                deployer_class = ModelArtifactDeployer
            else:
                deployer_class = MultiPartModelArtifactDeployer

            deployer = deployer_class(
                client=self.client,
                model_name=model_name,
                project_name=project_name,
                organization_name=self.organization_name,
                update=update,
            )

            job_uuid = deployer.deploy(
                file_path=Path(file_path), deployment_params=deployment_params
            )

        logger.info(
            'Model[%s/%s] - Submitted job (%s) for deploying model artifact',
            project_name,
            model_name,
            job_uuid,
        )

        if wait:
            job_name = f'Model[{project_name}/{model_name}] - Deploy model artifact'
            self.wait_for_job(uuid=job_uuid, job_name=job_name)  # noqa

        return job_uuid

    @handle_api_error_response
    def add_model_artifact(
        self,
        model_name: str,
        project_name: str,
        artifact_dir: str,
        deployment_params: Optional[DeploymentParams] = None,
        wait: bool = True,
    ) -> str:
        """
        Add model artifact to an existing model
        :param model_name: Model name
        :param project_name: Project name
        :param artifact_dir: Model artifact directory
        :param deployment_params: Model deployment parameters
        :param wait: Whether to wait for async job to finish or return
        :return: Async job uuid
        """
        return self._deploy_model_artifact(
            project_name=project_name,
            model_name=model_name,
            artifact_dir=artifact_dir,
            deployment_params=deployment_params,
            wait=wait,
            update=False,
        )

    @handle_api_error_response
    def update_model_artifact(
        self,
        model_name: str,
        project_name: str,
        artifact_dir: str,
        deployment_params: Optional[DeploymentParams] = None,
        wait: bool = True,
    ) -> str:
        """
        Update model artifact of an existing model
        :param model_name: Model name
        :param project_name: Project name
        :param artifact_dir: Model artifact directory
        :param deployment_params: Model deployment parameters
        :param wait: Whether to wait for async job to finish or return
        :return: Async job uuid
        """
        return self._deploy_model_artifact(
            project_name=project_name,
            model_name=model_name,
            artifact_dir=artifact_dir,
            deployment_params=deployment_params,
            wait=wait,
            update=True,
        )

    def _update_model_on_artifact_upload(
        self, model_name: str, project_name: str, artifact_dir: Path
    ) -> None:
        """Update model metadata based on artifact dir contents"""
        file_list = get_model_artifact_info(artifact_dir=artifact_dir)
        model_info = read_model_yaml(artifact_dir=artifact_dir)

        self.update_model(
            model_name=model_name,
            project_name=project_name,
            info=model_info,
            file_list=file_list,
        )
