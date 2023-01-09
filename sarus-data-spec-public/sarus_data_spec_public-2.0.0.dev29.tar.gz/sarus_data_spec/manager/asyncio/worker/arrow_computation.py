import logging
import traceback
import typing as t

import pyarrow as pa

from sarus_data_spec import typing as st
from sarus_data_spec.constants import ARROW_TASK
from sarus_data_spec.dataset import Dataset
from sarus_data_spec.manager.asyncio.base import ErrorCatchingAsyncIterator
from sarus_data_spec.manager.asyncio.worker.worker_computation import (
    WorkerComputation,
)
import sarus_data_spec.status as stt

BATCH_SIZE = 2000

logger = logging.getLogger(__name__)


class ToArrowComputation(WorkerComputation[t.AsyncIterator[pa.RecordBatch]]):

    task_name = ARROW_TASK

    async def prepare(self, dataspec: st.DataSpec) -> None:
        try:
            logger.debug(f'STARTED ARROW {dataspec.uuid()}')
            # Only prepare parents since calling `to_arrow` will require the
            # computation of the scalars in the ancestry.
            dataset = t.cast(st.Dataset, dataspec)
            await self.manager().async_prepare_parents(dataset)

            if dataset.is_source():
                await self.manager().async_schema(dataset)
            elif dataset.is_transformed():
                transform = dataset.transform()
                if not transform.is_external():
                    await self.manager().async_schema(dataset)
        except Exception:
            stt.error(
                dataspec=dataspec,
                manager=self.manager(),
                task=self.task_name,
                properties={"message": traceback.format_exc()},
            )
        else:
            logger.debug(f'FINISHED ARROW {dataspec.uuid()}')
            stt.ready(
                dataspec=dataspec,
                manager=self.manager(),
                task=self.task_name,
            )

    async def read_ready_result(
        self,
        dataspec: st.DataSpec,
        properties: t.Mapping[str, str],
        **kwargs: t.Any,
    ) -> t.AsyncIterator[pa.RecordBatch]:
        """Returns the iterator"""
        batch_size = kwargs['batch_size']
        ait = await self.manager().async_to_arrow_op(
            dataset=t.cast(Dataset, dataspec), batch_size=batch_size
        )
        return ErrorCatchingAsyncIterator(ait, dataspec, self)
