from datetime import datetime

from chalk.features import DataFrame, Feature, feature, feature_time, features, has_many, has_one, unwrap_feature


@features
class UnassignedIdFeatures:
    id: str
    other: str


@features
class UnassignedDecoratedIdFeatures:
    id: str = feature(owner="elliot@chalk.ai")
    other: str


@features
class OtherPrimaryKeyFeatures:
    id: str
    nah_really_this_is_id: str = feature(primary=True)
    other: str


@features
class ExplicitIdFeatures:
    id: str
    other: str


@features
class BogusIdFeature1:
    id: str = has_one(lambda: ExplicitIdFeatures.id == BogusIdFeature1.other)
    other: str


@features
class BogusIdFeature2:
    id: DataFrame[ExplicitIdFeatures] = has_many(lambda: ExplicitIdFeatures.id == BogusIdFeature2.other)
    other: str


@features
class BogusIdFeature3:
    id: datetime = feature_time()
    other: str


@features
class IdIsNotIdFeatures:
    id: str = feature(name="not_id")
    other: str


@features
class NotIdIsIdFeatures:
    not_id: str = feature(name="id")
    other: str


def test_unassigned_assigned():
    assert unwrap_feature(UnassignedIdFeatures.id).primary
    assert not unwrap_feature(UnassignedIdFeatures.other).primary
    assert "id" == UnassignedIdFeatures.__chalk_primary__.name


def test_unassigned_decorated_assigned():
    assert unwrap_feature(UnassignedDecoratedIdFeatures.id).primary
    assert not unwrap_feature(UnassignedDecoratedIdFeatures.other).primary
    assert "id" == UnassignedDecoratedIdFeatures.__chalk_primary__.name


def test_other_primary_key():
    assert not unwrap_feature(OtherPrimaryKeyFeatures.id).primary
    assert unwrap_feature(OtherPrimaryKeyFeatures.nah_really_this_is_id).primary
    assert "nah_really_this_is_id" == OtherPrimaryKeyFeatures.__chalk_primary__.name


def test_explicit_id():
    assert unwrap_feature(ExplicitIdFeatures.id).primary
    assert not unwrap_feature(ExplicitIdFeatures.other).primary
    assert "id" == ExplicitIdFeatures.__chalk_primary__.name


def test_id_is_bogus():
    assert not unwrap_feature(BogusIdFeature1.id).primary
    assert BogusIdFeature1.__chalk_primary__ is None

    assert not unwrap_feature(BogusIdFeature2.id).primary
    assert BogusIdFeature2.__chalk_primary__ is None

    assert isinstance(unwrap_feature(BogusIdFeature3.id), Feature)
    assert not unwrap_feature(BogusIdFeature3.id).primary
    assert BogusIdFeature3.__chalk_primary__ is None


def test_not_id_is_id():
    assert unwrap_feature(NotIdIsIdFeatures.not_id).primary
    assert not unwrap_feature(NotIdIsIdFeatures.other).primary
    assert "id" == NotIdIsIdFeatures.__chalk_primary__.name


def test_id_is_not_id():
    assert not unwrap_feature(IdIsNotIdFeatures.id).primary
    assert not unwrap_feature(IdIsNotIdFeatures.other).primary
    assert IdIsNotIdFeatures.__chalk_primary__ is None
