import hashlib
import importlib
import inspect
import json
import pickle as pkl
import typing as t

import pandas as pd
import pyarrow as pa

from sarus_data_spec.attribute import attach_properties
from sarus_data_spec.config import ROUTING
from sarus_data_spec.constants import PRIVATE_QUERY
from sarus_data_spec.manager.asyncio.utils import async_iter
from sarus_data_spec.manager.ops.asyncio.base import (
    BaseDatasetOp,
    BaseScalarOp,
)
from sarus_data_spec.protobuf.utilities import json as proto_to_json
from sarus_data_spec.transform import external, transform_id
import sarus_data_spec.manager.typing as smt
import sarus_data_spec.typing as st

from .protection_utils import (
    DPImplementation,
    ExternalOpImplementation,
    extract_data_from_pe,
    pandas_merge_pe,
)


class ExternalDatasetOp(BaseDatasetOp):
    def is_dp_applicable(self, public_context: t.Collection[str]) -> bool:
        """Statically check if a DP transform is applicable in this position.

        This verification is common to all dataspecs and is true if:
            - the dataspec is transformed and its transform has an equivalent
            DP transform
            - the DP transform's required PEP arguments are PEP and aligned
            (i.e. same PEP token)
            - other dataspecs arguments are public
        """
        (
            op_implementation,
            serialized_args,
            serialized_kwargs,
        ) = deserialize_external_op(self.dataset)

        args, kwargs = reorganize_arguments(
            self.dataset, *serialized_args, **serialized_kwargs
        )

        dp_implementation = op_implementation.dp_equivalent()
        if dp_implementation is None:
            return False

        pep_args, non_pep_args = group_by_pep(
            dp_implementation, *args, **kwargs
        )

        # All non PEP args should be public of published
        if not all(
            [
                arg.uuid() in public_context or arg.is_public()
                for arg in non_pep_args.values()
            ]
        ):
            return False

        # The PEP arg combination should be allowed
        if set(pep_args.keys()) not in dp_implementation.allowed_pep_args:
            return False

        # All PEP tokens should be equal
        pep_tokens = [arg.pep_token() for arg in pep_args.values()]
        if not all([token == pep_tokens[0] for token in pep_tokens]):
            return False

        return True

    def dp_transform(self) -> t.Optional[st.Transform]:
        """Return the dataspec's DP equivalent transform if existing."""
        (
            op_implementation,
            serialized_args,
            serialized_kwargs,
        ) = deserialize_external_op(self.dataset)

        dp_implementation = op_implementation.dp_equivalent()
        if dp_implementation is None:
            return None

        dp_transform_id = dp_implementation.transform_id
        assert dp_transform_id is not None

        return external(dp_transform_id, *serialized_args, **serialized_kwargs)

    def pep_token(
        self, public_context: t.List[str], privacy_limit: st.PrivacyLimit
    ) -> t.Optional[str]:
        """Return the current dataspec's PEP token."""
        (
            op_implementation,
            serialized_args,
            serialized_kwargs,
        ) = deserialize_external_op(self.dataset)

        transform_args, transform_kwargs = reorganize_arguments(
            self.dataset, *serialized_args, **serialized_kwargs
        )

        if not op_implementation.is_pep_transform():
            return None

        pep_op_implementation = t.cast(
            smt.PEPImplementation, op_implementation
        )
        if len(pep_op_implementation.allowed_pep_args) == 0:
            return None

        pep_args, non_pep_args = group_by_pep(
            pep_op_implementation, *transform_args, **transform_kwargs
        )

        # All non PEP args should be public of published
        if not all(
            [
                arg.uuid() in public_context or arg.is_public()
                for arg in non_pep_args.values()
            ]
        ):
            return None

        # The PEP arg combination should be allowed
        if set(pep_args.keys()) not in pep_op_implementation.allowed_pep_args:
            return None

        # All PEP tokens should be equal
        pep_tokens = [arg.pep_token() for arg in pep_args.values()]
        if not all([token == pep_tokens[0] for token in pep_tokens]):
            return None

        # The result is PEP, now check if it's aligned with the input(s)
        input_token = pep_tokens[0]
        assert input_token is not None
        if pep_op_implementation.is_token_preserving(
            *transform_args, **transform_kwargs
        ):
            output_token = input_token
        else:
            h = hashlib.md5()
            h.update(input_token.encode("ascii"))
            h.update(self.dataset.transform().protobuf().SerializeToString())
            output_token = h.hexdigest()

        return output_token

    async def to_arrow(
        self, batch_size: int
    ) -> t.AsyncIterator[pa.RecordBatch]:

        (
            op_implementation,
            serialized_args,
            serialized_kwargs,
        ) = deserialize_external_op(self.dataset)

        transform_args, transform_kwargs = reorganize_arguments(
            self.dataset, *serialized_args, **serialized_kwargs
        )

        data_args, data_kwargs, pe_candidates = await evaluate_arguments(
            *transform_args, **transform_kwargs
        )

        if self.dataset.is_pep() or isinstance(
            op_implementation, DPImplementation
        ):
            # If we reach this part then there should be only one input PE
            pe = next(iter(pe_candidates), None)
            if pe is None:
                raise ValueError(
                    "The dataset was infered PEP but has no input PE"
                )
            # For now, PE in external ops are only viewed as pd.DataFrames
            if not all([candidate.equals(pe) for candidate in pe_candidates]):
                raise ValueError(
                    "The dataset is PEP but has several differing"
                    " input PE values"
                )

        if isinstance(op_implementation, DPImplementation):
            # We also pass the PE for DP implementations
            data, private_query = await op_implementation.data_fn(
                *data_args, **data_kwargs, pe=pe
            )
            subqueries = [
                proto_to_json(q.protobuf())
                for q in private_query.all_subqueries()
            ]
            attach_properties(
                self.dataset,
                properties={PRIVATE_QUERY: json.dumps(subqueries)},
                name=PRIVATE_QUERY,
            )
        else:
            data = await op_implementation.data_fn(*data_args, **data_kwargs)

        if self.dataset.is_pep():
            # We guarantee that the data.index is a reliable way to trace how
            # the rows were rearranged
            assert pe is not None
            pe = pe.loc[data.index]
        else:
            pe = None

        if isinstance(data, pd.DataFrame):
            table = pandas_merge_pe(data, pe)
            return async_iter(table.to_batches(max_chunksize=batch_size))

        else:
            raise TypeError(f"Cannot convert {type(data)} to Arrow batches.")


