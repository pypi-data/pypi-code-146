"""Utilities for interpreting pod status"""
from __future__ import annotations

import functools
from dataclasses import dataclass
from enum import Enum, EnumMeta
from typing import Any, Dict, List, Set, Type, TypeVar

from kubernetes import client

from mcli.utils.utils_kube import deserialize
from mcli.utils.utils_string_functions import camel_case_to_snake_case, snake_case_to_camel_case

__all__ = ['RunStatus']


class StatusMeta(EnumMeta):
    """Metaclass for RunStatus that adds some useful class properties
    """

    @property
    def failed_states(cls) -> Set[RunStatus]:
        return {RunStatus.FAILED, RunStatus.FAILED_PULL, RunStatus.TERMINATING, RunStatus.STOPPED, RunStatus.STOPPING}

    @property
    def order(cls) -> List[RunStatus]:
        """Order of pod states, from latest to earliest
        """
        return [
            RunStatus.FAILED,
            RunStatus.FAILED_PULL,
            RunStatus.STOPPED,
            RunStatus.COMPLETED,
            RunStatus.STOPPING,
            RunStatus.TERMINATING,
            RunStatus.RUNNING,
            RunStatus.STARTING,
            RunStatus.SCHEDULED,
            RunStatus.QUEUED,
            RunStatus.PENDING,
            RunStatus.UNKNOWN,
        ]


@functools.total_ordering
class RunStatus(Enum, metaclass=StatusMeta):
    """Possible statuses of a run
    """

    #: The run has been dispatched and is waiting to be received
    PENDING = 'PENDING'

    #: The run has been scheduled and is waiting to be queued
    SCHEDULED = 'SCHEDULED'

    #: The run is queued and is awaiting execution
    QUEUED = 'QUEUED'

    #: The run is starting up and preparing to run
    STARTING = 'STARTING'

    #: The run is actively running
    RUNNING = 'RUNNING'

    #: The run is in the process of being terminated
    TERMINATING = 'TERMINATING'

    #: The run is in the process of being stopped
    STOPPING = 'STOPPING'

    #: The run has finished without any errors
    COMPLETED = 'COMPLETED'

    #: The run has stopped
    STOPPED = 'STOPPED'

    #: The run has failed due to a kubernetes error
    FAILED_PULL = 'FAILED_PULL'

    #: The run has failed due to an issue at runtime
    FAILED = 'FAILED'

    #: A valid run status cannot be found
    UNKNOWN = 'UNKNOWN'

    def __str__(self) -> str:
        return self.value

    def __lt__(self, other: RunStatus):
        if not isinstance(other, RunStatus):
            raise TypeError(f'Cannot compare order of ``RunStatus`` and {type(other)}')
        return RunStatus.order.index(self) > RunStatus.order.index(other)

    def before(self, other: RunStatus, inclusive: bool = False) -> bool:
        """Returns True if this state usually comes "before" the other

        Args:
            other: Another :class:`~mcli.utils.utils_run_status.RunStatus`
            inclusive: If True, equality evaluates to True. Default False.

        Returns:
            If this state is "before" the other

        Example:
            >>> RunStatus.RUNNING.before(RunStatus.COMPLETED)
            True
            >>> RunStatus.PENDING.before(RunStatus.RUNNING)
            True
        """
        return (self < other) or (inclusive and self == other)

    def after(self, other: RunStatus, inclusive: bool = False) -> bool:
        """Returns True if this state usually comes "after" the other

        Args:
            other: Another :class:`~mcli.utils.utils_run_status.RunStatus`
            inclusive: If True, equality evaluates to True. Default False.

        Returns:
            If this state is "after" the other

        Example:
            >>> RunStatus.RUNNING.before(RunStatus.COMPLETED)
            True
            >>> RunStatus.PENDING.before(RunStatus.RUNNING)
            True
        """
        return (self > other) or (inclusive and self == other)

    @classmethod
    def from_string(cls, run_status: str) -> RunStatus:
        """Convert a string to a valid RunStatus Enum

        If the run status string is not recognized, will return RunStatus.UNKNOWN
        instead of raising a KeyError
        """
        if isinstance(run_status, RunStatus):
            return run_status

        default = RunStatus.UNKNOWN
        try:
            key = camel_case_to_snake_case(run_status).upper()
            return cls[key]
        except TypeError:
            return default
        except KeyError:
            return default

    @property
    def display_name(self) -> str:
        return snake_case_to_camel_case(self.value, capitalize_first=True)


