from time import time_ns
from typing import Collection, Dict, List, Optional, Tuple, cast
import logging

from sarus_data_spec.attribute import attach_properties
from sarus_data_spec.constants import VARIANT_UUID
from sarus_data_spec.context import global_context
from sarus_data_spec.dataset import transformed
from sarus_data_spec.manager.ops.asyncio.processor import routing
from sarus_data_spec.query_manager.typing import QueryManager
from sarus_data_spec.scalar import privacy_budget
from sarus_data_spec.variant_constraint import (
    dp_constraint,
    public_constraint,
    syn_constraint,
)
import sarus_data_spec.protobuf as sp
import sarus_data_spec.typing as st

ArgStruct = Tuple[List[int], List[str]]
logger = logging.getLogger(__name__)


def flatten_args(
    args: List[st.DataSpec], kwargs: Dict[str, st.DataSpec]
) -> Tuple[List[st.Dataset], List[st.Scalar], ArgStruct]:
    """Split args and kwargs into Datasets and Scalars."""
    flat_args = args + list(kwargs.values())
    ds_args = [
        cast(st.Dataset, arg)
        for arg in flat_args
        if arg.prototype() == sp.Dataset
    ]
    sc_args = [
        cast(st.Scalar, arg)
        for arg in flat_args
        if arg.prototype() == sp.Scalar
    ]

    ds_idx = [
        i for i, arg in enumerate(flat_args) if arg.prototype() == sp.Dataset
    ]
    sc_idx = [
        i for i, arg in enumerate(flat_args) if arg.prototype() == sp.Scalar
    ]
    idx = ds_idx + sc_idx
    struct = (idx, list(kwargs.keys()))

    return ds_args, sc_args, struct


def nest_args(
    ds_args: List[st.DataSpec],
    sc_args: List[st.DataSpec],
    struct: ArgStruct,
) -> Tuple[List[st.DataSpec], Dict[str, st.DataSpec]]:
    """Nest Datasets and Scalars into args and kwargs."""
    idx, keys = struct
    all_args = ds_args + sc_args
    flat_args = [all_args[idx.index(i)] for i in range(len(idx))]
    n_args = len(flat_args) - len(keys)
    args = flat_args[:n_args]
    kwargs = {key: val for key, val in zip(keys, flat_args[n_args:])}
    return args, kwargs


def attach_variant(
    original: st.DataSpec,
    variant: st.DataSpec,
    kind: st.ConstraintKind,
) -> None:
    sp_kind = sp.ConstraintKind.Value(kind.name)
    attach_properties(
        original,
        properties={
            # TODO deprecated in SDS >= 2.0.0 -> use only VARIANT_UUID
            sp.ConstraintKind.Name(sp_kind): variant.uuid(),
            VARIANT_UUID: variant.uuid(),
        },
        name=sp.ConstraintKind.Name(sp_kind),
    )


def verifies(
    query_manager: QueryManager,
    variant_constraint: st.VariantConstraint,
    kind: st.ConstraintKind,
    public_context: Collection[str],
    privacy_limit: Optional[st.PrivacyLimit],
) -> bool:
    if kind == st.ConstraintKind.PUBLIC:
        return verifies_public(variant_constraint=variant_constraint)

    elif kind == st.ConstraintKind.SYNTHETIC:
        return verifies_synthetic(variant_constraint=variant_constraint)

    elif kind == st.ConstraintKind.DP:
        return verifies_dp(
            query_manager=query_manager,
            variant_constraint=variant_constraint,
            public_context=public_context,
            privacy_limit=privacy_limit,
        )

    else:  # kind == st.ConstraintKind.PEP:
        return verifies_pep(
            query_manager=query_manager,
            variant_constraint=variant_constraint,
            public_context=public_context,
            privacy_limit=privacy_limit,
        )


def verifies_public(variant_constraint: st.VariantConstraint) -> bool:
    return variant_constraint.constraint_kind() == st.ConstraintKind.PUBLIC


def verifies_synthetic(variant_constraint: st.VariantConstraint) -> bool:
    return variant_constraint.constraint_kind() in [
        st.ConstraintKind.PUBLIC,
        st.ConstraintKind.SYNTHETIC,
    ]


