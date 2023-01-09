from __future__ import annotations

from enum import Enum
from typing import Collection, List, Optional, Protocol

from sarus_data_spec.storage.typing import Storage
import sarus_data_spec.typing as st


class DataspecPrivacyPolicy(Enum):
    WHITE_LISTED = "Result of whitelisted operations"
    DP = "DP estimate"


class QueryManager(Protocol):
    def storage(self) -> Storage:
        ...

    def variant(
        self,
        dataspec: st.DataSpec,
        kind: st.ConstraintKind,
        public_context: List[str],
        privacy_limit: Optional[st.PrivacyLimit],
    ) -> Optional[st.DataSpec]:
        ...

    def variants(self, dataspec: st.DataSpec) -> Collection[st.DataSpec]:
        ...

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
        ...

    def verified_constraints(
        self, dataspec: st.DataSpec
    ) -> List[st.VariantConstraint]:
        """Return the list of VariantConstraints attached to a DataSpec.

        A VariantConstraint attached to a DataSpec means that the DataSpec
        verifies the constraint.
        """
        ...

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
        ...

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
        ...
