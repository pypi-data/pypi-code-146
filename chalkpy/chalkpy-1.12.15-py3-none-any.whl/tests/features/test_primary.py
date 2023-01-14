from chalk.features import Primary, feature, features, is_primary


@features
class PrimaryCls:
    myid: Primary[str]


@features
class PrimaryCls2:
    myid: Primary[str] = feature(max_staleness="3d")
    id: str


def test_primary():
    assert is_primary(PrimaryCls.myid)
    assert is_primary(PrimaryCls2.myid)
    assert not is_primary(PrimaryCls2.id)
