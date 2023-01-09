from typing import AsyncIterator, List, Union
import typing as t

import numpy as np
import pyarrow as pa

from sarus_data_spec.constants import DATASET_SLUGNAME
from sarus_data_spec.manager.asyncio.utils import async_iter
from sarus_data_spec.manager.ops.asyncio.processor.standard.standard_op import (  # noqa: E501
    StandardDatasetOp,
)
from sarus_data_spec.schema import schema
import sarus_data_spec.typing as st


class Sample(StandardDatasetOp):
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

        parent_batches = [
            batch async for batch in await self.parent_to_arrow()
        ]
        parent_table = pa.Table.from_batches(parent_batches)

        if (
            self.dataset.transform()
            .protobuf()
            .spec.sample.HasField('fraction')
        ):
            indices = np.random.choice(
                parent_table.num_rows,
                replace=False,
                size=int(
                    self.dataset.transform().protobuf().spec.sample.fraction
                    * parent_table.num_rows
                ),
            )
        else:
            indices = np.random.choice(
                parent_table.num_rows,
                replace=False,
                size=self.dataset.transform().protobuf().spec.sample.size,
            )
        return fast_gather(
            indices=indices,
            batches=parent_table.to_batches(max_chunksize=1000),
            batch_size=batch_size,
        )


# Copied from
# https://github.com/huggingface/datasets/blob/master/src/datasets/table.py
def fast_gather(
    indices: Union[List[int], np.ndarray],
    batches: List[pa.RecordBatch],
    batch_size: int,
) -> AsyncIterator[pa.RecordBatch]:
    """
    Create a pa.Table by gathering the records at the records at the specified
    indices. Should be faster than
    pa.concat_tables(
        table.fast_slice(int(i) % table.num_rows, 1) for i in indices
    )
    since NumPy can compute the binary searches in parallel,
    highly optimized C
    """
    assert len(indices), "Indices must be non-empty"
    offsets: np.ndarray = np.cumsum(
        [0] + [len(b) for b in batches], dtype=np.int64
    )
    batch_indices = np.searchsorted(offsets, indices, side="right") - 1
    # it is important to combine the chunks of the table: if each record batch
    # slice has a length smaller than batch_size, then they will be
    # kept as they are and we will not get batches of size `batch_size`
    return async_iter(
        pa.Table.from_batches(
            [
                batches[batch_idx].slice(i - offsets[batch_idx], 1)
                for batch_idx, i in zip(batch_indices, indices)
            ],
            schema=batches[0].schema,
        )
        .combine_chunks()
        .to_batches(max_chunksize=batch_size)
    )