def verifies_pep(
    query_manager: QueryManager,
    variant_constraint: st.VariantConstraint,
    public_context: Collection[str],
    privacy_limit: Optional[st.PrivacyLimit],
) -> bool:
    """If we attached a PEP constraint to a dataspec then it is PEP.

    NB: for now we don't check the context nor the privacy limit
    """
    return variant_constraint.constraint_kind() == st.ConstraintKind.PEP


def verifies_dp(
    query_manager: QueryManager,
    variant_constraint: st.VariantConstraint,
    public_context: Collection[str],
    privacy_limit: Optional[st.PrivacyLimit],
) -> bool:
    if privacy_limit is None:
        raise ValueError(
            "Input privacy limit required when checking against DP."
        )

    kind = variant_constraint.constraint_kind()
    if kind in [st.ConstraintKind.PUBLIC, st.ConstraintKind.SYNTHETIC]:
        return True

    elif kind == st.ConstraintKind.DP:
        constraint_privacy_limit = variant_constraint.privacy_limit()
        if constraint_privacy_limit is None:
            raise ValueError(
                "Found a DP constraint without a privacy limit "
                "when checking against DP."
            )

        return cast(
            bool,
            privacy_limit.delta_epsilon_dict()
            == constraint_privacy_limit.delta_epsilon_dict(),
        )

    else:
        return False


def compile(
    query_manager: QueryManager,
    dataspec: st.DataSpec,
    kind: st.ConstraintKind,
    public_context: List[str],
    privacy_limit: Optional[st.PrivacyLimit],
) -> Optional[st.DataSpec]:
    """Returns a compliant Node or None."""

    if kind == st.ConstraintKind.SYNTHETIC:
        variant, _ = compile_synthetic(
            query_manager,
            dataspec,
            public_context,
        )
        return variant

    if privacy_limit is None:
        raise ValueError(
            "Privacy limit must be defined for PEP or DP compilation"
        )

    if kind == st.ConstraintKind.DP:
        variant, _ = compile_dp(
            query_manager,
            dataspec,
            public_context=public_context,
            privacy_limit=privacy_limit,
        )
        return variant

    elif kind == st.ConstraintKind.PEP:
        raise NotImplementedError("PEP compilation")

    else:
        raise ValueError(
            f"Privacy policy {kind} compilation not implemented yet"
        )


def compile_synthetic(
    query_manager: QueryManager,
    dataspec: st.DataSpec,
    public_context: Collection[str],
) -> Tuple[st.DataSpec, Collection[str]]:
    # Current dataspec verifies the constraint?
    for constraint in query_manager.verified_constraints(dataspec):
        if query_manager.verifies(
            constraint,
            st.ConstraintKind.SYNTHETIC,
            public_context,
            privacy_limit=None,
        ):
            return dataspec, public_context

    # Current dataspec has a variant that verifies the constraint?
    for variant in dataspec.variants():
        if variant is None:
            logger.info(f"Found a None variant for dataspec {dataspec.uuid()}")
            continue
        for constraint in query_manager.verified_constraints(variant):
            if query_manager.verifies(
                constraint,
                st.ConstraintKind.SYNTHETIC,
                public_context,
                privacy_limit=None,
            ):
                return variant, public_context

    if dataspec.prototype() == sp.Dataset:
        dataset = cast(st.Dataset, dataspec)
        # TODO remove this constraint once we have the whole
        # graph for a remote DataSpec
        if not dataspec.is_remote() and dataset.is_synthetic():
            syn_constraint(
                dataspec=dataspec,
                required_context=list(public_context),
            )
            return dataset, list(public_context)

    if not dataspec.is_remote() and dataspec.is_transformed():
        transform = dataspec.transform()
        args, kwargs = dataspec.parents()
        ds_args, sc_args, struct = flatten_args(args, kwargs)
        ds_syn_args_context = [
            compile_synthetic(query_manager, parent, public_context)
            for parent in ds_args
        ]
        sc_syn_args_context = [
            compile_synthetic(query_manager, parent, public_context)
            for parent in sc_args
        ]

        if len(ds_syn_args_context) > 0:
            ds_syn_args, ds_contexts = zip(*ds_syn_args_context)
        else:
            ds_syn_args, ds_contexts = [], ([],)
        if len(sc_syn_args_context) > 0:
            sc_syn_args, sc_contexts = zip(*sc_syn_args_context)
        else:
            sc_syn_args, sc_contexts = [], ([],)
        new_context = list(set(sum(ds_contexts + sc_contexts, [])))
        args, kwargs = nest_args(
            cast(List[st.DataSpec], list(ds_syn_args)),
            cast(List[st.DataSpec], list(sc_syn_args)),
            struct,
        )
        syn_variant = cast(
            st.DataSpec,
            transformed(
                transform,
                *args,
                dataspec_type=sp.type_name(dataspec.prototype()),
                dataspec_name=None,
                **kwargs,
            ),
        )
        syn_constraint(
            dataspec=syn_variant, required_context=list(public_context)
        )
        attach_variant(dataspec, syn_variant, kind=st.ConstraintKind.SYNTHETIC)
        return syn_variant, new_context

    # Source (non transformed) dataset, we always
    # raise an error, the synthetic dataset is created
    # separately
    if dataspec.prototype() == sp.Dataset:
        raise TypeError(
            'Source Dataset cannot'
            'be compiled to Synthetic, a variant'
            'should have been created earlier'
        )

    elif dataspec.prototype() == sp.Scalar:
        scalar = cast(st.Scalar, dataspec)
        assert scalar.is_model()
        new_context = list(public_context) + [scalar.uuid()]
        public_constraint(dataspec=scalar)
        return scalar, new_context

    raise ValueError("Uncaught compilation case.")