# pylint: disable-next=invalid-name
CLI_STATUS_OPTIONS = [state.display_name for state in RunStatus]

StatusType = TypeVar('StatusType')  # pylint: disable=invalid-name


@dataclass
class PodStatus():
    """Base pod status detector
    """
    state: RunStatus
    message: str = ''
    reason: str = ''

    @classmethod
    def from_pod_dict(cls: Type[PodStatus], pod_dict: Dict[str, Any]) -> PodStatus:
        """Get the status of a pod from its dictionary representation

        This is useful if the pod has already been converted to a JSON representation

        Args:
            pod_dict: Dictionary representation of a V1Pod object

        Returns:
            PodStatus instance
        """
        if 'status' not in pod_dict:
            raise KeyError('pod_dict must have a valid "status" key')
        pod = deserialize(pod_dict, 'V1Pod')
        return cls.from_pod(pod)

    @classmethod
    def _pending_phase_match(cls: Type[PodStatus], pod: client.V1Pod) -> PodStatus:

        # Scheduled or queuing
        conditions = pod.status.conditions if pod.status.conditions else []
        if conditions:
            scheduled_condition = [c for c in conditions if c.type == 'PodScheduled'][0]
            if scheduled_condition.status == 'True' and len(conditions) == 1:
                return PodStatus(state=RunStatus.SCHEDULED)
            elif scheduled_condition.status == 'False' and scheduled_condition.reason == 'Unschedulable':
                return PodStatus(state=RunStatus.QUEUED)

        # Attempting to start container
        container_statuses = pod.status.container_statuses if pod.status.container_statuses else []
        if container_statuses:
            waiting = container_statuses[0].state.waiting
            if waiting and 'ContainerCreating' in waiting.reason:
                return PodStatus(state=RunStatus.STARTING)
            elif waiting and waiting.reason in {'ErrImagePull', 'ImagePullBackOff'}:
                return PodStatus(state=RunStatus.FAILED_PULL)

        # Else generic pending
        return PodStatus(state=RunStatus.PENDING)

    @classmethod
    def _running_phase_match(cls: Type[PodStatus], pod: client.V1Pod) -> PodStatus:
        del pod
        return PodStatus(state=RunStatus.RUNNING)

    @classmethod
    def _completed_phase_match(cls: Type[PodStatus], pod: client.V1Pod) -> PodStatus:
        del pod
        return PodStatus(state=RunStatus.COMPLETED)

    @classmethod
    def _failed_phase_match(cls: Type[PodStatus], pod: client.V1Pod) -> PodStatus:
        container_statuses = pod.status.container_statuses or []
        if container_statuses:
            terminated = container_statuses[0].state.terminated
            if terminated and terminated.exit_code == 137:
                return PodStatus(state=RunStatus.STOPPED)
        return PodStatus(state=RunStatus.FAILED)

    @classmethod
    def _unknown_phase_match(cls: Type[PodStatus], pod: client.V1Pod) -> PodStatus:
        del pod
        return PodStatus(state=RunStatus.UNKNOWN)

    @classmethod
    def from_pod(cls: Type[PodStatus], pod: client.V1Pod) -> PodStatus:
        """Get the appropriate PodStatus instance from a Kubernetes V1PodStatus object

        The resulting PodStatus instance contains parsed information about the current state of the pod

        Args:
            status: Valid V1PodStatus object

        Returns:
            PodStatus instance
        """

        if getattr(pod.metadata, 'deletion_timestamp', None) is not None:
            return PodStatus(state=RunStatus.TERMINATING)

        if pod.status.phase == 'Pending':
            return cls._pending_phase_match(pod)
        elif pod.status.phase == 'Running':
            return cls._running_phase_match(pod)
        elif pod.status.phase == 'Succeeded':
            return cls._completed_phase_match(pod)
        elif pod.status.phase == 'Failed':
            return cls._failed_phase_match(pod)
        else:
            return cls._unknown_phase_match(pod)
