from datetime import datetime

from chalk.features import feature_time, features, has_one


@features
class NoFunFeatures:
    id: str


@features
class FunFeatures:
    id: str
    nope: str
    single_parent: "NoFunFeatures" = has_one(lambda: FunFeatures.nope == NoFunFeatures.id)
    ts = feature_time()


def test_dictify_features():
    now = datetime.now()
    assert {"fun_features.nope": "hello", "fun_features.ts": now} == dict(FunFeatures(nope="hello", ts=now))
    assert {"fun_features.nope": "hello"} == dict(FunFeatures(nope="hello"))
    assert {"fun_features.nope": "hello"} == dict(FunFeatures(nope="hello", single_parent=NoFunFeatures(id="a")))
    assert {} == dict(FunFeatures())
