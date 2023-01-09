import logging
import os
import traceback
import typing as t

import pyarrow as pa
import pyarrow.parquet as pq

from sarus_data_spec import typing as st
from sarus_data_spec.constants import CACHE_PATH, TO_PARQUET_TASK
from sarus_data_spec.manager.asyncio.base import ErrorCatchingAsyncIterator
from sarus_data_spec.manager.asyncio.utils import async_iter
from sarus_data_spec.manager.asyncio.worker.arrow_computation import (
    ToArrowComputation,
)
from sarus_data_spec.manager.asyncio.worker.worker_computation import (
    TypedWorkerManager,
    WorkerComputation,
)
from sarus_data_spec.status import error, ready

logger = logging.getLogger(__name__)


class ToParquetComputation(WorkerComputation[t.AsyncIterator[pa.RecordBatch]]):
    """Class responsible for handling the caching
    in parquet of a dataset. It wraps a ToArrowComputation
    to get the iterator."""

    task_name = TO_PARQUET_TASK

    def __init__(
        self,
        manager: TypedWorkerManager,
        arrow_computation: ToArrowComputation,
    ) -> None:
        super().__init__(manager)
        self.arrow_computation = arrow_computation

    async def prepare(self, dataspec: st.DataSpec) -> None:

        logger.debug(f'STARTING TO_PARQUET {dataspec.uuid()}')
        try:
            iterator = await self.arrow_computation.task_result(
                dataspec, batch_size=5000
            )
            batches = [batch async for batch in iterator]
            pq.write_table(
                table=pa.Table.from_batches(batches),
                where=self.cache_path(dataspec=dataspec),
                version='2.6',
            )
        except Exception:
            error(
                dataspec=dataspec,
                manager=self.manager(),
                task=TO_PARQUET_TASK,
                properties={"message": traceback.format_exc()},
            )
        else:
            logger.debug(f'FINISHED TO_PARQUET {dataspec.uuid()}')
            ready(
                dataspec=dataspec,
                manager=self.manager(),
                task=TO_PARQUET_TASK,
                properties={CACHE_PATH: self.cache_path(dataspec)},
            )

    async def read_ready_result(
        self,
        dataspec: st.DataSpec,
        properties: t.Mapping[str, str],
        **kwargs: t.Any,
    ) -> t.AsyncIterator[pa.RecordBatch]:
        """Reads the cache and returns the arrow iterator"""

        batch_size = kwargs['batch_size']
        cache_path = properties[CACHE_PATH]
        ait = async_iter(
            pq.read_table(source=cache_path).to_batches(
                max_chunksize=batch_size
            )
        )
        return ErrorCatchingAsyncIterator(ait, dataspec, self)

    def cache_path(self, dataspec: st.DataSpec) -> str:
        """Returns the path where to cache the dataset"""
        return os.path.join(
            dataspec.manager().parquet_dir(), f"{dataspec.uuid()}.parquet"
        )
