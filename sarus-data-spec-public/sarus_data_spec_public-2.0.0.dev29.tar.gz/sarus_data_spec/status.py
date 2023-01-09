from __future__ import annotations

from datetime import datetime
from typing import Callable, List, Mapping, Optional, Type, cast
import logging
import typing as t

from sarus_data_spec.base import Base, Referring
from sarus_data_spec.dataset import Dataset
from sarus_data_spec.manager.typing import Manager
from sarus_data_spec.protobuf.typing import ProtobufWithUUIDAndDatetime
import sarus_data_spec.protobuf as sp
import sarus_data_spec.typing as st

logger = logging.getLogger(__name__)


class Status(Referring[sp.Status]):
    """A python class to describe status"""

    def __init__(self, protobuf: sp.Status, store: bool = True) -> None:
        self._referred = {
            protobuf.dataspec,
            protobuf.manager,
        }  # This has to be defined before it is initialized
        super().__init__(protobuf, store=store)

    def prototype(self) -> Type[sp.Status]:
        """Return the type of the underlying protobuf."""
        return sp.Status

    def datetime(self) -> datetime:
        return datetime.fromisoformat(self.protobuf().datetime)

    def update(
        self,
        task_stages: Optional[Mapping[str, st.Stage]] = None,
        properties: Optional[Mapping[str, str]] = None,
    ) -> Status:
        """
        This method apply an atomic update
        to the last version of the status. The update
        is not performed if the transition from the old
        to the new stage is a regression (see method
        transitions_allowed)
        """

        def update_last(
            status: st.Referring[ProtobufWithUUIDAndDatetime],
        ) -> t.Tuple[st.Referring[ProtobufWithUUIDAndDatetime], bool]:
            """Returns whether the update should be done, ie transitions
            are respected and the status that can be updated in case"""
            # We copy the content of the current status
            proto = cast(Status, status).protobuf()
            # We update its timestamp and properties
            proto.datetime = datetime.now().isoformat()
            if properties is not None:
                proto.properties.update(properties)
                # Protobuf implementation of the merge
                # does not work as expected on maps...
            if task_stages is not None:
                for task in task_stages:
                    stage = task_stages[task].protobuf()
                    if task in proto.task_stages and proto.task_stages[
                        task
                    ].WhichOneof('stage') == task_stages[
                        task
                    ].protobuf().WhichOneof(
                        'stage'
                    ):
                        proto.task_stages[task].properties.update(
                            stage.properties
                        )
                    else:
                        if transition_allowed(
                            existing_stage=proto.task_stages.get(task, None),
                            new_stage=stage,
                            task_name=task,
                        ):
                            proto.task_stages[task].CopyFrom(stage)
                        else:
                            return status, False
            # And return a new UNSTORED data spec object
            return Status(proto, store=False), True

        # Now update the last version of this status
        return cast(
            Status,
            self.storage().update_last_referring(
                self.referred(), self.type_name(), update_last
            ),
        )

    def clear_task(self, task: str) -> t.Optional[Status]:
        """Creates a new status removing the task specified.
        To remove the task specified, the stage must be either
        ready or error (a static situation in which no one
        is processing the task).
        If the task does not exist, nothing is created"""
        # We copy the content of the current status
        proto = self.protobuf()
        # We update its timestamp and properties
        proto.datetime = datetime.now().isoformat()
        try:
            stage = proto.task_stages.pop(task)
        except KeyError:
            return None
        # we can create a new empty status only
        # if the current stage is static ie ready
        # (for example when removing cache) or
        # error (relaunch after timeout)
        else:
            can_be_cleared = transition_allowed(
                existing_stage=stage, new_stage=None, task_name=task
            )
            if can_be_cleared:
                # create a new data spec object
                return Status(proto)
            return None

    def task(self, task: str) -> t.Optional[Stage]:
        stage = self.protobuf().task_stages.get(task, None)
        return Stage(stage) if stage is not None else stage

    def task_stages(self) -> t.Mapping[str, Stage]:
        return {
            stage_name: Stage(stage_proto)
            for stage_name, stage_proto in self.protobuf().task_stages.items()
        }

    def pending(
        self,
    ) -> bool:
        """this is true if all tasks have status at least pending
        (i.e. pending, processing or ready) and at least one is pending"""
        has_one = False
        all_better = True
        task_stages = self.protobuf().task_stages
        if task_stages is not None:
            for task in task_stages:
                has_one = has_one or task_stages[task].HasField('pending')
                all_better = all_better and not (
                    task_stages[task].HasField('error')
                )
        return has_one and all_better

    def processing(
        self,
    ) -> bool:
        """this is true if all tasks have status at least processing
        (i.e. processing or ready) and at least one is processing"""
        has_one = False
        all_better = True
        task_stages = self.protobuf().task_stages
        if task_stages is not None:
            for task in task_stages:
                has_one = has_one or task_stages[task].HasField('processing')
                all_better = all_better and not (
                    task_stages[task].HasField('error')
                    or task_stages[task].HasField('pending')
                )
        return has_one and all_better

    def ready(
        self,
    ) -> bool:  # TODO this should be true if all tasks have status ready
        """this is true if all tasks have status ready"""
        all_ready = True
        task_stages = self.protobuf().task_stages
        if task_stages is not None:
            for task in task_stages:
                all_ready = all_ready and task_stages[task].HasField('ready')
        return all_ready

    def error(
        self,
    ) -> bool:  # TODO this should be true if any task have status error
        """this is true if any tasks have status error"""
        has_error = False
        task_stages = self.protobuf().task_stages
        if task_stages is not None:
            for task in task_stages:
                has_error = has_error or task_stages[task].HasField('error')
        return has_error

    def dataset(self) -> Dataset:
        dataspec = self.dataspec()
        assert isinstance(dataspec, Dataset)
        return dataspec

    def dataspec(self) -> st.DataSpec:
        return cast(
            st.DataSpec, self.storage().referrable(self._protobuf.dataspec)
        )

    def owner(
        self,
    ) -> Manager:
        # TODO: Maybe find a better name, but this was shadowing
        # the actual manager of this object.  # noqa: E501
        return cast(Manager, self.storage().referrable(self._protobuf.manager))


