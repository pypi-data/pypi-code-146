import typing as t

import pyarrow as pa

from sarus_data_spec import typing as st
from sarus_data_spec.manager.asyncio.api.api_computation import ApiComputation
from sarus_data_spec.manager.asyncio.base import BaseAsyncManager
from sarus_data_spec.manager.asyncio.worker.arrow_computation import (
    ToArrowComputation,
)
from sarus_data_spec.manager.asyncio.worker.cache_scalar_computation import (
    CacheScalarComputation,
)
from sarus_data_spec.manager.asyncio.worker.caching_computation import (
    ToParquetComputation,
)
from sarus_data_spec.manager.asyncio.worker.schema_computation import (
    SchemaComputation,
)
from sarus_data_spec.manager.asyncio.worker.value_computation import (
    ValueComputation,
)
from sarus_data_spec.manager.ops.asyncio.processor.routing import (
    TransformedDataset,
    TransformedScalar,
)
from sarus_data_spec.manager.ops.asyncio.source.routing import SourceScalar
import sarus_data_spec.manager.typing as smt
import sarus_data_spec.protobuf as sp
import sarus_data_spec.status as stt
import sarus_data_spec.storage.typing as storage_typing


class DelegatingManager(BaseAsyncManager):
    """Manager that can compute a result locally or delegate a computation.

    This manager is initialized with a reference to the remote Manager so that
    we can register its statuses in the local storage.

    The local computations implementations are taken from the WorkerManager.

    Subclasses should implement the following three computations to compute
    values remotely:
        - self.remote_to_parquet_computation
        - self.remote_to_arrow_computation
        - self.remote_value_computation

    Subclasses also have to implement the `is_remotely_computed` method to
    decide if a computation should be performed locally or remotely.

    Finally, subclasses should implement the `delegate_manager_statuses` method
    to fetch statuses from the remote Manager.
    """

    def __init__(
        self,
        storage: storage_typing.Storage,
        protobuf: sp.Manager,
        remote_manager: smt.Manager,
    ) -> None:
        super().__init__(storage, protobuf)
        self.remote_manager = remote_manager
        self.local_schema_computation = SchemaComputation(self)
        self.local_to_arrow_computation = ToArrowComputation(self)
        self.local_value_computation = ValueComputation(self)
        self.local_to_parquet_computation = ToParquetComputation(
            self, ToArrowComputation(self)
        )
        self.local_cache_scalar_computation = CacheScalarComputation(
            self, ValueComputation(self)
        )

        # To define in subclasses
        self.remote_to_parquet_computation: ApiComputation[
            t.AsyncIterator[pa.RecordBatch]
        ]
        self.remote_to_arrow_computation: ApiComputation[
            t.AsyncIterator[pa.RecordBatch]
        ]
        self.remote_cache_scalar_computation: ApiComputation[t.Any]
        self.remote_value_computation: ApiComputation[t.Any]

    def dataspec_computation(self, dataspec: st.DataSpec) -> smt.Computation:
        """Return the computation for a Dataspec."""
        is_cached = self.is_cached(dataspec)
        is_delegated = self.is_delegated(dataspec)
        proto = dataspec.prototype()
        if proto == sp.Dataset:
            if is_cached:
                if is_delegated:
                    return self.remote_to_parquet_computation
                else:
                    return self.local_to_parquet_computation
            else:
                if is_delegated:
                    return self.remote_to_arrow_computation
                else:
                    return self.local_to_arrow_computation
        else:
            if is_cached:
                if is_delegated:
                    return self.remote_cache_scalar_computation
                else:
                    return self.local_cache_scalar_computation
            else:
                if is_delegated:
                    return self.remote_value_computation
                else:
                    return self.local_value_computation

    def _delegate_manager_status(
        self, dataspec: st.DataSpec, task_name: str
    ) -> t.Optional[st.Status]:
        """Fetch the remote status a single Dataspec."""
        statuses = self._delegate_manager_statuses(
            [dataspec], task_name=task_name
        )
        (status,) = statuses
        return status

    def _delegate_manager_statuses(
        self, dataspecs: t.List[st.DataSpec], task_name: str
    ) -> t.List[t.Optional[st.Status]]:
        """Fetch the remote statuses for a list of Dataspecs."""
        raise NotImplementedError

    def is_delegated(self, dataspec: st.DataSpec) -> bool:
        """Return True is the dataspec's computation is delegated."""
        raise NotImplementedError

    def is_cached(self, dataspec: st.DataSpec) -> bool:
        """Sets whether a dataset should be cached or not"""
        raise NotImplementedError

    def status(
        self, dataspec: st.DataSpec, task_name: str
    ) -> t.Optional[st.Status]:
        """Reads the delegate manager's status and update the API status if
        needed.

        Returns the API manager's status.
        """
        local_status = stt.last_status(
            dataspec=dataspec,
            task=task_name,
            manager=self,
        )

        if not self.is_delegated(dataspec):
            # computation not delegated, return local status
            return local_status

        delegate_status = self._delegate_manager_status(dataspec, task_name)
        if delegate_status is None:
            # return local status which may be pending
            return local_status

        local_stage = local_status.task(task_name) if local_status else None
        delegate_stage = delegate_status.task(task_name)
        assert delegate_stage

        if delegate_stage == local_stage:
            # no progress: update not needed
            return local_status

        # copy delegate manager status as API status
        if delegate_stage.ready():
            status = stt.ready(
                dataspec=dataspec,
                task=task_name,
                manager=self,
                properties=delegate_stage.properties(),
            )
        elif delegate_stage.error():
            status = stt.error(
                dataspec=dataspec,
                task=task_name,
                manager=self,
                properties=delegate_stage.properties(),
            )
        elif delegate_stage.processing():
            status = stt.processing(
                dataspec=dataspec,
                task=task_name,
                manager=self,
                properties=delegate_stage.properties(),
            )
        elif delegate_stage.pending():
            raise ValueError('Delegate manager statuses should not be pending')
        else:
            raise ValueError('Delegate manager status not properly managed')

        return status

    async def async_schema(self, dataset: st.Dataset) -> st.Schema:
        """Schema computation is done locally."""
        return await self.local_schema_computation.task_result(
            dataspec=dataset
        )

    async def async_to_parquet(self, dataset: st.Dataset) -> None:
        await self.local_to_parquet_computation.complete_task(dataspec=dataset)

    async def async_cache_scalar(self, scalar: st.Scalar) -> None:
        await self.local_cache_scalar_computation.complete_task(
            dataspec=scalar
        )

    async def async_to_arrow_op(
        self, dataset: st.Dataset, batch_size: int
    ) -> t.AsyncIterator[pa.RecordBatch]:
        """Route a Dataset to its Op implementation.

        When the computation is not delegated the manager should also be
        able to compute the value.
        """
        if dataset.is_transformed():
            iterator = await TransformedDataset(dataset).to_arrow(
                batch_size=batch_size
            )
            return iterator

        else:
            raise ValueError('Dataset should be transformed.')

    async def async_value_op(self, scalar: st.Scalar) -> t.Any:
        """Route a Scalar to its Op implementation.

        This method is shared between API and Worker because when the data is
        not cached the API manager should also be able to compute the value.
        """
        if scalar.is_transformed():
            return await TransformedScalar(scalar).value()
        else:
            return await SourceScalar(scalar).value()

    async def async_schema_op(self, dataset: st.Dataset) -> st.Schema:
        if dataset.is_transformed():
            return await TransformedDataset(dataset).schema()
        else:
            raise ValueError('Dataset should be transformed.')
