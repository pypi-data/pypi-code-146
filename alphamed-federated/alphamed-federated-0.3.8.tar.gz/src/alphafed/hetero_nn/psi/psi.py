"""Private Set Intersection basic components."""


from abc import ABC, abstractmethod
from typing import List, Set

from ... import logger

__all__ = ['IntersectionError', 'PSIInitiatorScheduler', 'PSICollaboratorScheduler']


class IntersectionError(Exception):
    ...


class PSIInitiatorScheduler(ABC):

    def __init__(self,
                 task_id: str,
                 initiator_id: str,
                 ids: List[str],
                 collaborator_ids: List[str]) -> None:
        """Schedule the process of PSI as the initiator.

        :args
            :initiator_id
                The ID of the initiator.
            :ids
                The list of local ID strings.
            :collaborator_ids
                The ID list of collaborators.
        """
        super().__init__()
        if not task_id or not isinstance(task_id, str):
            raise ValueError(f'Invalid task ID: {task_id}')
        if not initiator_id or not isinstance(initiator_id, str):
            raise ValueError(f'must specify the ID of initiator, got: {initiator_id}')
        if (
            not ids or not isinstance(ids, list)
            or not all(_id and isinstance(_id, str) for _id in ids)
        ):
            raise ValueError(f'ids must be a list of string, got: {ids}')
        if (
            not collaborator_ids or not isinstance(collaborator_ids, list)
            or not all(_coll and isinstance(_coll, str) for _coll in collaborator_ids)
        ):
            raise ValueError(f'must specify the ID list of collaborators, got: {collaborator_ids}')

        self.task_id = task_id
        self.initiator_id = initiator_id
        self.ids = ids
        self.collaborator_ids = collaborator_ids

    @abstractmethod
    def make_intersection(self) -> Set[str]:
        """Initiate a process to get the intersection ids with a list of collaborators.

        :return
            The intersection of ID strings.
        """
        ...

    def _switch_status(self, _status: str):
        """Switch to a new status and leave a log."""
        self.status = _status
        logger.debug(f'{self.status=}')


class PSICollaboratorScheduler(ABC):

    def __init__(self, task_id: str, collaborator_id: str, ids: List[str]) -> None:
        """Schedule the process of PSI as a collaborator.

        :args
            :collaborator_id
                The ID of the collaborator.
            :ids
                The list of local ID strings.
        """
        super().__init__()
        if not task_id or not isinstance(task_id, str):
            raise ValueError(f'Invalid task ID: {task_id}')
        if not collaborator_id or not isinstance(collaborator_id, str):
            raise ValueError(f'must specify the ID of collaborator, got: {collaborator_id}')
        if (
            not ids or not isinstance(ids, list)
            or not all(_id and isinstance(_id, str) for _id in ids)
        ):
            raise ValueError(f'ids must be a list of string, got: {ids}')

        self.task_id = task_id
        self.collaborator_id = collaborator_id
        self.ids = ids

    @abstractmethod
    def collaborate_intersection(self) -> Set[str]:
        """Collaborate in a process to get the intersection ids.

        :return
            The intersection of ID strings.
        """
        ...

    def _switch_status(self, _status: str):
        """Switch to a new status and leave a log."""
        self.status = _status
        logger.debug(f'{self.status=}')
