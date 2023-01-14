from typing import Optional
from urllib.parse import urljoin

from fiddler._version import __version__
from fiddler.libs.http_client import RequestClient
from fiddler.utils import logging
from fiddler.v2.api.alert_mixin import AlertMixin
from fiddler.v2.api.baseline_mixin import BaselineMixin

# @todo: This is v1 implementation needs to have a proper v2 approach
from fiddler.v2.api.dataset_mixin import DatasetMixin
from fiddler.v2.api.events_mixin import EventsMixin
from fiddler.v2.api.job_mixin import JobMixin
from fiddler.v2.api.model_mixin import ModelMixin
from fiddler.v2.api.project_mixin import ProjectMixin
from fiddler.v2.constants import FIDDLER_CLIENT_VERSION_HEADER
from fiddler.v2.schema.server_info import ServerInfo

logger = logging.getLogger(__name__)
VERSION = '/v2'


class Client(
    ModelMixin,
    DatasetMixin,
    ProjectMixin,
    EventsMixin,
    JobMixin,
    BaselineMixin,
    AlertMixin,
):
    def __init__(
        self, url: str, organization_name: str, auth_token: str, timeout: int = None
    ) -> None:
        self.url = urljoin(url, VERSION)
        self.auth_token = auth_token
        self.organization_name = organization_name
        self.request_headers = {'Authorization': f'Bearer {auth_token}'}
        self.request_headers.update({FIDDLER_CLIENT_VERSION_HEADER: f'{__version__}'})
        self.timeout = timeout
        self.client = RequestClient(self.url, self.request_headers)

        # @TODO Move this from optional to required once /get_supported_features api moved to v2
        self.server_info: Optional[ServerInfo] = None
