import random
import typing as t

import pyarrow as pa

from sarus_data_spec.bounds import bounds as bounds_builder
from sarus_data_spec.constants import DATASET_SLUGNAME
from sarus_data_spec.manager.asyncio.utils import async_iter
from sarus_data_spec.manager.ops.asyncio.processor.standard.standard_op import (  # noqa: E501
    StandardDatasetOp,
)
from sarus_data_spec.marginals import marginals as marg_builder
from sarus_data_spec.schema import schema
from sarus_data_spec.size import size as size_builder
import sarus_data_spec.typing as st


class Shuffle(StandardDatasetOp):
    """Computes schema and arrow
    batches for a dataspec transformed by
    a user_settings transform
    """

    async def schema(self) -> st.Schema:
        parent_schema = await self.parent_schema()
        return schema(
            self.dataset,
            schema_type=parent_schema.type(),
            protected_paths=parent_schema.protobuf().protected,
            properties=parent_schema.properties(),
            name=self.dataset.properties().get(DATASET_SLUGNAME, None),
        )

    async def to_arrow(
        self, batch_size: int
    ) -> t.AsyncIterator[pa.RecordBatch]:

        arrow_batches = [
            batch async for batch in await self.parent_to_arrow(batch_size=1)
        ]
        random.shuffle(arrow_batches)
        return async_iter(
            pa.Table.from_batches(arrow_batches).to_batches(
                max_chunksize=batch_size
            )
        )

    async def size(self) -> st.Size:
        sizes = await self.parent_size()
        return size_builder(
            dataset=self.dataset, statistics=sizes.statistics()
        )

    async def bounds(self) -> st.Bounds:
        bounds = await self.parent_bounds()
        return bounds_builder(
            dataset=self.dataset, statistics=bounds.statistics()
        )

    async def marginals(self) -> st.Marginals:
        marginals = await self.parent_marginals()
        return marg_builder(
            dataset=self.dataset, statistics=marginals.statistics()
        )
