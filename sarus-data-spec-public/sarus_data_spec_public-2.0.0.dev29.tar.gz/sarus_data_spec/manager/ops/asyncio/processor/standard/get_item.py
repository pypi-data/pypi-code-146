import typing as t

import pyarrow as pa

from sarus_data_spec.arrow.array import convert_record_batch
from sarus_data_spec.bounds import bounds as bounds_builder
from sarus_data_spec.constants import DATASET_SLUGNAME
from sarus_data_spec.dataset import Dataset
from sarus_data_spec.manager.ops.asyncio.processor.standard.standard_op import (  # noqa: E501
    StandardDatasetOp,
)
from sarus_data_spec.manager.ops.asyncio.processor.standard.visitor_selector import (  # noqa : E501
    select_rows,
)
from sarus_data_spec.marginals import marginals as marg_builder
from sarus_data_spec.path import Path
from sarus_data_spec.schema import schema
from sarus_data_spec.size import size as size_builder
import sarus_data_spec.type as sdt
import sarus_data_spec.typing as st


class GetItem(StandardDatasetOp):
    """Computes schema and arrow
    batches for a dataspec transformed by
    a get_item transform
    """

    async def schema(self) -> st.Schema:
        parent_schema = await self.parent_schema()
        path = Path(self.dataset.transform().protobuf().spec.get_item.path)
        sub_types = parent_schema.data_type().sub_types(path)
        assert len(sub_types) == 1
        new_type = sub_types[0]
        # TODO: update foreign_keys/primary_keys in the type
        previous_fields = parent_schema.type().children()
        if 'data' in previous_fields.keys():
            previous_fields['data'] = new_type
            new_type = sdt.Struct(fields=previous_fields)
        return schema(
            self.dataset,
            schema_type=new_type,
            protected_paths=parent_schema.protobuf().protected,
            name=self.dataset.properties().get(DATASET_SLUGNAME, None),
        )

    async def to_arrow(
        self, batch_size: int
    ) -> t.AsyncIterator[pa.RecordBatch]:
        previous_ds = t.cast(Dataset, self.parent())
        path = Path(self.dataset.transform().protobuf().spec.get_item.path)
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
                if 'data' in previous_ds.schema().type().children():
                    old_arrays = array.flatten()
                    array = array.field('data')
                    updated_array = get_items(
                        _type=previous_ds.schema().data_type(),
                        array=array,
                        path=path,
                    )
                    old_arrays[0] = updated_array
                    new_struct = pa.StructArray.from_arrays(
                        old_arrays,
                        names=list(
                            previous_ds.schema().type().children().keys()
                        ),
                    )
                    yield pa.RecordBatch.from_struct_array(new_struct)
                else:
                    updated_array = get_items(
                        _type=previous_ds.schema().data_type(),
                        array=array,
                        path=path,
                    )
                    if isinstance(updated_array, pa.StructArray):
                        yield pa.RecordBatch.from_struct_array(updated_array)
                    else:
                        yield pa.RecordBatch.from_arrays(
                            [updated_array],
                            names=[path.to_strings_list()[0][-1]],
                        )

        return async_generator(
            parent_iter=await previous_ds.async_to_arrow(batch_size=batch_size)
        )

    async def size(self) -> st.Size:
        sizes = await self.parent_size()
        path = Path(self.dataset.transform().protobuf().spec.get_item.path)
        new_stats = sizes.statistics().nodes_statistics(path)
        assert len(new_stats) == 1
        return size_builder(dataset=self.dataset, statistics=new_stats[0])

    async def bounds(self) -> st.Bounds:
        bounds = await self.parent_bounds()
        path = Path(self.dataset.transform().protobuf().spec.get_item.path)
        new_stats = bounds.statistics().nodes_statistics(path)
        assert len(new_stats) == 1
        return bounds_builder(dataset=self.dataset, statistics=new_stats[0])

    async def marginals(self) -> st.Marginals:
        marginals = await self.parent_marginals()
        path = Path(self.dataset.transform().protobuf().spec.get_item.path)
        new_stats = marginals.statistics().nodes_statistics(path)
        assert len(new_stats) == 1
        return marg_builder(dataset=self.dataset, statistics=new_stats[0])


