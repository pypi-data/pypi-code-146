from datetime import datetime

from chalk.client.client_impl import _expand_scalar_features_shallow
from chalk.features import DataFrame, feature_time, features, has_many, has_one


@features
class Ankle:
    id: int
    foot_id: int


@features
class Foot:
    id: int
    is_flat: bool
    person_id: int
    ts: datetime = feature_time()
    ankle: Ankle = has_one(lambda: Ankle.foot_id == Foot.id)


@features
class Person:
    id: int
    name: str
    best_foot_id: int
    best_foot: Foot = has_one(lambda: Foot.id == Person.best_foot_id)
    feet: DataFrame[Foot] = has_many(lambda: Person.id == Foot.person_id)


def _expand(*items):
    ans = set()
    for x in items:
        ans.update(_expand_scalar_features_shallow(x))
    return ans


def test_expand_features():
    assert _expand(Person) == {"person.id", "person.name", "person.best_foot_id"}
    assert _expand(Ankle) == {"ankle.id", "ankle.foot_id"}
    assert _expand(Foot) == {"foot.id", "foot.is_flat", "foot.person_id"}


def test_expand_has_ones():
    assert _expand(Foot.ankle) == {"foot.ankle.id", "foot.ankle.foot_id"}
    assert _expand(Person.best_foot.ankle) == {"person.best_foot.ankle.id", "person.best_foot.ankle.foot_id"}
    assert _expand(Foot.ankle, Foot) == {
        "foot.ankle.id",
        "foot.ankle.foot_id",
        "foot.id",
        "foot.is_flat",
        "foot.person_id",
    }
    assert _expand(Person, Person.best_foot) == {
        "person.id",
        "person.name",
        "person.best_foot_id",
        "person.best_foot.id",
        "person.best_foot.is_flat",
        "person.best_foot.person_id",
    }
    assert _expand(Person, Person.best_foot, Person.best_foot.ankle) == {
        "person.id",
        "person.name",
        "person.best_foot_id",
        "person.best_foot.id",
        "person.best_foot.is_flat",
        "person.best_foot.person_id",
        "person.best_foot.ankle.id",
        "person.best_foot.ankle.foot_id",
    }
