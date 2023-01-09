import hashlib
import typing as t

import pyarrow as pa

from sarus_data_spec.dataset import Dataset
from sarus_data_spec.manager.ops.asyncio.base import (
    BaseDatasetOp,
    BaseScalarOp,
)
from sarus_data_spec.scalar import Scalar
import sarus_data_spec.typing as st


class StandardDatasetOp(BaseDatasetOp):
    """Object that executes first routing among ops between
    transformed/source and processor
    """

    def pep_token(
        self, public_context: t.List[str], privacy_limit: st.PrivacyLimit
    ) -> t.Optional[str]:
        """By default we implement that the transform inherits the PEP status
        but changes the PEP token."""
        parent_token = self.parent().pep_token()
        if parent_token is None:
            return None

        transform = self.dataset.transform()
        h = hashlib.md5()
        h.update(parent_token.encode("ascii"))
        h.update(transform.protobuf().SerializeToString())

        return h.hexdigest()

    def parents(self) -> t.List[st.DataSpec]:
        return parents(self.dataset)

    def parent(self, kind: str = 'dataset') -> t.Union[st.Dataset, st.Scalar]:
        return parent(self.dataset, kind=kind)

    async def parent_to_arrow(
        self, batch_size: int = 10000
    ) -> t.AsyncIterator[pa.RecordBatch]:
        parent = self.parent(kind='dataset')
        assert isinstance(parent, Dataset)
        parent_iterator = await parent.manager().async_to_arrow(
            parent, batch_size=batch_size
        )
        return await self.decoupled_async_iter(parent_iterator)

    async def parent_schema(self) -> st.Schema:
        parent = self.parent(kind='dataset')
        assert isinstance(parent, Dataset)
        return await parent.manager().async_schema(parent)

    async def parent_value(self) -> t.Any:
        parent = self.parent(kind='scalar')
        assert isinstance(parent, Scalar)
        return await parent.manager().async_value(parent)

    async def parent_size(self) -> st.Size:
        parent = self.parent(kind='dataset')
        assert isinstance(parent, Dataset)
        return await parent.manager().async_size(parent)

    async def parent_bounds(self) -> st.Bounds:
        parent = self.parent(kind='dataset')
        assert isinstance(parent, Dataset)
        return await parent.manager().async_bounds(parent)

    async def parent_marginals(self) -> st.Marginals:
        parent = self.parent(kind='dataset')
        assert isinstance(parent, Dataset)
        return await parent.manager().async_marginals(parent)


class StandardScalarOp(BaseScalarOp):
    def parent(self, kind: str = 'dataset') -> st.DataSpec:
        return parent(self.scalar, kind=kind)

    def parents(self) -> t.List[st.DataSpec]:
        return parents(self.scalar)

    async def parent_to_arrow(
        self, batch_size: int = 10000
    ) -> t.AsyncIterator[pa.RecordBatch]:
        parent = self.parent(kind='dataset')
        assert isinstance(parent, Dataset)
        parent_iterator = await parent.manager().async_to_arrow(
            parent, batch_size=batch_size
        )
        return await self.decoupled_async_iter(parent_iterator)

    async def parent_schema(self) -> st.Schema:
        parent = self.parent(kind='dataset')
        assert isinstance(parent, Dataset)
        return await parent.manager().async_schema(parent)

    async def parent_value(self) -> t.Any:
        parent = self.parent(kind='scalar')
        assert isinstance(parent, Scalar)
        return await parent.manager().async_value(parent)


def parent(dataspec: st.DataSpec, kind: str) -> t.Union[st.Dataset, st.Scalar]:
    pars = parents(dataspec)
    if kind == 'dataset':
        parent: t.Union[t.List[Scalar], t.List[Dataset]] = [
            element for element in pars if isinstance(element, Dataset)
        ]
    else:
        parent = [element for element in pars if isinstance(element, Scalar)]
    assert len(parent) == 1
    return parent[0]


def parents(dataspec: st.DataSpec) -> t.List[st.DataSpec]:
    parents_args, parents_kwargs = dataspec.parents()
    parents_args.extend(parents_kwargs.values())
    return parents_args
