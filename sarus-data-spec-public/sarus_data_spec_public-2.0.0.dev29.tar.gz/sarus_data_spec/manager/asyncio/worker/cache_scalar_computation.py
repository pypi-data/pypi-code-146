import logging
import os
import pickle as pkl
import traceback
import typing as t

from sarus_data_spec import typing as st
from sarus_data_spec.constants import (
    CACHE_PATH,
    CACHE_PROTO,
    CACHE_SCALAR_TASK,
    CACHE_TYPE,
    ScalarCaching,
)
from sarus_data_spec.manager.asyncio.worker.value_computation import (
    ValueComputation,
)
from sarus_data_spec.manager.asyncio.worker.worker_computation import (
    TypedWorkerManager,
    WorkerComputation,
)
from sarus_data_spec.status import error, ready
import sarus_data_spec.protobuf as sp

logger = logging.getLogger(__name__)


class CacheScalarComputation(WorkerComputation[t.Any]):
    """Class responsible for handling the caching
    in of a scalar. It wraps a ValueComputation to get the value."""

    task_name = CACHE_SCALAR_TASK

    def __init__(
        self,
        manager: TypedWorkerManager,
        value_computation: ValueComputation,
    ) -> None:
        super().__init__(manager)
        self.value_computation = value_computation

    async def prepare(self, dataspec: st.DataSpec) -> None:

        logger.debug(f'STARTING CACHE_SCALAR {dataspec.uuid()}')
        try:
            value = await self.value_computation.task_result(dataspec)

            if isinstance(value, st.HasProtobuf):
                properties = {
                    CACHE_PROTO: sp.to_base64(value.protobuf()),
                    CACHE_TYPE: sp.type_name(value.prototype()),
                }
            else:
                properties = {
                    CACHE_TYPE: ScalarCaching.PICKLE.value,
                    CACHE_PATH: self.cache_path(dataspec),
                }
                with open(self.cache_path(dataspec), "wb") as f:
                    pkl.dump(value, f)

        except Exception:
            error(
                dataspec=dataspec,
                manager=self.manager(),
                task=self.task_name,
                properties={"message": traceback.format_exc()},
            )
        else:
            logger.debug(f'FINISHED CACHE_SCALAR {dataspec.uuid()}')
            ready(
                dataspec=dataspec,
                manager=self.manager(),
                task=self.task_name,
                properties=properties,
            )

    async def read_ready_result(
        self,
        dataspec: st.DataSpec,
        properties: t.Mapping[str, str],
        **kwargs: t.Any,
    ) -> t.Any:
        """Reads the cache and returns the value."""
        if properties[CACHE_TYPE] == ScalarCaching.PICKLE.value:
            with open(properties[CACHE_PATH], "rb") as f:
                data = pkl.load(f)
            return data

        return sp.python_proto_factory(
            properties[CACHE_PROTO], properties[CACHE_TYPE]
        )

    def cache_path(self, dataspec: st.DataSpec) -> str:
        """Returns the path where to cache the scalar."""
        return os.path.join(
            dataspec.manager().parquet_dir(), f"{dataspec.uuid()}.pkl"
        )
