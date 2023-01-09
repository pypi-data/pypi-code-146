import typing as t
import warnings

import pyarrow as pa

import sarus_data_spec.typing as st

try:
    from sarus_synthetic_data.synthetic_generator.generator import (
        SyntheticGenerator,
    )

except ModuleNotFoundError:
    warnings.warn(
        'sarus-synthetic-data Module not found, synthetic data operations not '
        'available '
    )

from sarus_data_spec.constants import DATASET_SLUGNAME, SYNTHETIC_TASK
from sarus_data_spec.dataset import Dataset

try:
    from sarus_data_spec.manager.ops.asyncio.source.query_builder import (
        synthetic_parameters,
    )
except ModuleNotFoundError:
    warnings.warn(
        "synthetic_parameters not found, "
        "synthetic data operations not available "
    )
from sarus_data_spec.scalar import Scalar
from sarus_data_spec.schema import schema

from .standard_op import StandardDatasetOp, StandardScalarOp

MAX_SIZE = 1e6  # TODO: in sarus_data_spec.constants ?


def convert_array_to_table(
    schema_type: st.Type, arrow_data: pa.array
) -> pa.Array:
    """Given a PyArrow array, returns a correctly-defined Table."""

    class ArrayToTable(st.TypeVisitor):
        """Handles both configuration: a dataset as a Struct or as an Union."""

        result = None

        def Struct(
            self,
            fields: t.Mapping[str, st.Type],
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            names = list(fields.keys())
            self.result = pa.Table.from_arrays(
                arrays=arrow_data.flatten(), names=names
            )

        def Union(
            self,
            fields: t.Mapping[str, st.Type],
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            names = list(fields.keys())
            names.append("field_selected")
            self.result = pa.Table.from_arrays(
                arrays=arrow_data.flatten(), names=names
            )

        def Null(
            self, properties: t.Optional[t.Mapping[str, str]] = None
        ) -> None:
            raise NotImplementedError

        def Unit(
            self, properties: t.Optional[t.Mapping[str, str]] = None
        ) -> None:
            raise NotImplementedError

        def Boolean(
            self, properties: t.Optional[t.Mapping[str, str]] = None
        ) -> None:
            raise NotImplementedError

        def Id(
            self,
            unique: bool,
            reference: t.Optional[st.Path] = None,
            base: t.Optional[st.IdBase] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

        def Integer(
            self,
            min: int,
            max: int,
            base: st.IntegerBase,
            possible_values: t.Iterable[int],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

        def Enum(
            self,
            name: str,
            name_values: t.Sequence[t.Tuple[str, int]],
            ordered: bool,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

        def Float(
            self,
            min: float,
            max: float,
            base: st.FloatBase,
            possible_values: t.Iterable[float],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

        def Text(
            self,
            encoding: str,
            possible_values: t.Iterable[str],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

        def Bytes(
            self, properties: t.Optional[t.Mapping[str, str]] = None
        ) -> None:
            raise NotImplementedError

        def Optional(
            self,
            type: st.Type,
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

        def List(
            self,
            type: st.Type,
            max_size: int,
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

        def Array(
            self,
            type: st.Type,
            shape: t.Tuple[int, ...],
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

        def Datetime(
            self,
            format: str,
            min: str,
            max: str,
            base: st.DatetimeBase,
            possible_values: t.Iterable[str],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

        def Time(
            self,
            format: str,
            min: str,
            max: str,
            base: st.TimeBase,
            possible_values: t.Iterable[str],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

        def Date(
            self,
            format: str,
            min: str,
            max: str,
            base: st.DateBase,
            possible_values: t.Iterable[str],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

        def Duration(
            self,
            unit: str,
            min: int,
            max: int,
            possible_values: t.Iterable[int],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

        def Constrained(
            self,
            type: st.Type,
            constraint: st.Predicate,
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

        def Hypothesis(
            self,
            *types: t.Tuple[st.Type, float],
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

    visitor = ArrayToTable()
    schema_type.accept(visitor)
    return visitor.result


async def async_iter_arrow(
    iterator: t.Iterator[pa.RecordBatch],
) -> t.AsyncIterator[pa.RecordBatch]:
    """Async generator from the synthetic data iterator."""
    for batch in iterator:
        yield batch
    return


class Synthetic(StandardDatasetOp):
    """Create a Synthetic op class for is_pep."""

    def pep_token(
        self, public_context: t.List[str], privacy_limit: st.PrivacyLimit
    ) -> t.Optional[str]:
        # TODO add pep token when the synthetic data is actually protected
        return None

    async def to_arrow(
        self, batch_size: int
    ) -> t.AsyncIterator[pa.RecordBatch]:
        dataset = self.dataset
        parents, parents_dict = dataset.parents()

        # Forcing the marginals to be computed first
        parent = t.cast(Dataset, parents[0])
        _ = await parent.manager().async_marginals(parent)

        # Budget
        budget_param = parents_dict['sd_budget']
        budget = t.cast(
            t.Tuple[float, float],
            await dataset.manager().async_value(t.cast(Scalar, budget_param)),
        )

        # Generator params
        generator_params = await synthetic_parameters(
            dataset, sd_budget=budget, task=SYNTHETIC_TASK
        )
        # Links computation
        _ = await self.dataset.manager().async_links(self.dataset)
        # compute
        generator = SyntheticGenerator(dataset, generator_params)
        dataset_schema = await dataset.manager().async_schema(dataset)
        datatype = dataset_schema.type()
        sample = generator.sample()
        table = convert_array_to_table(datatype, sample)
        return async_iter_arrow(table.to_batches(max_chunksize=batch_size))

    async def schema(self) -> st.Schema:
        parent_schema = await self.parent_schema()
        return schema(
            self.dataset,
            schema_type=parent_schema.data_type(),
            properties=parent_schema.properties(),
            name=self.dataset.properties().get(DATASET_SLUGNAME, None),
        )


class SamplingRatios(StandardScalarOp):
    """Computes the sampling ratios for the SD
    of the dataspec given the total budget"""

    async def value(self) -> t.Any:
        dataset = t.cast(st.Dataset, self.parent())
        out = {}
        for table_path in (await self.parent_schema()).tables():
            sizes = await dataset.manager().async_size(dataset)
            assert sizes
            stat = sizes.statistics().nodes_statistics(table_path)[0]
            out[table_path] = min(1, MAX_SIZE / stat.size())
        return out
