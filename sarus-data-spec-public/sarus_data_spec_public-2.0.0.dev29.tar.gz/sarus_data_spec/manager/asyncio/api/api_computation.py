import asyncio
import logging
import typing as t

import pyarrow as pa

from sarus_data_spec.manager.asyncio.base import BaseComputation, T
from sarus_data_spec.manager.typing import DelegatedComputation, Manager
import sarus_data_spec.status as stt
import sarus_data_spec.typing as st

logger = logging.getLogger(__name__)


class TypedApiManager(Manager, t.Protocol):
    async def async_to_arrow_op(
        self, dataset: st.Dataset, batch_size: int
    ) -> t.AsyncIterator[pa.RecordBatch]:
        ...

    async def async_value_op(self, scalar: st.Scalar) -> st.DataSpecValue:
        ...


class ApiComputation(BaseComputation[T], DelegatedComputation):
    def __init__(self, manager: TypedApiManager):
        self._manager: TypedApiManager = manager

    def manager(self) -> TypedApiManager:
        return self._manager

    async def read_ready_result(
        self,
        dataspec: st.DataSpec,
        properties: t.Mapping[str, str],
        **kwargs: t.Any,
    ) -> T:
        raise NotImplementedError

    async def pending(self, dataspec: st.DataSpec) -> st.Status:
        """if the status of a task is pending, delegation has been
        already done, so the manager just waits for the task to
        be completed"""

        for _ in range(100):
            logger.debug(f'POLLING {self.task_name} {dataspec.uuid()}')
            status = self.status(dataspec=dataspec)
            if status is None:
                await asyncio.sleep(1)
                continue
            else:
                break

        assert status
        stage = status.task(self.task_name)
        assert stage
        if stage.pending():
            # TODO push error status to worker ?
            stt.error(
                dataspec=dataspec,
                manager=dataspec.manager(),
                task=self.task_name,
                properties={
                    "message": f'Timeout exceeded in Pending task {self.task_name}'  # noqa: E501
                },
            )

        return await self.complete_task(dataspec)

    async def processing(self, dataspec: st.DataSpec) -> st.Status:
        """If processing, wait for the task to be ready.
        Such a case can happen if another manager has taken the computation
        of the task. After a given timeout, an error is raised.
        """

        for _ in range(100):
            logger.debug(f'POLLING {self.task_name} {dataspec.uuid()}')
            status = self.status(dataspec=dataspec)
            assert status
            stage = status.task(self.task_name)
            assert stage
            if stage.processing():
                await asyncio.sleep(1)
                continue
            else:
                break

        assert stage
        if stage.processing() or stage.pending():
            # TODO push error status to worker ?
            stt.error(
                dataspec=dataspec,
                manager=dataspec.manager(),
                task=self.task_name,
                properties={
                    "message": f'Timeout exceeded in Processing task {self.task_name}'  # noqa: E501
                },
            )

        return await self.complete_task(dataspec)
