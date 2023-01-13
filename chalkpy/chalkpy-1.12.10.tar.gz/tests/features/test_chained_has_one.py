from chalk.features import features, has_one, unwrap_feature
from chalk.features.feature_field import HasOnePathObj


@features
class ExampleFraudOrg:
    uid: str
    org_name: str


@features
class ExampleFraudUser:
    uid: str
    org: ExampleFraudOrg = has_one(lambda: ExampleFraudUser.uid == ExampleFraudOrg.uid)


@features
class ExampleFraudProfile:
    uid: str
    user: ExampleFraudUser = has_one(lambda: ExampleFraudProfile.uid == ExampleFraudUser.uid)


def test_chain():
    referenced_org = unwrap_feature(ExampleFraudProfile.user.org.org_name)

    assert len(referenced_org.path) == 2
    assert isinstance(referenced_org.path[0], HasOnePathObj)
    assert isinstance(referenced_org.path[1], HasOnePathObj)
