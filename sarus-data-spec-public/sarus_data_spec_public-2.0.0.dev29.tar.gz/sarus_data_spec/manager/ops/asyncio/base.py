from __future__ import annotations

import typing as t

import pyarrow as pa

from sarus_data_spec.manager.asyncio.utils import decoupled_async_iter
import sarus_data_spec.typing as st


class BaseDatasetOp:
    def __init__(self, dataset: st.Dataset):
        self.dataset = dataset

    async def schema(self) -> st.Schema:
        """Computes the schema of the dataspec"""
        raise NotImplementedError

    async def to_arrow(
        self, batch_size: int
    ) -> t.AsyncIterator[pa.RecordBatch]:
        raise NotImplementedError

    def pep_token(
        self, public_context: t.List[str], privacy_limit: st.PrivacyLimit
    ) -> t.Optional[str]:
        """Return a token if the output is PEP."""
        raise NotImplementedError

    async def size(self) -> st.Size:
        raise NotImplementedError

    async def bounds(self) -> st.Bounds:
        raise NotImplementedError

    async def marginals(self) -> st.Marginals:
        raise NotImplementedError

    @staticmethod
    async def decoupled_async_iter(
        source: t.AsyncIterator[pa.RecordBatch], buffer_size: int = 1
    ) -> t.AsyncIterator[pa.RecordBatch]:
        return decoupled_async_iter(source=source, buffer_size=buffer_size)

    def is_dp_applicable(self, public_context: t.Collection[str]) -> bool:
        return False

    def dp_transform(self) -> t.Optional[st.Transform]:
        return None


class BaseScalarOp:
    def __init__(self, scalar: st.Scalar):
        self.scalar = scalar

    async def value(self) -> t.Any:
        raise NotImplementedError

    @staticmethod
    async def decoupled_async_iter(
        source: t.AsyncIterator[pa.RecordBatch], buffer_size: int = 1
    ) -> t.AsyncIterator[pa.RecordBatch]:
        return decoupled_async_iter(source=source, buffer_size=buffer_size)

    def is_dp_applicable(self, public_context: t.Collection[str]) -> bool:
        return False

    def dp_transform(self) -> t.Optional[st.Transform]:
        return None
