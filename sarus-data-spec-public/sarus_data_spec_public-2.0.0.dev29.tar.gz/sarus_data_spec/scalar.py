from __future__ import annotations

from typing import (
    Any,
    Collection,
    Dict,
    List,
    Optional,
    Set,
    Tuple,
    Type,
    cast,
)
import json
import pickle as pkl

from sarus_data_spec.base import Referring
from sarus_data_spec.constants import PRIVATE_QUERY
from sarus_data_spec.protobuf.utilities import dejson
from sarus_data_spec.transform import Transform
import sarus_data_spec.protobuf as sp
import sarus_data_spec.typing as st

try:
    from sarus_differential_privacy.protobuf.private_query_pb2 import (
        PrivateQuery,
    )
except ModuleNotFoundError:
    pass  # warning raised in typing.py


class Scalar(Referring[sp.Scalar]):
    """A python class to describe scalars"""

    def __init__(self, protobuf: sp.Scalar, store: bool = True) -> None:
        if protobuf.spec.HasField("transformed"):
            transformed = protobuf.spec.transformed
            self._referred = {
                transformed.transform,
                *transformed.arguments,
                *list(transformed.named_arguments.values()),
            }

        super().__init__(protobuf=protobuf, store=store)

    def prototype(self) -> Type[sp.Scalar]:
        """Return the type of the underlying protobuf."""
        return sp.Scalar

    def name(self) -> str:
        return self._protobuf.name

    def doc(self) -> str:
        return self._protobuf.doc

    def spec(self) -> str:
        return str(self._protobuf.spec.WhichOneof('spec'))

    def is_transformed(self) -> bool:
        """Is the scalar composed."""
        return self._protobuf.spec.HasField("transformed")

    def is_remote(self) -> bool:
        """Is the dataspec a remotely defined dataset."""
        return self.manager().is_remote(self)

    def is_model(self) -> bool:
        """Is the scalar a model."""
        return self._protobuf.spec.HasField("model")

    def is_privacy_params(self) -> bool:
        """Is the scalar privacy parameters."""
        return self._protobuf.spec.HasField("privacy_params")

    def is_random_seed(self) -> bool:
        """Is the scalar a random seed."""
        return self._protobuf.spec.HasField("random_seed")

    def is_pep(self) -> bool:
        """Is the scalar PEP."""
        return False

    def pep_token(self) -> Optional[str]:
        """Returns the scalar PEP token."""
        return None

    def is_public(self) -> bool:
        """Is the scalar public."""
        return self.manager().query_manager().is_public(self)

    def status(self, task_name: str) -> Optional[st.Status]:
        return self.manager().status(self, task_name)

    def transform(self) -> st.Transform:
        return cast(
            st.Transform,
            self.storage().referrable(
                self.protobuf().spec.transformed.transform
            ),
        )

    def parents(
        self,
    ) -> Tuple[List[st.DataSpec], Dict[str, st.DataSpec]]:
        if not self.is_transformed():
            return list(), dict()

        args_id = self._protobuf.spec.transformed.arguments
        kwargs_id = self._protobuf.spec.transformed.named_arguments

        args_parents = [
            cast(st.DataSpec, self.storage().referrable(uuid))
            for uuid in args_id
        ]
        kwargs_parents = {
            name: cast(st.DataSpec, self.storage().referrable(uuid))
            for name, uuid in kwargs_id.items()
        }

        return args_parents, kwargs_parents

    def sources(self) -> Set[st.Dataset]:
        """Returns the set of non-transformed datasets that are parents
        of the current dataset"""

        class Sources(st.Visitor):
            visited: Set[st.DataSpec] = set()
            results: Set[st.Dataset] = set()

            def transformed(
                self,
                visited: st.DataSpec,
                transform: st.Transform,
                *arguments: st.DataSpec,
                **named_arguments: st.DataSpec,
            ) -> None:
                if visited not in self.visited:
                    for argument in arguments:
                        argument.accept(self)
                    for _, argument in named_arguments.items():
                        argument.accept(self)
                    self.visited.add(visited)

            def other(self, visited: st.DataSpec) -> None:
                if visited.prototype() == sp.Dataset:
                    dataset = cast(st.Dataset, visited)
                    self.results.add(dataset)

        visitor = Sources()
        self.accept(visitor)
        return visitor.results

    def variant(
        self,
        kind: st.ConstraintKind,
        public_context: List[str] = [],
        privacy_limit: Optional[st.PrivacyLimit] = None,
    ) -> Optional[st.DataSpec]:
        return (
            self.manager()
            .query_manager()
            .variant(self, kind, public_context, privacy_limit)
        )

    def variants(self) -> Collection[st.DataSpec]:
        return self.manager().query_manager().variants(self)

    def private_queries(self) -> List[PrivateQuery]:
        """Return the list of PrivateQueries used in a Dataspec's transform.

        It represents the privacy loss associated with the current computation.

        It can be used by Sarus when a user (Access object) reads a DP dataspec
        to update its accountant. Note that Private Query objects are generated
        with a random uuid so that even if they are submitted multiple times to
        an account, they are only accounted once (ask @cgastaud for more on
        accounting)."""
        attribute = self.attribute(name=PRIVATE_QUERY)
        if attribute is None:
            return []

        private_query_str = attribute[PRIVATE_QUERY]
        return [
            cast(PrivateQuery, dejson(q))
            for q in json.loads(private_query_str)
        ]

    def value(self) -> st.DataSpecValue:
        return self.manager().value(self)

    async def async_value(self) -> st.DataSpecValue:
        return await self.manager().async_value(self)

    # A Visitor acceptor
    def accept(self, visitor: st.Visitor) -> None:
        visitor.all(self)
        if self.is_transformed():
            visitor.transformed(
                self,
                cast(
                    Transform,
                    self.storage().referrable(
                        self._protobuf.spec.transformed.transform
                    ),
                ),
                *(
                    cast(Scalar, self.storage().referrable(arg))
                    for arg in self._protobuf.spec.transformed.arguments
                ),
                **{
                    name: cast(Scalar, self.storage().referrable(arg))
                    for name, arg in self._protobuf.spec.transformed.named_arguments.items()  # noqa: E501
                },
            )
        else:
            visitor.other(self)

    def dot(self) -> str:
        """return a graphviz representation of the scalar"""

        class Dot(st.Visitor):
            visited: Set[st.DataSpec] = set()
            nodes: Dict[str, Tuple[str, str]] = {}
            edges: Dict[Tuple[str, str], str] = {}

            def transformed(
                self,
                visited: st.DataSpec,
                transform: st.Transform,
                *arguments: st.DataSpec,
                **named_arguments: st.DataSpec,
            ) -> None:
                if visited not in self.visited:
                    if visited.prototype() == sp.Dataset:
                        self.nodes[visited.uuid()] = (
                            visited.name(),
                            "Dataset",
                        )
                    else:
                        self.nodes[visited.uuid()] = (visited.name(), "Scalar")

                    if not visited.is_remote():
                        for argument in arguments:
                            self.edges[
                                (argument.uuid(), visited.uuid())
                            ] = transform.name()
                            argument.accept(self)
                        for _, argument in named_arguments.items():
                            self.edges[
                                (argument.uuid(), visited.uuid())
                            ] = transform.name()
                            argument.accept(self)
                    self.visited.add(visited)

            def other(self, visited: st.DataSpec) -> None:
                if visited.prototype() == sp.Dataset:
                    self.nodes[visited.uuid()] = (
                        visited.name(),
                        "Dataset",
                    )
                else:
                    self.nodes[visited.uuid()] = (visited.name(), "Scalar")

        visitor = Dot()
        self.accept(visitor)
        result = 'digraph {'
        for uuid, (label, node_type) in visitor.nodes.items():
            shape = "polygon" if node_type == "Scalar" else "ellipse"
            result += (
                f'\n"{uuid}" [label="{label} ({uuid[:2]})", shape={shape}];'
            )
        for (u1, u2), label in visitor.edges.items():
            result += f'\n"{u1}" -> "{u2}" [label="{label} ({uuid[:2]})"];'
        result += '}'
        return result

    def attribute(self, name: str) -> Optional[st.Attribute]:
        return self.manager().attribute(name=name, dataspec=self)


