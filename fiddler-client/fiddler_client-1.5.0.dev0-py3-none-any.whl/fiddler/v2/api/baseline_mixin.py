from http import HTTPStatus
from typing import List

from pydantic import parse_obj_as

from fiddler.core_objects import BaselineType, WindowSize
from fiddler.libs.http_client import RequestClient
from fiddler.utils import logging
from fiddler.v2.schema.baseline import Baseline
from fiddler.v2.utils.exceptions import handle_api_error_response
from fiddler.v2.utils.response_handler import (
    APIResponseHandler,
    PaginatedResponseHandler,
)

logger = logging.getLogger(__name__)


class BaselineMixin:
    client: RequestClient
    organization_name: str

    @handle_api_error_response
    def get_baselines(self, project_id: str, model_id: str = None) -> List[Baseline]:
        """Get list of all Baselines at project or model level

        :params project_id: project to list baselines from
        :params model_id: [Optional] model within project to list baselines from
        :returns: List containing Baseline objects
        """
        response = self.client.get(
            url='baselines/',
            params={
                'organization_name': self.organization_name,
                'project_name': project_id,
                'model_name': model_id,
            },
        )
        _, items = PaginatedResponseHandler(response).get_pagination_details_and_items()
        return parse_obj_as(List[Baseline], items)

    @handle_api_error_response
    def get_baseline(self, project_id: str, baseline_id: str) -> Baseline:
        """Get the details of a Baseline.

        :params project_id: The project to which the Baseline belongs to
        :params baseline_id: The Baseline name of which you need the details

        :returns: Baseline object which contains the details
        """
        response = self.client.get(
            url=f'baselines/{self.organization_name}:{project_id}:{baseline_id}',
        )
        response_handler = APIResponseHandler(response)
        return Baseline.deserialize(response_handler)

    @handle_api_error_response
    def add_baseline(
        self,
        project_id: str,
        name: str,
        type: BaselineType,
        dataset_id: str = None,
        source_model_id: str = None,
        start_time: int = None,
        end_time: int = None,
        offset: int = None,
        window_size: WindowSize = None,
        model_id: str = None,
    ) -> Baseline:
        """Function to add a Baseline to fiddler for monitoring

        :param project_id: project name where the Baseline will be added
        :type project_id: string
        :param name: name of the Baseline
        :type name: string
        :param type: type of the Baseline
        :type type: BaselineType
        :param dataset_id: (optional) dataset to be used as baseline
        :type dataset_id: string
        :param source_model_id: (optional) model to be used as baseline
        :type source_model_id: string
        :param start_time: (optional) seconds since epoch to be used as start time for STATIC baseline
        :type start_time: int
        :param end_time: (optional) seconds since epoch to be used as end time for STATIC baseline
        :type end_time: int
        :param offset: (optional) seconds from current time to be used for RELATIVE baseline
        :type offset: int
        :param window_size: (optional) width of window in seconds to be used for RELATIVE baseline
        :type window_size: int
        :param model_id: (optional) model to associate baseline to
        :type model_id: string

        :return: Baseline object which contains the Baseline details
        """
        if start_time:
            start_time = start_time * 1000  # convert to milliseconds

        if end_time:
            end_time = end_time * 1000  # convert to milliseconds

        if window_size:
            window_size = int(window_size)  # ensure enum is converted to int

        request_body = Baseline(
            organization_name=self.organization_name,
            project_id=project_id,
            name=name,
            type=str(type),
            model_association=model_id,
            dataset_id=dataset_id,
            model_name=source_model_id,
            start_time=start_time,
            end_time=end_time,
            offset=offset,
            window_size=window_size,
        ).dict()

        if 'id' in request_body:
            request_body.pop('id')

        response = self.client.post(
            url='baselines/',
            data=request_body,
        )

        if response.status_code == HTTPStatus.OK:
            logger.info(f'{name} setup successful')
            return Baseline.deserialize(APIResponseHandler(response))

    @handle_api_error_response
    def delete_baseline(self, project_id: str, baseline_id: str) -> None:
        """Delete a Baseline

        :params project_id: Project name to which the Baseline belongs to.
        :params baseline_id: Baseline name to be deleted

        :returns: None
        """
        response = self.client.delete(
            url=f'baselines/{self.organization_name}:{project_id}:{baseline_id}',
        )
        if response.status_code == HTTPStatus.OK:
            logger.info(f'{baseline_id} delete request received.')
        else:
            # @TODO: Handle non 200 status response
            logger.info('Delete unsuccessful')

    @handle_api_error_response
    def attach_baseline(
        self,
        project_id: str,
        baseline_id: str,
        model_id: str,
    ) -> None:
        """Function to add a Baseline to fiddler for monitoring

        :param project_id: project name where the Baseline will be added
        :type project_id: string
        :param baseline_id: name of the Baseline
        :type baseline_id: string
        :param model_id: (optional) model to associate baseline to
        :type model_id: string
        """

        response = self.client.post(
            url=f'baselines/{self.organization_name}:{project_id}:{baseline_id}:{model_id}',
            data={},
        )

        if APIResponseHandler(response).get_status_code() != HTTPStatus.OK:
            logger.info(f'Baseline {baseline_id} attachment to model {model_id} failed')
        else:
            logger.info(
                f'Baseline {baseline_id} successfully attached to model {model_id}'
            )

    @handle_api_error_response
    def detach_baseline(
        self,
        project_id: str,
        baseline_id: str,
        model_id: str,
    ) -> None:
        """Function to remove baseline from model

        :param project_id: project name where the Baseline will be added
        :type project_id: string
        :param baseline_id: name of the Baseline
        :type baseline_id: string
        :param model_id: (optional) model to associate baseline to
        :type model_id: string
        """

        response = self.client.delete(
            url=f'baselines/{self.organization_name}:{project_id}:{baseline_id}:{model_id}',
            data={},
        )

        if APIResponseHandler(response).get_status_code() != HTTPStatus.OK:
            logger.info(
                f'Baseline {baseline_id} detachment from model {model_id} failed'
            )
        else:
            logger.info(
                f'Baseline {baseline_id} successfully detached from model {model_id}'
            )
