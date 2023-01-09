import platform
import time
from typing import BinaryIO, List, Optional
from urllib.parse import urlparse

from bravado.client import SwaggerClient
from bravado.requests_client import RequestsClient

from mlsteam_model_sdk.core.exceptions import (
    InvalidModelException,
    InvalidModelVersionException,
    InvalidProjectException,
)
from mlsteam_model_sdk.utils.config import get_value, OPTION_API_ENDPOINT
from mlsteam_model_sdk.utils.identity import Credential
from mlsteam_model_sdk.utils.typing import PathLike
from mlsteam_model_sdk.core.version import __version__


class ApiClient:
    DEFAULT_REQ_TIMEOUT = 90
    DOWNLOAD_REQ_TIMEOUT = 60 * 60

    def __init__(self, api_token=None):
        self.credential = Credential(api_token)
        self.api_address = self._get_api_endpoint()
        self.http_client = self.create_http_client()
        self.http_client.set_api_key(
            host=urlparse(self.api_address).netloc,
            api_key=f'Bearer {self.credential.api_token}',
            param_name='Authorization',
            param_in='header',
        )
        self.swagger_client = SwaggerClient.from_url(
            f'{self.api_address}/api/v2/swagger.json',
            config=dict(
                validate_swagger_spec=False,
                validate_requests=False,
                validate_response=False
            ),
            http_client=self.http_client,
        )

    def _get_api_endpoint(self) -> str:
        if False:
            api_endpoint = NotImplemented

        def _walrus_wrapper_api_endpoint_178ef4e1abf446ff9467928aa7d4d837(expr):
            """Wrapper function for assignment expression."""
            nonlocal api_endpoint
            api_endpoint = expr
            return api_endpoint

        if (_walrus_wrapper_api_endpoint_178ef4e1abf446ff9467928aa7d4d837(get_value(OPTION_API_ENDPOINT))):
            return api_endpoint
        return self.credential.api_address

    @classmethod
    def create_http_client(cls):
        http_client = RequestsClient()
        user_agent = (
            'mlsteam-model-sdk-client/{lib_version} ({system}, python {python_version})'.format(
                lib_version=__version__,
                system=platform.platform(),
                python_version=platform.python_version(),
            )
        )
        http_client.session.headers.update({'User-Agent': user_agent})
        return http_client

    def poll(self, job_id: str, interval: float, max_attempts: Optional[int] = None):
        STOPPED_STATES = ('finished', 'stopped', 'canceled', 'failed')
        attempts = 0
        while True:
            attempts += 1
            result = self.get_async_job(job_id)
            if result['state'] in STOPPED_STATES:
                return result
            if max_attempts is not None and attempts >= max_attempts:
                raise TimeoutError(f'Max attempts exceeded (job_id={job_id})')
            time.sleep(interval)

    def get_async_job(self, job_id):
        rsp = self.swagger_client.async_jobs.getAsyncJob(
            job_id=job_id
        ).response(timeout=self.DEFAULT_REQ_TIMEOUT)
        return rsp.result

    def get_project(self, project_name) -> dict:
        rsp = self.swagger_client.project.listProject(
            name=project_name
        ).response(timeout=self.DEFAULT_REQ_TIMEOUT)
        if rsp.result:
            project = rsp.result[0]
            if project:
                return project
        raise InvalidProjectException(project_name=project_name)

    def list_models(self, puuid) -> List[dict]:
        rsp = self.swagger_client.model.listModel(
            puuid=puuid
        ).response(timeout=self.DEFAULT_REQ_TIMEOUT)
        return rsp.result

    def get_model(self, puuid, muuid=None, model_name=None) -> dict:
        if muuid:
            rsp = self.swagger_client.model.getModel(
                puuid=puuid,
                muuid=muuid
            ).response(timeout=self.DEFAULT_REQ_TIMEOUT)
            return rsp.result
        elif model_name:
            models = self.list_models(puuid)
            for m in models:
                if m['name'] == model_name:
                    return self.get_model(puuid, muuid=m['uuid'])
            raise InvalidModelException(model_name=model_name)
        raise ValueError('Neither muuid nor model_name is given')

    def list_model_versions(self, puuid, muuid) -> List[dict]:
        rsp = self.swagger_client.model.listVersionModel(
            puuid=puuid,
            muuid=muuid
        ).response(timeout=self.DEFAULT_REQ_TIMEOUT)
        return rsp.result

    def get_model_version(self, puuid, muuid, vuuid=None, version_name=None) -> dict:
        if vuuid:
            rsp = self.swagger_client.model.getVersionModel(
                puuid=puuid,
                muuid=muuid,
                vuuid=vuuid
            ).response(timeout=self.DEFAULT_REQ_TIMEOUT)
            return rsp.result
        elif version_name:
            versions = self.list_model_versions(puuid, muuid)
            for v in versions:
                if v['version'] == version_name:
                    return self.get_model_version(puuid, muuid, vuuid=v['uuid'])
            raise InvalidModelVersionException(version_name=version_name)
        raise ValueError('Neither vuuid nor version_name is given')

    def prepare_download_model_version(self, puuid, muuid, vuuid, req: Optional[bytes] = None) -> dict:
        rsp = self.swagger_client.model.prepareDownloadVersionModel(
            puuid=puuid,
            muuid=muuid,
            vuuid=vuuid,
            req=req
        ).response(timeout=self.DEFAULT_REQ_TIMEOUT)
        return rsp.result

    def download_model_version(self, puuid, muuid, vuuid, download_id,
                               download_fp: Optional[BinaryIO] = None,
                               download_path: Optional[PathLike] = None):
        """Download model version

        download_fp takes precendence over download_path
        download_fp should be positioned in advance
        the parent directories of download_path should exist in advance
        """
        if not download_fp and not download_path:
            raise ValueError('Neither download_fp nor download_path is given')

        rsp = self.swagger_client.model.downloadVersionModel(
            puuid=puuid, muuid=muuid, vuuid=vuuid, download_id=download_id
        ).response(timeout=self.DOWNLOAD_REQ_TIMEOUT)
        if download_fp:
            download_fp.write(rsp.result)
        else:
            with open(download_path, 'wb') as fp:
                fp.write(rsp.result)
