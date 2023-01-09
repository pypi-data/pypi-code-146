import typing as t

import pyarrow as pa

from sarus_data_spec.arrow.array import convert_record_batch
from sarus_data_spec.bounds import bounds as bounds_builder
from sarus_data_spec.constants import DATASET_SLUGNAME, OPTIONAL_VALUE
from sarus_data_spec.manager.ops.asyncio.processor.standard.standard_op import (  # noqa: E501
    StandardDatasetOp,
)
from sarus_data_spec.manager.ops.asyncio.processor.standard.visitor_selector import (  # noqa: E501
    filter_primary_keys,
    select_rows,
    update_fks,
)
from sarus_data_spec.marginals import marginals as marg_builder
from sarus_data_spec.schema import schema
from sarus_data_spec.size import size as size_builder
import sarus_data_spec.statistics as sds
import sarus_data_spec.type as sdt
import sarus_data_spec.typing as st


class Filter(StandardDatasetOp):
    """Computes schema and arrow
    batches for a dataspec transformed by
    a user_settings transform
    """

    async def schema(self) -> st.Schema:
        parent_schema = await self.parent_schema()
        new_type = sdt.Type(
            self.dataset.transform().protobuf().spec.filter.filter
        )
        new_type = update_fks(
            curr_type=new_type, original_type=new_type  # type:ignore
        )
        old_properties = parent_schema.properties()

        if 'primary_keys' in old_properties.keys():
            new_pks = filter_primary_keys(
                old_properties['primary_keys'],
                new_type,
            )
            old_properties['primary_keys'] = new_pks  # type:ignore

        # VERY UGLY SHOULD BE REMOVED WHEN WE HAVE PROTECTED TYPE
        previous_fields = parent_schema.type().children()
        if 'data' in previous_fields.keys():
            previous_fields['data'] = new_type.data_type()
            new_type = sdt.Struct(fields=previous_fields)
        return schema(
            self.dataset,
            schema_type=new_type,
            protected_paths=parent_schema.protobuf().protected,
            properties=old_properties,
            name=self.dataset.properties().get(DATASET_SLUGNAME, None),
        )

    async def to_arrow(
        self, batch_size: int
    ) -> t.AsyncIterator[pa.RecordBatch]:

        schema = await self.dataset.manager().async_schema(
            dataset=self.dataset
        )
        parent_schema = await self.parent_schema()

        async def async_generator(
            parent_iter: t.AsyncIterator[pa.RecordBatch],
        ) -> t.AsyncIterator[pa.RecordBatch]:
            async for batch in parent_iter:
                # TODO: what follows is really ugly and is necessary
                # because we do not have a proper type for the
                # protected entity, it will be removed when we
                # switch to that formalism

                array = convert_record_batch(
                    record_batch=batch, _type=parent_schema.type()
                )
                # VERY UGLY SHOULD BE REMOVED WHEN WE HAVE PROTECTED TYPE
                if 'data' in parent_schema.type().children():
                    old_arrays = array.flatten()
                    array = array.field('data')
                    updated_array, filter_indices = select_rows(
                        schema.data_type(),
                        array,
                    )
                    old_arrays[0] = updated_array
                    new_struct = pa.StructArray.from_arrays(
                        old_arrays,
                        names=list(parent_schema.type().children().keys()),
                    )
                    yield pa.RecordBatch.from_struct_array(
                        new_struct.filter(filter_indices)
                    )
                else:
                    updated_array, filter_indices = select_rows(
                        schema.data_type(),
                        array,
                    )
                    yield pa.RecordBatch.from_struct_array(
                        updated_array.filter(filter_indices)
                    )

        return async_generator(
            parent_iter=await self.parent_to_arrow(batch_size=batch_size)
        )

    async def size(self) -> st.Size:
        schema = await self.dataset.manager().async_schema(self.dataset)
        sizes = await self.parent_size()
        new_stats = update_statistics(
            stats=sizes.statistics(), new_type=schema.data_type()
        )
        return size_builder(dataset=self.dataset, statistics=new_stats)

    async def bounds(self) -> st.Bounds:
        schema = await self.dataset.manager().async_schema(self.dataset)
        bounds = await self.parent_bounds()
        new_stats = update_statistics(
            stats=bounds.statistics(), new_type=schema.data_type()
        )
        return bounds_builder(dataset=self.dataset, statistics=new_stats)

    async def marginals(self) -> st.Marginals:
        schema = await self.dataset.manager().async_schema(self.dataset)
        marginals = await self.parent_marginals()
        new_stats = update_statistics(
            stats=marginals.statistics(), new_type=schema.data_type()
        )
        return marg_builder(dataset=self.dataset, statistics=new_stats)


