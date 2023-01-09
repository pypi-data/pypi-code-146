from __future__ import annotations

from typing import Collection, List, Optional, cast
import logging

from sarus_data_spec.constants import PEP_TOKEN, VARIANT_UUID
from sarus_data_spec.manager.ops.asyncio.processor import routing
from sarus_data_spec.query_manager.privacy_limit import DeltaEpsilonLimit
from sarus_data_spec.storage.typing import Storage
from sarus_data_spec.variant_constraint import (
    pep_constraint,
    public_constraint,
)
import sarus_data_spec.protobuf as sp
import sarus_data_spec.query_manager.simple_rules as compilation_rules
import sarus_data_spec.typing as st

logger = logging.getLogger(__name__)


class BaseQueryManager:
    def __init__(self, storage: Storage):
        self._storage = storage

    def storage(self) -> Storage:
        return self._storage

    def variant(
        self,
        dataspec: st.DataSpec,
        kind: st.ConstraintKind,
        public_context: List[str],
        privacy_limit: Optional[st.PrivacyLimit],
    ) -> Optional[st.DataSpec]:
        return compilation_rules.compile(
            self, dataspec, kind, public_context, privacy_limit
        )

    def variants(self, dataspec: st.DataSpec) -> Collection[st.DataSpec]:
        """Return all variants attached to a Dataspec."""
        variants_attributes = {
            variant_kind: dataspec.attribute(name=variant_kind)
            for variant_kind in sp.ConstraintKind.DESCRIPTOR.values_by_name
        }
        variants = {
            variant_kind: self.storage().referrable(att[VARIANT_UUID])
            for variant_kind, att in variants_attributes.items()
            if att is not None
        }
        # raise warning if some variants are not found in the storage
        for variant_kind, variant in variants.items():
            if variant is None:
                logger.warning(
                    "Inconsistent storage, found None "
                    f"variant {variant_kind} for dataspec {dataspec}"
                )
        return [
            cast(st.DataSpec, variant)
            for variant in variants.values()
            if variant is not None
        ]

    def verified_constraints(
        self, dataspec: st.DataSpec
    ) -> List[st.VariantConstraint]:
        """Return the list of VariantConstraints attached to a DataSpec.

        A VariantConstraint attached to a DataSpec means that the DataSpec
        verifies the constraint.
        """
        constraints = self.storage().referring(
            dataspec, type_name=sp.type_name(sp.VariantConstraint)
        )
        return cast(List[st.VariantConstraint], list(constraints))

    def verifies(
        self,
        variant_constraint: st.VariantConstraint,
        kind: st.ConstraintKind,
        public_context: Collection[str],
        privacy_limit: Optional[st.PrivacyLimit],
    ) -> bool:
        """Check if the constraint attached to a Dataspec meets requirements.

        This function is useful because comparisons are not straightforwards.
        For instance, a Dataspec might have the variant constraint SYNTHETIC
        attached to it. This synthetic dataspec also verifies the DP constraint
        and the PUBLIC constraint.

        Args:
            variant_constraint: VariantConstraint attached to the Dataspec
            kind: constraint kind to verify compliance with
            public_context: actual current public context
            epsilon: current privacy consumed
        """
        return compilation_rules.verifies(
            query_manager=self,
            variant_constraint=variant_constraint,
            kind=kind,
            public_context=public_context,
            privacy_limit=privacy_limit,
        )

    def is_public(self, dataspec: st.DataSpec) -> bool:
        """Return True if the dataspec is public.

        Some DataSpecs are intrinsically Public, this is the case if they are
        freely available externally, they can be tagged so and will never be
        considered otherwise.

        This function returns True in the following cases:
        - The dataspec is an ML model
        - The dataspec is transformed but all its inputs are public

        This functions creates a VariantConstraint on the DataSpec to cache the
        PUBLIC constraint.
        """
        # TODO fetch real context and epsilon
        public_context: List[str] = []
        privacy_limit = DeltaEpsilonLimit({0.0: 0.0})
        kind = st.ConstraintKind.PUBLIC

        # Does any saved constraint yet verifies that the Dataspec is public
        for constraint in self.verified_constraints(dataspec):
            if self.verifies(constraint, kind, public_context, privacy_limit):
                return True

        # Determine is the Dataspec is public
        if dataspec.is_transformed():
            # Returns true if the DataSpec derives only from public
            args_parents, kwargs_parents = dataspec.parents()
            is_public = all(
                [self.is_public(ds) for ds in args_parents]
                + [self.is_public(ds) for ds in kwargs_parents.values()]
            )
        elif dataspec.prototype() == sp.Scalar:
            scalar = cast(st.Scalar, dataspec)
            if scalar.is_model():
                is_public = True
        else:
            is_public = False

        # save variant constraint
        if is_public:
            public_constraint(dataspec)

        return is_public

    def pep_token(self, dataspec: st.DataSpec) -> Optional[str]:
        """Return a token if the dataspec is PEP, otherwise return None.

        DataSpec.pep_token() returns a PEP token if the dataset is PEP and None
        otherwise. The PEP token is stored in the properties of the
        VariantConstraint. It is a hash initialized with a value when the
        Dataset is protected.

        If a transform does not preserve the PEID then the token is set to None
        If a transform preserves the PEID assignment but changes the rows (e.g.
        sample, shuffle, filter,...) then the token's value is changed If a
        transform does not change the rows (e.g. selecting a column, adding a
        scalar,...) then the token is passed without change

        A Dataspec is PEP if its PEP token is not None. Two PEP Dataspecs are
        aligned (i.e. they have the same number of rows and all their rows have
        the same PEID) if their tokens are equal.
        """
        if dataspec.prototype() == sp.Scalar:
            return None

        dataset = cast(st.Dataset, dataspec)

        # TODO fetch real context and budget
        public_context: List[str] = []
        privacy_limit = DeltaEpsilonLimit({0.0: 0.0})
        kind = st.ConstraintKind.PEP

        # Does any constraint yet verifies that the Dataset is PEP
        for constraint in self.verified_constraints(dataset):
            if self.verifies(constraint, kind, public_context, privacy_limit):
                return constraint.properties()[PEP_TOKEN]

        # Compute the PEP token
        if not dataset.is_transformed():
            return None

        transform = dataset.transform()
        OpClass = routing.get_dataset_op(transform)
        pep_token = OpClass(dataset).pep_token(public_context, privacy_limit)
        if pep_token is not None:
            pep_constraint(
                dataspec=dataset,
                token=pep_token,
                required_context=[],
                privacy_limit=privacy_limit,
            )

        return pep_token
