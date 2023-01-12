from datetime import datetime

from chalk.features import feature_time, features, unwrap_feature


@features
class FeaturesClassWithoutTimestamp:
    pass


def test_features_class_without_timestamp():
    ts_feature_wrapped = getattr(FeaturesClassWithoutTimestamp, "__chalk_observed_at__")
    ts_feature = unwrap_feature(ts_feature_wrapped)
    assert ts_feature.attribute_name == "__chalk_observed_at__"
    assert ts_feature.name == "__chalk_observed_at__"
    assert ts_feature.namespace == "features_class_without_timestamp"
    assert ts_feature.typ is not None
    assert ts_feature.typ.underlying == datetime
    assert [ts_feature] == FeaturesClassWithoutTimestamp.features
    assert FeaturesClassWithoutTimestamp.__chalk_ts__ is ts_feature


@features
class FeaturesClassWithNamedTs:
    ts: datetime


def test_features_class_with_named_ts():
    ts_feature_wrapped = FeaturesClassWithNamedTs.ts
    ts_feature = unwrap_feature(ts_feature_wrapped)
    assert ts_feature.attribute_name == "ts"
    assert ts_feature.name == "ts"
    assert ts_feature.namespace == "features_class_with_named_ts"
    assert ts_feature.typ is not None
    assert ts_feature.typ.underlying == datetime
    assert [ts_feature] == FeaturesClassWithNamedTs.features
    assert FeaturesClassWithNamedTs.__chalk_ts__ is ts_feature


@features
class FeaturesClassWithCustomTsName:
    ts_custom_name: datetime = feature_time()


def test_features_class_with_custom_ts_name():
    ts_feature_wrapped = FeaturesClassWithCustomTsName.ts_custom_name
    ts_feature = unwrap_feature(ts_feature_wrapped)
    assert ts_feature.attribute_name == "ts_custom_name"
    assert ts_feature.name == "ts_custom_name"
    assert ts_feature.namespace == "features_class_with_custom_ts_name"
    assert ts_feature.typ is not None
    assert ts_feature.typ.underlying == datetime
    assert [ts_feature] == FeaturesClassWithCustomTsName.features
    assert FeaturesClassWithCustomTsName.__chalk_ts__ is ts_feature
