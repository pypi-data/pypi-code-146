from datetime import datetime

from chalk.features import Features, feature_time, features, has_one, online, unwrap_feature
from chalk.features.feature_field import HasOnePathObj


@features
class HomeFeaturesChainedFeatureTime:
    home_id: str
    address: str
    price: int
    sq_ft: int
    homeowner: "Homeowner" = has_one(lambda: Homeowner.home_id == HomeFeaturesChainedFeatureTime.home_id)


@features
class Homeowner:
    fullname: str
    home_id: str
    ts: datetime = feature_time()


@online
def get_home_data(
    hid: HomeFeaturesChainedFeatureTime.home_id, dd: HomeFeaturesChainedFeatureTime.homeowner.ts
) -> Features[HomeFeaturesChainedFeatureTime.price, HomeFeaturesChainedFeatureTime.sq_ft]:
    return HomeFeaturesChainedFeatureTime(
        price=200_000,
        sq_ft=2_000,
    )


def test_chain():
    ts = unwrap_feature(HomeFeaturesChainedFeatureTime.homeowner.ts)
    assert len(ts.path) == 1
    assert isinstance(ts.path[0], HasOnePathObj)
