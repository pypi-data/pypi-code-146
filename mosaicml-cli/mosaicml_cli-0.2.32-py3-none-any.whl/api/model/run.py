""" GraphQL representation of MCLIJob"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from http import HTTPStatus
from typing import Any, Dict, Optional, Tuple

from mcli.api.exceptions import MAPIException
from mcli.api.schema.generic_model import DeserializableModel, convert_datetime
from mcli.models.run_config import FinalRunConfig
from mcli.serverside.job.mcli_job import MCLIJobType
from mcli.utils.utils_run_status import RunStatus


@dataclass
class Run(DeserializableModel):
    """A run that has been launched on the MosaicML Cloud

    Args:
        run_uid (`str`): Unique identifier for the run
        run (`str`): User-defined name of the run
        status (:class:`~mcli.utils.utils_run_status.RunStatus`): Status of the run at a moment in time
        created_at (`datetime`): Date and time when the run was created
        updated_at (`datetime`): Date and time when the run was last updated
        config (:class:`~mcli.models.run_config.RunConfig`): The
            :class:`run configuration <mcli.models.run_config.RunConfig>` that was used to launch to the run

        started_at (`Optional[datetime]`): Date and time when the run entered
            the `STARTED` :class:`~mcli.utils.utils_run_status.RunStatus`
        completed_at (`Optional[datetime]`): Date and time when the run entered
            the `COMPLETED` :class:`~mcli.utils.utils_run_status.RunStatus`
    """

    run_uid: str
    name: str
    status: RunStatus
    created_at: datetime
    updated_at: datetime
    config: FinalRunConfig

    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    reason: Optional[str] = None

    _required_properties: Tuple[str] = tuple([
        'id',
        'name',
        'status',
        'createdAt',
        'updatedAt',
        'runInput',
    ])

    # This "job type" field is used only by interactive sessions in kube mcli
    # Let's add it as an optional only to be used by api.kube.get_runs
    _type: Optional[MCLIJobType] = None

    @classmethod
    def from_mapi_response(cls, response: Dict[str, Any]) -> Run:
        missing = set(cls._required_properties) - set(response)
        if missing:
            raise MAPIException(
                status=HTTPStatus.BAD_REQUEST,
                message=f'Missing required key(s) in response to deserialize Run object: {", ".join(missing)}',
            )

        started_at = None
        if response['startedAt'] is not None:
            started_at = convert_datetime(response['startedAt'])

        completed_at = None
        if response['completedAt'] is not None:
            completed_at = convert_datetime(response['completedAt'])

        return cls(run_uid=response['id'],
                   name=response['name'],
                   created_at=convert_datetime(response['createdAt']),
                   started_at=started_at,
                   completed_at=completed_at,
                   updated_at=convert_datetime(response['updatedAt']),
                   status=RunStatus.from_string(response['status']),
                   config=FinalRunConfig.from_mapi_response(response['runInput']),
                   reason=response['reason'])
