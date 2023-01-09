from datetime import datetime

from chalk.features import (
    features,
    FeatureTime,
    is_feature_time,
    feature_time,
)


@features
class FTCls:
    id: str
    timestamp: FeatureTime


def test_by_annotation():
    assert is_feature_time(FTCls.timestamp)
    assert not is_feature_time(FTCls.id)


@features
class FTCls1:
    id: str
    ts: datetime


def test_by_naming_convention():
    assert is_feature_time(FTCls1.ts)


@features
class FTCls2:
    id: str
    ts: datetime
    timestamp: datetime = feature_time()


def test_by_feature():
    assert is_feature_time(FTCls2.timestamp)
    assert not is_feature_time(FTCls2.ts)