def compile_dp(
    query_manager: QueryManager,
    dataspec: st.DataSpec,
    public_context: Collection[str],
    privacy_limit: st.PrivacyLimit,
) -> Tuple[st.DataSpec, Collection[str]]:
    """Simple DP compilation.

    Only check the dataspec's parents, do not go further up in the graph.
    """
    # Current dataspec verifies the constraint?
    for constraint in query_manager.verified_constraints(dataspec):
        if query_manager.verifies(
            variant_constraint=constraint,
            kind=st.ConstraintKind.DP,
            public_context=public_context,
            privacy_limit=privacy_limit,
        ):
            return dataspec, public_context

    # Current dataspec has a variant that verifies the constraint?
    for variant in dataspec.variants():
        for constraint in query_manager.verified_constraints(variant):
            if query_manager.verifies(
                variant_constraint=constraint,
                kind=st.ConstraintKind.DP,
                public_context=public_context,
                privacy_limit=privacy_limit,
            ):
                return variant, public_context

    if not dataspec.is_transformed():
        return compile_synthetic(query_manager, dataspec, public_context)

    transform = dataspec.transform()
    if dataspec.prototype() == sp.Dataset:
        dataset = cast(st.Dataset, dataspec)
        DatasetOpClass = routing.get_dataset_op(transform)
        is_dp_applicable = DatasetOpClass(dataset).is_dp_applicable(
            public_context
        )
        dp_transform = DatasetOpClass(dataset).dp_transform()
    else:
        scalar = cast(st.Scalar, dataspec)
        ScalarOpClass = routing.get_scalar_op(transform)
        is_dp_applicable = ScalarOpClass(scalar).is_dp_applicable(
            public_context
        )
        dp_transform = ScalarOpClass(scalar).dp_transform()

    if not is_dp_applicable:
        return compile_synthetic(query_manager, dataspec, public_context)

    # Create the DP variant
    assert dp_transform is not None
    budget = privacy_budget(privacy_limit)
    seed = global_context().generate_seed(salt=time_ns())
    args, kwargs = dataspec.parents()
    dp_variant = cast(
        st.DataSpec, dp_transform(*args, **kwargs, budget=budget, seed=seed)
    )
    dp_constraint(
        dataspec=dp_variant,
        required_context=list(public_context),
        privacy_limit=privacy_limit,
    )
    attach_variant(
        original=dataspec,
        variant=dp_variant,
        kind=st.ConstraintKind.DP,
    )

    return dp_variant, public_context
