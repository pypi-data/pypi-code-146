import logging
from typing import Sequence, Union

from truera.client.public.auth_details import AuthDetails
from truera.client.public.communicator.mrc_http_communicator import \
    HttpMrcCommunicator


class MrcClient:

    def __init__(
        self,
        connection_string: str = None,
        auth_details: AuthDetails = None,
        logger=None,
        *,
        verify_cert: Union[bool, str] = True
    ):
        self.logger = logger or logging.getLogger(__name__)
        self.communicator = HttpMrcCommunicator(
            connection_string, auth_details, logger, verify_cert=verify_cert
        )

    def get_current_runs(self, project_id: str) -> Sequence[str]:
        return [
            data["id"]
            for data in self.communicator.get_runs(project_id)["data"]
            if data['state'].lower() not in [
                "canceled", "failed", "finished"
            ]  # duplicating RunState constants to avoid importing MR deps
        ]

    def get_percentages_done(
        self, project_id: str, model_runner_ids: Sequence[str]
    ):
        json_resp = self.communicator.get_runs(project_id)
        ret = {}
        for data in json_resp["data"]:
            assert data["projectId"] == project_id
            model_runner_id = data["id"]
            if model_runner_id in model_runner_ids:
                assert model_runner_id not in ret
                task_status = data["job"]["taskStatus"]
                valid_progress_percent = (task_status is not None) and (
                    task_status["progressPercent"] is not None
                )
                ret[model_runner_id] = task_status[
                    "progressPercent"] if valid_progress_percent else 0
        return ret
