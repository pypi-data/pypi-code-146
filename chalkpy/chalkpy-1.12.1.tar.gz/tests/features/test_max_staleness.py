from chalk.features import feature, features, unwrap_feature
from chalk.streams import Windowed, windowed


@features(max_staleness="1d", etl_offline_to_online=True)
class FSWithStaleness:
    parent_id: str
    scalar: int
    windowed_int: Windowed[int] = windowed("10m")

    scalar_override: int = feature(max_staleness="2d", etl_offline_to_online=False)
    windowed_int_override: Windowed[int] = windowed("10m", max_staleness="2d", etl_offline_to_online=False)


def test_assigning_max_staleness_from_class():
    """
    FeatureSet              -> FSWithStaleness
    """

    assert unwrap_feature(FSWithStaleness.scalar).max_staleness == "1d"
    assert unwrap_feature(FSWithStaleness.windowed_int).max_staleness == "1d"
    assert unwrap_feature(FSWithStaleness.windowed_int__600__).max_staleness == "1d"
    assert unwrap_feature(FSWithStaleness.scalar_override).max_staleness == "2d"
    assert unwrap_feature(FSWithStaleness.windowed_int_override).max_staleness == "2d"
    assert unwrap_feature(FSWithStaleness.windowed_int_override__600__).max_staleness == "2d"


def test_assigning_etl_offline_online_from_class():
    """
    FeatureSet              -> FSWithStaleness
    """

    assert unwrap_feature(FSWithStaleness.scalar).etl_offline_to_online == True
    assert unwrap_feature(FSWithStaleness.windowed_int).etl_offline_to_online == True
    assert unwrap_feature(FSWithStaleness.windowed_int__600__).etl_offline_to_online == True
    assert unwrap_feature(FSWithStaleness.scalar_override).etl_offline_to_online == False
    assert unwrap_feature(FSWithStaleness.windowed_int_override).etl_offline_to_online == False
    assert unwrap_feature(FSWithStaleness.windowed_int_override__600__).etl_offline_to_online == False
