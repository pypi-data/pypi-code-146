import json
import logging
from typing import Union

from truera.client.public.auth_details import AuthDetails
from truera.client.public.communicator.http_communicator import \
    HttpCommunicator


class HttpMrcCommunicator():

    def __init__(
        self,
        connection_string: str,
        auth_details: AuthDetails,
        logger: logging.Logger,
        *,
        verify_cert: Union[bool, str] = True
    ):
        self.logger = logging.getLogger(__name__)
        self.http_communicator = HttpCommunicator(
            connection_string=connection_string,
            auth_details=auth_details,
            logger=logger,
            verify_cert=verify_cert
        )

    def get_runs(self, project_id: str):
        next_token = ""
        runs = []
        while next_token is not None:
            uri = f"{self.http_communicator.connection_string}/model-runner/v0/runs?project_id={project_id}&next_token={next_token}"
            response = json.loads(self.http_communicator.get_request(uri, None))
            runs.extend(response.get("data"))
            next_token = response.get("next_token", None)
        return {"data": runs}
