from typing import AsyncIterator
import logging
import typing as t

import pyarrow as pa

from sarus_data_spec.manager.ops.asyncio.base import BaseScalarOp
import sarus_data_spec.typing as st

from .model import Model
from .privacy_params import PrivacyParams
from .random_seed import RandomSeed

logger = logging.getLogger(__name__)
try:
    from sarus_data_spec.manager.ops.asyncio.source.sql_source import SourceSQL
except ModuleNotFoundError:
    logger.info(
        "sqlalquemy not installed, source SQL operations not available."
    )

try:
    from sarus_data_spec.manager.ops.asyncio.source.csv.arrow import (
        csv_to_arrow,
    )
    from sarus_data_spec.manager.ops.asyncio.source.csv.schema import (
        csv_schema,
    )
except ModuleNotFoundError:
    logger.info("CSV package not found, source CSV operations not available.")


def get_scalar_op(scalar: st.Scalar) -> t.Type[BaseScalarOp]:
    if scalar.is_model():
        return Model
    elif scalar.is_random_seed():
        return RandomSeed
    elif scalar.is_privacy_params():
        return PrivacyParams
    else:
        raise NotImplementedError(f"Source scalar for {scalar}")


class SourceScalar(BaseScalarOp):
    async def value(self) -> t.Any:
        OpClass = get_scalar_op(self.scalar)
        return await OpClass(self.scalar).value()


async def source_dataset_to_arrow(
    dataset: st.Dataset, batch_size: int
) -> AsyncIterator[pa.RecordBatch]:
    if dataset.is_file():
        file_format = dataset.protobuf().spec.file.format
        if file_format == "csv":
            return csv_to_arrow(dataset, batch_size=batch_size)
        else:
            raise NotImplementedError(f"File format {file_format}")

    elif dataset.protobuf().spec.HasField('sql'):
        return await SourceSQL(dataset=dataset).to_arrow(batch_size=batch_size)
    else:
        source_type = dataset.protobuf().spec.WhichOneof('spec')
        raise NotImplementedError(f"Source {source_type}")


async def source_dataset_schema(dataset: st.Dataset) -> st.Schema:
    if dataset.protobuf().spec.HasField('sql'):
        return await SourceSQL(dataset=dataset).schema()
    elif dataset.is_file():
        file_format = dataset.protobuf().spec.file.format
        if file_format == "csv":
            return await csv_schema(dataset)
        else:
            raise NotImplementedError(f"File format {file_format}")
    else:
        raise NotImplementedError