def transition_allowed(
    existing_stage: t.Optional[sp.Status.Stage],
    new_stage: t.Optional[sp.Status.Stage],
    task_name: str,
) -> bool:
    """Method that verifies that the new stage for a given task
    can be set to the existing. The rule is that stages can only
    go towards a more advanced stage and never backwards, except
    for error and ready that can be reset to None.
    When the stage is None, it means that the task is not present"""

    if existing_stage is None:
        return True  # all transitions allowed if no task exists

    allowed_transitions = {
        'pending': ['processing', 'ready', 'error'],
        'processing': ['ready', 'error'],
        'ready': ['error', None],
        'error': [None],
    }
    if new_stage is not None:
        if (
            new_stage.WhichOneof('stage')  # type:ignore
            in allowed_transitions[
                existing_stage.WhichOneof('stage')  # type:ignore
            ]
        ):
            return True
        else:
            logger.warning(
                f"Trying to update a status with stage "
                f"{new_stage.WhichOneof('stage')} for the task {task_name} "
                f"while the existing stage "
                f"is {existing_stage.WhichOneof('stage')}, "
                f"therefore the update will be ignored"
            )
        return False

    else:
        if (
            new_stage  # type:ignore
            in allowed_transitions[
                existing_stage.WhichOneof('stage')  # type:ignore
            ]
        ):
            return True

        else:
            logger.warning(
                f"Trying to update a status with stage "
                f"{new_stage} for the task {task_name} "
                f"while the existing stage "
                f"is {existing_stage.WhichOneof('stage')}, "
                f"therefore the update will be ignored"
            )
            return False


# Builders
def status(
    dataspec: st.DataSpec,
    task_stages: Optional[Mapping[str, st.Stage]] = None,
    properties: Optional[Mapping[str, str]] = None,
    manager: Optional[Manager] = None,
) -> st.Status:
    """A builder to ease the construction of a status
    - dataspec: is the dataspec, the status is added to
    - manager: is which manager, if None,
        the default manager of the dataspec is used
    """
    # Use the right manager
    manager = dataspec.manager() if manager is None else manager
    # If a status already exists for the dataspec
    # and manager simply create an updated version of it
    last = last_status(dataspec=dataspec, manager=manager)
    if last is None:
        return Status(
            sp.Status(
                dataspec=dataspec.uuid(),
                manager=manager.uuid(),
                datetime=datetime.now().isoformat(),
                task_stages=None
                if task_stages is None
                else {
                    task: task_stages[task].protobuf() for task in task_stages
                },
                properties=properties,
            )
        )
    else:
        return last.update(task_stages=task_stages, properties=properties)


