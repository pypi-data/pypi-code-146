from typing import Optional

from fiddler.libs.http_client import RequestClient
from fiddler.utils import logging
from fiddler.v2.schema.model_deployment import ModelDeployment
from fiddler.v2.utils.exceptions import handle_api_error_response

logger = logging.getLogger(__name__)


class ModelDeploymentMixin:
    """Model deployment api handler"""

    client: RequestClient
    organization_name: str

    @handle_api_error_response
    def get_model_deployment(
        self,
        model_name: str,
        project_name: str,
    ) -> ModelDeployment:
        """
        Get model deployment object
        :param model_name: Model name
        :param project_name: Project name
        :return: Model deployment object
        """
        model_id = f'{self.organization_name}:{project_name}:{model_name}'
        response = self.client.get(url=f'model-deployments/{model_id}')

        return ModelDeployment(**response.json().get('data'))

    @handle_api_error_response
    def update_model_deployment(
        self,
        model_name: str,
        project_name: str,
        active: Optional[bool] = None,
        replicas: Optional[int] = None,
        cpu: Optional[int] = None,
        memory: Optional[int] = None,
        wait: bool = True,
    ) -> ModelDeployment:
        """
        Update model deployment fields like replicas, cpu, memory
        :param model_name: Model name
        :param project_name: Project name
        :param active: Set False to scale down model deployment and True to scale up
        :param replicas: Number of model deployment replicas to run
        :param cpu: Amount of milli cpus to allocate for each replica
        :param memory: Amount of mebibytes memory to allocate for each replica
        :param wait: Whether to wait for async job to finish or return
        :return: Model deployment object
        """
        body = {}

        if active is not None:
            body['active'] = active

        if replicas is not None:
            body['replicas'] = replicas

        if cpu is not None:
            body['cpu'] = cpu

        if memory is not None:
            body['memory'] = memory

        if not body:
            raise ValueError('Pass at least one parameter to update model deployment')

        model_id = f'{self.organization_name}:{project_name}:{model_name}'
        response = self.client.patch(
            url=f'model-deployments/{model_id}',
            data=body,
        )

        model_deployment = ModelDeployment(**response.json().get('data'))

        logger.info(
            'Model[%s/%s] - Submitted job (%s) for updating model deployment',
            project_name,
            model_name,
            model_deployment.job_uuid,
        )

        if wait:
            job_name = f'Model[{project_name}/{model_name}] - Update model deployment'
            self.wait_for_job(uuid=model_deployment.job_uuid, job_name=job_name)  # noqa

        return model_deployment
