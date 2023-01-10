"""create_run SDK for Kubernetes"""

from __future__ import annotations

import datetime as dt
import uuid
from concurrent.futures import Future
from typing import Optional, Union, overload

from typing_extensions import Literal

from mcli.api.engine.engine import run_kube_in_threadpool
from mcli.api.model.run import Run
from mcli.models.mcli_integration import IntegrationType
from mcli.models.run_config import FinalRunConfig, RunConfig
from mcli.serverside.clusters.cluster import PriorityLabel
from mcli.serverside.job.mcli_job import MCLIJob, MCLIJobType
from mcli.serverside.runners.runner import Runner
from mcli.utils.utils_run_status import RunStatus

__all__ = ['create_run']


def _submit_run(model: Run,
                mcli_job: MCLIJob,
                priority: Optional[str] = None,
                job_type: MCLIJobType = MCLIJobType.RUN) -> Run:
    """Submit a run and return the run model

    This is only used to provide the same "future" and "timeout" interface for the
    kubernetes calls as for the MAPI calls.

    Args:
        model: The run that will be returned
        mcli_job: The job that will be submitted
        priority: The priority that the job should be submitted at. Defaults to None.

    Returns:
        The run that was passed in
    """

    # Processes local integration before run starts
    for integration in mcli_job.integrations:
        if integration.integration_type == IntegrationType.local:
            integration.build_to_docker(mcli_job.image)

    Runner().submit(job=mcli_job, priority_class=priority, job_type=job_type)
    return model


@overload
def create_run(
    run: Union[RunConfig, FinalRunConfig],
    timeout: Optional[float] = 10,
    future: Literal[False] = False,
    _priority: Optional[Union[PriorityLabel, str]] = None,
    _job_type: MCLIJobType = MCLIJobType.RUN,
) -> Run:
    ...


@overload
def create_run(
    run: Union[RunConfig, FinalRunConfig],
    timeout: Optional[float] = None,
    future: Literal[True] = True,
    _priority: Optional[Union[PriorityLabel, str]] = None,
    _job_type: MCLIJobType = MCLIJobType.RUN,
) -> Future[Run]:
    ...


def create_run(
    run: Union[RunConfig, FinalRunConfig],
    timeout: Optional[float] = 10,
    future: bool = False,
    _priority: Optional[Union[PriorityLabel, str]] = None,
    _job_type: MCLIJobType = MCLIJobType.RUN,
):
    """Launch a run

    Launch a run in the MosaicML Cloud. The provided :class:`run <mcli.models.run_config.RunConfig>`
    must contain enough details to fully configure the run. If it does not, an error will be thrown.

    Args:
        run (:class:`~mcli.models.run_config.RunConfig`):
            A :class:`run configuration <mcli.models.run_config.RunConfig>` with enough
            details to launch. The run will be queued and persisted in the run database.
        timeout (``Optional[float]``): Time, in seconds, in which the call should complete.
            If the run creation takes too long, a :exc:`~concurrent.futures.TimeoutError`
            will be raised. If ``future`` is ``True``, this value will be ignored.
        future (``bool``): Return the output as a :class:`~concurrent.futures.Future`. If True, the
            call to :func:`create_run` will return immediately and the request will be
            processed in the background. This takes precedence over the ``timeout``
            argument. To get the :class:`~mcli.api.model.run.Run` output, use ``return_value.result()``
            with an optional ``timeout`` argument.
        _priority (``Optional[PriorityLabel | str]``): **DEPRECATED** An optional priority
            level at which the run should be created. Only effective for certain clusters.
        _job_type (``MCLIJobType``): **DEPRECATED** An optional "job type" descriptor for the run

    Raises:
        ``InstanceTypeUnavailable``: Raised if an invalid compute instance is requested

    Returns:
        If future is False:
            The created :class:`~mcli.api.model.run.Run` object
        Otherwise:
            A :class:`~concurrent.futures.Future` for the object
    """

    if isinstance(run, RunConfig):
        run = FinalRunConfig.finalize_config(run)

    if isinstance(_priority, PriorityLabel):
        _priority = _priority.value
        assert not isinstance(_priority, PriorityLabel)

    mcli_job = MCLIJob.from_final_run_config(run)
    mock_uuid = str(uuid.uuid4())
    model = Run(
        run_uid=mock_uuid,
        name=mcli_job.unique_name,
        status=RunStatus.PENDING,
        created_at=dt.datetime.now(),
        updated_at=dt.datetime.now(),
        config=run,
    )

    res = run_kube_in_threadpool(_submit_run, model, mcli_job, _priority, _job_type)

    if not future:
        return res.result(timeout=timeout)
    else:
        return res
