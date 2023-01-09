import json
import math
import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Callable, Dict, List, Optional

from fiddler.libs.http_client import RequestClient
from fiddler.utils import logging
from fiddler.v2.constants import CONTENT_TYPE_OCTET_STREAM_HEADER, MULTI_PART_CHUNK_SIZE
from fiddler.v2.schema.model_deployment import DeploymentParams
from fiddler.v2.utils.response_handler import APIResponseHandler

logger = logging.getLogger(__name__)


class _AbstractModelDeployer(ABC):
    """Abstract class for deploying model artifact"""

    def __init__(
        self,
        client: RequestClient,
        model_name: str,
        project_name: str,
        organization_name: str,
        update: bool = False,
    ) -> None:
        """
        Abstract class for deploying model artifact
        :param client: HTTP client
        :param model_name: Model name
        :param project_name: Project name
        :param organization_name: Organization name
        :param update: Set True for updating artifact, False for adding artifact
        """
        self.client = client
        self.model_name = model_name
        self.project_name = project_name
        self.organization_name = organization_name
        self.update = update

        self._model_id = (
            f'{self.organization_name}:{self.project_name}:{self.model_name}'
        )
        self._base_url = f'models/{self._model_id}/deploy-artifacts'

    @abstractmethod
    def deploy(
        self, file_path: Path, deployment_params: Optional[DeploymentParams] = None
    ) -> str:
        pass

    def _get_method(self) -> Callable:
        """Get HTTP method"""
        return self.client.put if self.update else self.client.post


class MultiPartModelArtifactDeployer(_AbstractModelDeployer):
    """Upload model artifact with multi-part upload and deploy"""

    def __init__(
        self,
        client: RequestClient,
        model_name: str,
        project_name: str,
        organization_name: str,
        update: bool = False,
    ):
        super().__init__(client, model_name, project_name, organization_name, update)

        self._init_url = f'{self._base_url}/multi-part-init'
        self._upload_url = f'{self._base_url}/multi-part-upload'
        self._complete_url = f'{self._base_url}/deploy-artifacts/multi-part-complete'

    def _initialize_multi_part_upload(self) -> str:
        """
        Initialize multi-part upload request
        :return: Multi-part upload id
        """
        logger.info(
            'Model[%s/%s] - Initializing multi-part model upload',
            self.project_name,
            self.model_name,
        )

        method = self._get_method()

        response = method(url=self._init_url)

        response_data = APIResponseHandler(response).get_data()

        logger.info(
            'Model[%s/%s] - Multi-part model upload initialized',
            self.project_name,
            self.model_name,
        )
        return response_data.get('upload_id')

    def _upload_multi_part_chunk(
        self, data: bytes, upload_id: str, part_number: int
    ) -> Dict:
        """
        Upload data chunk
        :param data: Data chunk
        :param upload_id: Multi-part upload id
        :param part_number: Chunk part number
        :return: Part details
        """
        method = self._get_method()

        response = method(
            url=self._upload_url,
            params={
                'upload_id': upload_id,
                'part_number': part_number,
            },
            data=data,
            headers=CONTENT_TYPE_OCTET_STREAM_HEADER,
        )
        response_data = APIResponseHandler(response).get_data()

        return {
            'etag': response_data.get('etag'),
            'part_number': response_data.get('part_number'),
        }

    def _complete_multi_part_upload(
        self,
        upload_id: str,
        parts: List[Dict],
        deployment_params: Optional[DeploymentParams] = None,
    ) -> str:
        """
        Complete multi-part upload request and deploy model artifact
        :param upload_id: Multi-part upload id
        :param parts: List of all parts
        :param deployment_params: Deployment parameters
        :return: Async job uuid
        """
        method = self._get_method()
        payload = {
            'upload_id': upload_id,
            'parts': parts,
        }

        if deployment_params:
            payload['deployment_params'] = deployment_params.dict(exclude_unset=True)

        response = method(
            url=self._complete_url,
            data=payload,
        )

        logger.info(
            'Model[%s/%s] - Multi-part model upload completed',
            self.project_name,
            self.model_name,
        )
        data = APIResponseHandler(response).get_data()
        return data['job_uuid']

    def deploy(
        self, file_path: Path, deployment_params: Optional[DeploymentParams] = None
    ) -> str:
        """
        Upload and deploy model artifact
        :param file_path: Path to model artifact tar file
        :param deployment_params: Model deployment parameters
        :return: Async job uuid
        """
        # 1. Initialize multi-part upload request
        upload_id = self._initialize_multi_part_upload()
        part_number = 1
        parts = []
        file_size = os.path.getsize(file_path)
        total_chunks = math.ceil(file_size / MULTI_PART_CHUNK_SIZE)

        # 2. Chunk and upload
        with open(file_path, 'rb') as f:
            while True:
                data = f.read(MULTI_PART_CHUNK_SIZE)
                if not data:
                    break

                logger.info(
                    'Model[%s/%s] - Uploading multi-part chunk - %d/%d',
                    self.project_name,
                    self.model_name,
                    part_number,
                    total_chunks,
                )

                part = self._upload_multi_part_chunk(
                    data=data,
                    upload_id=upload_id,
                    part_number=part_number,
                )
                parts.append(part)
                logger.info(
                    'Model[%s/%s] - Uploaded multi-part chunk - %d/%d',
                    self.project_name,
                    self.model_name,
                    part_number,
                    total_chunks,
                )
                part_number += 1

        # 3: Complete the upload
        return self._complete_multi_part_upload(
            upload_id=upload_id, parts=parts, deployment_params=deployment_params
        )


class ModelArtifactDeployer(_AbstractModelDeployer):
    """Upload and deploy model artifact in a single request"""

    def __init__(
        self,
        client: RequestClient,
        model_name: str,
        project_name: str,
        organization_name: str,
        update: bool = False,
    ):
        super().__init__(client, model_name, project_name, organization_name, update)

        self._upload_url = self._base_url

    def deploy(
        self, file_path: Path, deployment_params: Optional[DeploymentParams] = None
    ) -> str:
        """
        Upload and deploy model artifact
        :param file_path: Path to model artifact tar file
        :param deployment_params: Model deployment parameters
        :return: Async job uuid
        """
        logger.info(
            'Model[%s/%s] - Uploading model artifact',
            self.project_name,
            self.model_name,
        )

        method = self._get_method()
        params = {}
        if deployment_params:
            params['deployment_params'] = json.dumps(
                deployment_params.dict(exclude_unset=True)
            )

        with open(file_path, 'rb') as f:
            data = f.read()
            response = method(
                url=self._upload_url,
                params=params,
                data=data,
                headers=CONTENT_TYPE_OCTET_STREAM_HEADER,
            )

        logger.info(
            'Model[%s/%s] - Uploaded model artifact',
            self.project_name,
            self.model_name,
        )

        data = APIResponseHandler(response).get_data()
        return data['job_uuid']