class ExternalScalarOp(BaseScalarOp):
    def is_dp_applicable(self, public_context: t.Collection[str]) -> bool:
        """Statically check if a DP transform is applicable in this position.

        This verification is common to all dataspecs and is true if:
            - the dataspec is transformed and its transform has an equivalent
            DP transform
            - the DP transform's required PEP arguments are PEP and aligned
            (i.e. same PEP token)
            - other dataspecs arguments are public
        """
        (
            op_implementation,
            serialized_args,
            serialized_kwargs,
        ) = deserialize_external_op(self.scalar)

        args, kwargs = reorganize_arguments(
            self.scalar, *serialized_args, **serialized_kwargs
        )

        dp_implementation = op_implementation.dp_equivalent()
        if dp_implementation is None:
            return False

        pep_args, non_pep_args = group_by_pep(
            dp_implementation, *args, **kwargs
        )

        # All non PEP args should be public of published
        if not all(
            [
                arg.uuid() in public_context or arg.is_public()
                for arg in non_pep_args.values()
            ]
        ):
            return False

        # The PEP arg combination should be allowed
        if set(pep_args.keys()) not in dp_implementation.allowed_pep_args:
            return False

        # All PEP tokens should be equal
        pep_tokens = [arg.pep_token() for arg in pep_args.values()]
        if not all([token == pep_tokens[0] for token in pep_tokens]):
            return False

        return True

    def dp_transform(self) -> t.Optional[st.Transform]:
        """Return the dataspec's DP equivalent transform if existing."""
        (
            op_implementation,
            serialized_args,
            serialized_kwargs,
        ) = deserialize_external_op(self.scalar)

        dp_implementation = op_implementation.dp_equivalent()
        if dp_implementation is None:
            return None

        dp_transform_id = dp_implementation.transform_id
        assert dp_transform_id is not None

        return external(
            dp_transform_id,
            *serialized_args,
            **serialized_kwargs,
        )

    async def value(self) -> t.Any:

        (
            op_implementation,
            serialized_args,
            serialized_kwargs,
        ) = deserialize_external_op(self.scalar)

        transform_args, transform_kwargs = reorganize_arguments(
            self.scalar, *serialized_args, **serialized_kwargs
        )

        data_args, data_kwargs, pe_candidates = await evaluate_arguments(
            *transform_args, **transform_kwargs
        )

        if isinstance(op_implementation, DPImplementation):
            # If we reach this part then there should be only one input PE
            pe = next(iter(pe_candidates), None)
            if pe is None:
                raise ValueError(
                    "The dataset was infered PEP but has no input PE"
                )
            # For now, PE in external ops are only viewed as pd.DataFrames
            if not all([candidate.equals(pe) for candidate in pe_candidates]):
                raise ValueError(
                    "The dataset is PEP but has several differing"
                    " input PE values"
                )
            # We also pass the PE for DP implementations
            data, private_query = await op_implementation.data_fn(
                *data_args, **data_kwargs, pe=pe
            )
            subqueries = [
                proto_to_json(q.protobuf())
                for q in private_query.all_subqueries()
            ]
            attach_properties(
                self.scalar,
                properties={PRIVATE_QUERY: json.dumps(subqueries)},
                name=PRIVATE_QUERY,
            )
        else:
            data = await op_implementation.data_fn(*data_args, **data_kwargs)

        return data


