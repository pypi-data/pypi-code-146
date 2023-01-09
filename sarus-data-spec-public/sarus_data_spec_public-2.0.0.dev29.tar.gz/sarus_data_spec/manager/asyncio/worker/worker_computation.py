import asyncio
import logging
import typing as t

import pyarrow as pa

from sarus_data_spec.manager.asyncio.base import BaseComputation, T
from sarus_data_spec.manager.typing import Manager
import sarus_data_spec.status as stt
import sarus_data_spec.typing as st

logger = logging.getLogger(__name__)

# This is done to avoid circular dependencies..


class TypedWorkerManager(Manager, t.Protocol):
    async def async_value_op(self, scalar: st.Scalar) -> st.DataSpecValue:
        ...

    async def async_schema_op(self, dataset: st.Dataset) -> st.Schema:
        ...

    async def async_to_arrow_op(
        self, dataset: st.Dataset, batch_size: int
    ) -> t.AsyncIterator[pa.RecordBatch]:
        ...


class WorkerComputation(BaseComputation[T]):
    def __init__(self, manager: TypedWorkerManager):
        self._manager: TypedWorkerManager = manager

    def manager(self) -> TypedWorkerManager:
        return self._manager

    async def read_ready_result(
        self,
        dataspec: st.DataSpec,
        properties: t.Mapping[str, str],
        **kwargs: t.Any,
    ) -> T:
        raise NotImplementedError

    async def processing(self, dataspec: st.DataSpec) -> st.Status:
        """If processing, wait for the task to be ready.
        Such a case can happen if another manager has taken the computation
        of the task. After a given timeout, an error is raised.
        """

        for i in range(100):
            status = stt.last_status(
                dataspec=dataspec, task=self.task_name, manager=self.manager()
            )
            assert status
            logger.debug(f'POLLING {self.task_name} {dataspec.uuid()}')
            stage = status.task(self.task_name)
            assert stage
            if not stage.processing():
                break
            await asyncio.sleep(1)

        assert stage
        if stage.processing():
            # clear the status processing
            # and relaunch task
            status.clear_task(self.task_name)  # type: ignore
        return await self.complete_task(dataspec)

    def launch_task(self, dataspec: st.DataSpec) -> t.Optional[t.Awaitable]:

        status = stt.last_status(
            dataspec=dataspec, manager=self.manager(), task=self.task_name
        )
        if status is None:
            stt.processing(
                dataspec=dataspec,
                manager=self.manager(),
                task=self.task_name,
            )
            return asyncio.create_task(
                self.prepare(dataspec),
                name=self.task_name + dataspec.uuid(),
            )

        return None

    async def prepare(self, dataspec: st.DataSpec) -> None:
        """Prepare the computation and set the status accordingly.

        It is up to the computation to define what preparing means. It can be
        computing and caching the data as well as simply checking that the
        parents are themselves ready.
        """
        raise NotImplementedError