# Builders
def model(
    model_class: sp.Scalar.Model.ModelClass.V, *args: Any, **kwargs: Any
) -> Scalar:
    return Scalar(
        sp.Scalar(
            name=sp.Scalar.Model.ModelClass.Name(model_class),
            spec=sp.Scalar.Spec(
                model=sp.Scalar.Model(
                    model_class=model_class,
                    arguments=pkl.dumps(args),
                    named_arguments=pkl.dumps(kwargs),
                )
            ),
        )
    )


def privacy_budget(privacy_limit: st.PrivacyLimit) -> Scalar:
    delta_epsilon_dict = privacy_limit.delta_epsilon_dict()
    return Scalar(
        sp.Scalar(
            name='privacy_budget',
            spec=sp.Scalar.Spec(
                privacy_params=sp.Scalar.PrivacyParameters(
                    points=[
                        sp.Scalar.PrivacyParameters.Point(
                            epsilon=epsilon, delta=delta
                        )
                        for delta, epsilon in delta_epsilon_dict.items()
                    ]
                )
            ),
        )
    )


def random_seed(value: int) -> Scalar:
    return Scalar(
        sp.Scalar(
            name='seed',
            spec=sp.Scalar.Spec(random_seed=sp.Scalar.RandomSeed(value=value)),
        )
    )


class Visitor:
    """A visitor class for Scalar"""

    def all(self, visited: Scalar) -> None:
        return

    def transformed(
        self,
        visited: Scalar,
        transform: Transform,
        *arguments: Scalar,
        **named_arguments: Scalar,
    ) -> None:
        return

    def other(self, visited: Scalar) -> None:
        return
