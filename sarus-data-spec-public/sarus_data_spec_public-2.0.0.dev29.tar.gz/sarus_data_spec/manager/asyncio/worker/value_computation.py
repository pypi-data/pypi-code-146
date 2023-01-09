import logging
import traceback
import typing as t

from sarus_data_spec import typing as st
from sarus_data_spec.constants import SCALAR_TASK
from sarus_data_spec.manager.asyncio.worker.worker_computation import (
    WorkerComputation,
)
from sarus_data_spec.scalar import Scalar
import sarus_data_spec.status as stt

logger = logging.getLogger(__name__)


class ValueComputation(WorkerComputation[t.Any]):
    """Class responsible for handling the computation
    of scalars."""

    task_name = SCALAR_TASK

    async def read_ready_result(
        self,
        dataspec: st.DataSpec,
        properties: t.Mapping[str, str],
        **kwargs: t.Any,
    ) -> t.Any:
        return await self.manager().async_value_op(
            scalar=t.cast(Scalar, dataspec)
        )

    async def prepare(self, dataspec: st.DataSpec) -> None:
        try:
            logger.debug(f'STARTED SCALAR {dataspec.uuid()}')
            await self.manager().async_prepare_parents(dataspec)
        except Exception:
            stt.error(
                dataspec=dataspec,
                manager=self.manager(),
                task=self.task_name,
                properties={"message": traceback.format_exc()},
            )
        else:
            logging.debug(f'FINISHED SCALAR {dataspec.uuid()}')
            stt.ready(
                dataspec=dataspec,
                manager=self.manager(),
                task=self.task_name,
            )