def update_statistics(
    stats: st.Statistics, new_type: st.Type
) -> st.Statistics:
    """Visitor to update recursively the stats object via the new_type.
    Sub_statistics whose corresponding type is absent in new_type are removed.
    """

    class Updater(st.StatisticsVisitor):
        result = stats

        def Struct(
            self,
            fields: t.Mapping[str, st.Statistics],
            size: int,
            multiplicity: float,
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            # filter does not affect structs
            children_type = new_type.children()
            new_struct = sds.Struct(
                fields={
                    fieldname: update_statistics(
                        fieldstat, children_type[fieldname]
                    )
                    for fieldname, fieldstat in self.result.children().items()
                },
                size=size,
                multiplicity=multiplicity,
                name=name,
                properties=self.result.properties(),
            )
            self.result = new_struct

        def Union(
            self,
            fields: t.Mapping[str, st.Statistics],
            size: int,
            multiplicity: float,
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            children_type = new_type.children()
            children_stat = self.result.children()
            new_fields = {
                fieldname: update_statistics(
                    children_stat[fieldname], fieldtype
                )
                for fieldname, fieldtype in children_type.items()
            }
            self.result = sds.Union(
                fields=new_fields,
                size=size,
                multiplicity=multiplicity,
                name=name if name is not None else 'Union',
                properties=self.result.properties(),
            )

        def Optional(
            self, statistics: st.Statistics, size: int, multiplicity: float
        ) -> None:
            self.result = sds.Optional(
                statistics=update_statistics(
                    self.result.children()[OPTIONAL_VALUE],
                    new_type.children()[OPTIONAL_VALUE],
                ),
                size=size,
                multiplicity=multiplicity,
                properties=self.result.properties(),
            )

        def Null(self, size: int, multiplicity: float) -> None:
            pass

        def Unit(self, size: int, multiplicity: float) -> None:
            pass

        def Boolean(
            self,
            size: int,
            multiplicity: float,
            probabilities: t.Optional[t.List[float]] = None,
            names: t.Optional[t.List[bool]] = None,
            values: t.Optional[t.List[int]] = None,
        ) -> None:
            pass

        def Id(self, size: int, multiplicity: float) -> None:
            pass

        def Integer(
            self,
            size: int,
            multiplicity: float,
            min_value: int,
            max_value: int,
            probabilities: t.Optional[t.List[float]] = None,
            values: t.Optional[t.List[int]] = None,
        ) -> None:
            pass

        def Enum(
            self,
            size: int,
            multiplicity: float,
            probabilities: t.Optional[t.List[float]] = None,
            names: t.Optional[t.List[str]] = None,
            values: t.Optional[t.List[float]] = None,
            name: str = 'Enum',
        ) -> None:
            pass

        def Float(
            self,
            size: int,
            multiplicity: float,
            min_value: float,
            max_value: float,
            probabilities: t.Optional[t.List[float]] = None,
            values: t.Optional[t.List[float]] = None,
        ) -> None:
            pass

        def Text(
            self,
            size: int,
            multiplicity: float,
            min_value: int,
            max_value: int,
            example: str = '',
            probabilities: t.Optional[t.List[float]] = None,
            values: t.Optional[t.List[int]] = None,
        ) -> None:
            pass

        def Bytes(self, size: int, multiplicity: float) -> None:
            pass

        def List(
            self,
            statistics: st.Statistics,
            size: int,
            multiplicity: float,
            min_value: int,
            max_value: int,
            name: str = 'List',
            probabilities: t.Optional[t.List[float]] = None,
            values: t.Optional[t.List[int]] = None,
        ) -> None:
            raise NotImplementedError

        def Array(
            self,
            statistics: st.Statistics,
            size: int,
            multiplicity: float,
            min_values: t.Optional[t.List[float]] = None,
            max_values: t.Optional[t.List[float]] = None,
            name: str = 'Array',
            probabilities: t.Optional[t.List[t.List[float]]] = None,
            values: t.Optional[t.List[t.List[float]]] = None,
        ) -> None:
            raise NotImplementedError

        def Datetime(
            self,
            size: int,
            multiplicity: float,
            min_value: int,
            max_value: int,
            probabilities: t.Optional[t.List[float]] = None,
            values: t.Optional[t.List[int]] = None,
        ) -> None:
            pass

        def Date(
            self,
            size: int,
            multiplicity: float,
            min_value: int,
            max_value: int,
            probabilities: t.Optional[t.List[float]] = None,
            values: t.Optional[t.List[int]] = None,
        ) -> None:
            pass

        def Time(
            self,
            size: int,
            multiplicity: float,
            min_value: int,
            max_value: int,
            probabilities: t.Optional[t.List[float]] = None,
            values: t.Optional[t.List[int]] = None,
        ) -> None:
            pass

        def Duration(
            self,
            size: int,
            multiplicity: float,
            min_value: int,
            max_value: int,
            probabilities: t.Optional[t.List[float]] = None,
            values: t.Optional[t.List[int]] = None,
        ) -> None:
            pass

        def Constrained(
            self, statistics: st.Statistics, size: int, multiplicity: float
        ) -> None:
            raise NotImplementedError

    visitor = Updater()
    stats.accept(visitor)
    return visitor.result
