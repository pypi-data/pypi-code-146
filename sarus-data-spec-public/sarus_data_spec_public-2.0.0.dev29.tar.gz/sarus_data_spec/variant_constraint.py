from __future__ import annotations

from typing import List, Optional, Type, cast
import json

from sarus_data_spec.base import Referring
from sarus_data_spec.constants import PEP_TOKEN, PRIVACY_LIMIT
from sarus_data_spec.query_manager.privacy_limit import DeltaEpsilonLimit
import sarus_data_spec.protobuf as sp
import sarus_data_spec.typing as st


class VariantConstraint(Referring[sp.VariantConstraint]):
    def __init__(
        self, protobuf: sp.VariantConstraint, store: bool = True
    ) -> None:
        self._referred = {protobuf.dataspec}
        super().__init__(protobuf=protobuf, store=store)

    def prototype(self) -> Type[sp.VariantConstraint]:
        """Return the type of the underlying protobuf."""
        return sp.VariantConstraint

    def constraint_kind(self) -> st.ConstraintKind:
        return st.ConstraintKind(self.protobuf().constraint_kind)

    def required_context(self) -> List[str]:
        return list(self.protobuf().required_context)

    def privacy_limit(self) -> Optional[st.PrivacyLimit]:
        """Instantiate the privacy limit from the protobuf properties."""
        dump = self.protobuf().properties.get(PRIVACY_LIMIT, None)
        if dump is None:
            return None

        # in JSON keys are converted to str, we reconvert to float here
        data_epsilon_dict = {float(k): v for k, v in json.loads(dump).items()}
        return DeltaEpsilonLimit(data_epsilon_dict)

    def dataspec(self) -> st.DataSpec:
        return cast(
            st.DataSpec, self.storage().referrable(self.protobuf().dataspec)
        )


# Builders


def public_constraint(dataspec: st.DataSpec) -> VariantConstraint:
    """Create a variant constraint specifying a dataspec is Public."""
    return VariantConstraint(
        sp.VariantConstraint(
            dataspec=dataspec.uuid(),
            constraint_kind=sp.ConstraintKind.PUBLIC,
        )
    )


def dp_constraint(
    dataspec: st.DataSpec,
    required_context: List[str],
    privacy_limit: st.PrivacyLimit,
) -> VariantConstraint:
    """Create a variant constraint specifying a dataspec is DP."""
    return VariantConstraint(
        sp.VariantConstraint(
            dataspec=dataspec.uuid(),
            constraint_kind=sp.ConstraintKind.DP,
            required_context=required_context,
            properties={
                PRIVACY_LIMIT: json.dumps(privacy_limit.delta_epsilon_dict()),
            },
        )
    )


def pep_constraint(
    dataspec: st.DataSpec,
    token: str,
    required_context: List[str],
    privacy_limit: st.PrivacyLimit,
) -> VariantConstraint:
    """Create a variant constraint specifying a dataspec is PEP."""
    return VariantConstraint(
        sp.VariantConstraint(
            dataspec=dataspec.uuid(),
            constraint_kind=sp.ConstraintKind.PEP,
            required_context=required_context,
            properties={
                PRIVACY_LIMIT: json.dumps(privacy_limit.delta_epsilon_dict()),
                PEP_TOKEN: token,
            },
        )
    )


def syn_constraint(
    dataspec: st.DataSpec,
    required_context: List[str] = [],
) -> VariantConstraint:
    """Create a variant constraint specifying a dataspec is synthetic."""
    return VariantConstraint(
        sp.VariantConstraint(
            dataspec=dataspec.uuid(),
            constraint_kind=sp.ConstraintKind.SYNTHETIC,
            required_context=required_context,
        )
    )