def last_status(
    dataspec: st.DataSpec,
    manager: Optional[Manager] = None,
    task: t.Optional[str] = None,
) -> Optional[st.Status]:
    """Return a DataSpec's last status by sorted datetime."""
    manager = dataspec.manager() if manager is None else manager
    status = cast(
        Optional[st.Status],
        manager.storage().last_referring(
            (dataspec, manager), sp.type_name(sp.Status)
        ),
    )

    if status is None or task is None:
        return status

    if status.task(task=task) is None:
        return None

    return status


def last_statuses(
    dataspec: st.DataSpec, task: t.Optional[str] = None
) -> List[st.Status]:
    """Return a list composed by the last status of every
    DataSpec's manager."""
    managers = dataspec.storage().type_name(sp.type_name(sp.Manager))
    statuses = []
    for manager in managers:
        stt = last_status(
            dataspec,
            cast(
                Optional[Manager],
                manager,
            ),
        )
        if stt is not None:
            if task is not None:
                if stt.task(task) is not None:
                    statuses.append(stt)
            else:
                statuses.append(stt)
    return statuses


class Stage(Base[sp.Status.Stage]):
    """A simple wrapper type to simplify protobuf usage"""

    def accept(self, visitor: st.StageVisitor) -> None:
        dispatch: Callable[[], None] = {
            'pending': visitor.pending,
            'processing': visitor.processing,
            'ready': visitor.ready,
            'error': visitor.error,
        }[cast(str, self.protobuf().WhichOneof('stage'))]
        dispatch()

    def stage(self) -> str:
        return cast(str, self.protobuf().WhichOneof('stage'))

    def ready(self) -> bool:
        return self.stage() == 'ready'

    def pending(self) -> bool:
        return self.stage() == 'pending'

    def processing(self) -> bool:
        return self.stage() == 'processing'

    def error(self) -> bool:
        return self.stage() == 'error'


# Builders for stages
def pending_stage(properties: Optional[Mapping[str, str]] = None) -> Stage:
    return Stage(
        sp.Status.Stage(
            pending=sp.Status.Stage.Pending(), properties=properties
        )
    )


def processing_stage(properties: Optional[Mapping[str, str]] = None) -> Stage:
    return Stage(
        sp.Status.Stage(
            processing=sp.Status.Stage.Processing(), properties=properties
        )
    )


def ready_stage(properties: Optional[Mapping[str, str]] = None) -> Stage:
    return Stage(
        sp.Status.Stage(ready=sp.Status.Stage.Ready(), properties=properties)
    )


def error_stage(properties: Optional[Mapping[str, str]] = None) -> Stage:
    return Stage(
        sp.Status.Stage(error=sp.Status.Stage.Error(), properties=properties)
    )


# Builders for statuses


def properties(
    dataspec: st.DataSpec,
    properties: Optional[Mapping[str, str]],
    manager: Optional[Manager] = None,
) -> st.Status:
    return status(
        dataspec,
        task_stages=None,
        properties=properties,
        manager=manager,
    )


def pending(
    dataspec: st.DataSpec,
    task: str,
    properties: Optional[Mapping[str, str]] = None,
    manager: Optional[Manager] = None,
) -> st.Status:
    return status(
        dataspec,
        task_stages={task: pending_stage(properties=properties)},
        properties=None,
        manager=manager,
    )


def processing(
    dataspec: st.DataSpec,
    task: str,
    properties: Optional[Mapping[str, str]] = None,
    manager: Optional[Manager] = None,
) -> st.Status:
    return status(
        dataspec,
        task_stages={task: processing_stage(properties=properties)},
        properties=None,
        manager=manager,
    )


def ready(
    dataspec: st.DataSpec,
    task: str,
    properties: Optional[Mapping[str, str]] = None,
    manager: Optional[Manager] = None,
) -> st.Status:
    return status(
        dataspec,
        task_stages={task: ready_stage(properties=properties)},
        properties=None,
        manager=manager,
    )


def error(
    dataspec: st.DataSpec,
    task: str,
    properties: Optional[Mapping[str, str]] = None,
    manager: Optional[Manager] = None,
) -> st.Status:
    return status(
        dataspec,
        task_stages={task: error_stage(properties=properties)},
        properties=None,
        manager=manager,
    )


def clear_task(dataspec: st.DataSpec, task: str) -> None:
    """This methods creates a new status for each manager
    where the specified task has been cleared"""

    statuses = last_statuses(dataspec)
    for manager_status in statuses:
        manager_status.clear_task(task)