def group_by_pep(
    op_implementation: smt.ExternalOpImplementation,
    *args: t.Any,
    **kwargs: t.Any,
) -> t.Tuple[t.Dict[str, st.DataSpec], t.Dict[str, st.DataSpec]]:
    """Get Dataspec arguments and split them between PEP and non PEP.

    This also identifies positional arguments by names based on the `data_fn`
    signature.
    """
    # Add name to positional arguments to identify them by their names
    n_args = len(args)
    argument_names = list(
        inspect.signature(op_implementation.data_fn).parameters.keys()
    )
    """
    Example :
    In [1]: def foo(a, b=3):
    ...:     return a+b
    ...:

    In [2]: list(inspect.signature(foo).parameters.keys())
    Out[2]: ['a', 'b']
    """
    for arg_name, arg_val in zip(argument_names[:n_args], args):
        # put all args in kwargs
        kwargs[arg_name] = arg_val

    # Keep only dataspec args and split PEP from non PEP
    dataspec_args = {
        arg_name: arg
        for arg_name, arg in kwargs.items()
        if isinstance(arg, st.DataSpec)
    }
    pep_args = {
        arg_name: arg
        for arg_name, arg in dataspec_args.items()
        if arg.is_pep()
    }
    non_pep_args = {
        arg_name: arg
        for arg_name, arg in dataspec_args.items()
        if arg_name not in pep_args
    }
    return pep_args, non_pep_args


def reorganize_arguments(
    dataspec: st.DataSpec,
    py_args: t.Dict[int, t.Any],
    py_kwargs: t.Dict[str, t.Any],
    ds_args_pos: t.List[int],
) -> t.Tuple:
    """Interleave Python arguments with Dataspec arguments."""
    ds_args, ds_kwargs = dataspec.parents()
    pos_values = {pos: val for pos, val in zip(ds_args_pos, ds_args)}
    kwargs = {**py_kwargs, **ds_kwargs}
    pos_args = {**pos_values, **py_args}
    args = [pos_args[i] for i in range(len(pos_args))]
    return args, kwargs


def transform_implementation(
    transform_id: str,
) -> smt.ExternalOpImplementation:
    """Return the OpImplementation from a Transform ID.

    The mapping is done by the config file.
    """
    library, op_name = transform_id.split(".")
    if op_name not in ROUTING["external"][library]:
        raise NotImplementedError(
            f"Routing: {op_name} not in {list(ROUTING['external'][library].keys())}"  # noqa: E501
        )

    implementation_name = ROUTING["external"][library][op_name]
    module = importlib.import_module(
        f"sarus_data_spec.manager.ops.asyncio.processor.external.{library}"
    )
    op_implementation = getattr(module, implementation_name)

    if not isinstance(op_implementation, smt.ExternalOpImplementation):
        op_implementation = ExternalOpImplementation(op_implementation)

    op_implementation.transform_id = transform_id

    return t.cast(ExternalOpImplementation, op_implementation)


def deserialize_external_op(
    dataspec: st.DataSpec,
) -> t.Tuple[smt.ExternalOpImplementation, t.Any, t.Mapping[str, t.Any]]:
    """Deserialize Python arguments and fetch the op implementation.

    The op implementation can be either a simple function or an
    ExternalOpImplementation instance. If the op is a function,
    it is considered to be the data implementation and
    we instantiate an `ExternalOpImplementation` from this data
    function.
    """
    op_implementation = transform_implementation(
        transform_id(dataspec.transform())
    )
    transform_spec = dataspec.transform().protobuf().spec
    # serialized_args: usually empty
    # serialized_kwargs: usually {py_args, py_kwargs, ds_args_pos}
    serialized_args = pkl.loads(transform_spec.external.arguments)
    serialized_kwargs = pkl.loads(transform_spec.external.named_arguments)

    return op_implementation, serialized_args, serialized_kwargs


async def evaluate_arguments(
    *args: t.Any, **kwargs: t.Any
) -> t.Tuple[t.List[t.Any], t.Dict[str, t.Any], t.List[t.Any]]:
    """Evaluate sarus dataspecs and extract the PE.

    Compute the value of Dataspec arguments. Extract all the protections and
    return them in a list.
    """
    data_pe_args = [await extract_data_from_pe(arg) for arg in args]
    data_args = [data for data, _ in data_pe_args]
    pe_args = [pe for _, pe in data_pe_args]

    data_pe_kwargs = {
        name: await extract_data_from_pe(arg) for name, arg in kwargs.items()
    }
    data_kwargs = {name: data for name, (data, _) in data_pe_kwargs.items()}
    pe_kwargs = [pe for _, pe in data_pe_kwargs.values()]

    pe_candidates = list(filter(lambda x: x is not None, pe_args + pe_kwargs))

    return data_args, data_kwargs, pe_candidates