def get_items(array: pa.Array, path: st.Path, _type: st.Type) -> pa.Array:
    """Visitor selecting columns based on the type.
    The idea is that at each level,
    the filter for the array is computed, and for the union,
    we remove the fields that we want to filter among
    the columns
    """

    class ItemSelector(st.TypeVisitor):
        batch_array: pa.Array = array

        def Struct(
            self,
            fields: t.Mapping[str, st.Type],
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:

            if len(path.sub_paths()) > 0:
                sub_path = path.sub_paths()[0]
                self.batch_array = get_items(
                    array=array.field(sub_path.label()),
                    path=sub_path,
                    _type=fields[sub_path.label()],
                )

        def Constrained(
            self,
            type: st.Type,
            constraint: st.Predicate,
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            raise NotImplementedError

        def Optional(
            self,
            type: st.Type,
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            array = self.batch_array.field(path.label())
            if len(path.sub_paths()) == 0:
                self.batch_array = array
            else:
                self.batch_array = get_items(
                    array=array, path=path.sub_paths()[0], _type=type
                )

        def Union(
            self,
            fields: t.Mapping[str, st.Type],
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:

            if len(path.sub_paths()) == 0:
                self.batch_array = array
            else:
                sub_path = path.sub_paths()[0]
                self.batch_array = get_items(
                    array=array.field(sub_path.label()),
                    path=sub_path,
                    _type=fields[sub_path.label()],
                )

        def Array(
            self,
            type: st.Type,
            shape: t.Tuple[int, ...],
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

        def Boolean(
            self, properties: t.Optional[t.Mapping[str, str]] = None
        ) -> None:
            pass

        def Bytes(
            self, properties: t.Optional[t.Mapping[str, str]] = None
        ) -> None:
            pass

        def Unit(
            self, properties: t.Optional[t.Mapping[str, str]] = None
        ) -> None:
            pass

        def Date(
            self,
            format: str,
            min: str,
            max: str,
            base: st.DateBase,
            possible_values: t.Iterable[str],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            pass

        def Time(
            self,
            format: str,
            min: str,
            max: str,
            base: st.TimeBase,
            possible_values: t.Iterable[str],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            pass

        def Datetime(
            self,
            format: str,
            min: str,
            max: str,
            base: st.DatetimeBase,
            possible_values: t.Iterable[str],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            pass

        def Duration(
            self,
            unit: str,
            min: int,
            max: int,
            possible_values: t.Iterable[int],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            pass

        def Enum(
            self,
            name: str,
            name_values: t.Sequence[t.Tuple[str, int]],
            ordered: bool,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            pass

        def Text(
            self,
            encoding: str,
            possible_values: t.Iterable[str],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            pass

        def Hypothesis(
            self,
            *types: t.Tuple[st.Type, float],
            name: t.Optional[str] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            pass

        def Id(
            self,
            unique: bool,
            reference: t.Optional[st.Path] = None,
            base: t.Optional[st.IdBase] = None,
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            pass

        def Integer(
            self,
            min: int,
            max: int,
            base: st.IntegerBase,
            possible_values: t.Iterable[int],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            pass

        def Null(
            self, properties: t.Optional[t.Mapping[str, str]] = None
        ) -> None:
            pass

        def Float(
            self,
            min: float,
            max: float,
            base: st.FloatBase,
            possible_values: t.Iterable[float],
            properties: t.Optional[t.Mapping[str, str]] = None,
        ) -> None:
            pass

    visitor = ItemSelector()
    _type.accept(visitor)
    return visitor.batch_array
