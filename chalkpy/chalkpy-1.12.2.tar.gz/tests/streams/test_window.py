from typing import Any, List, cast

import pytest
from pydantic import BaseModel
from typing_extensions import TypeGuard

from chalk import OnlineResolver, online
from chalk.features import DataFrame, Feature, Features, feature, features, has_one, unwrap_feature
from chalk.streams import KafkaSource, Windowed, stream, windowed


@features
class GrandchildWindow:
    id: str
    grandchildfeat: Windowed[str] = windowed("10m", "20m", max_staleness="1h")


@features
class ChildWindow:
    id: str
    childfeat: Windowed[str] = windowed("10m", "20m", max_staleness="1h")
    grand: GrandchildWindow = has_one(lambda: ChildWindow.id == GrandchildWindow.id)


@features
class StreamFeaturesWindow:
    uid: str = feature(primary=True)
    scalar_feature: Windowed[str] = windowed("10m", "20m", max_staleness="1h")
    scalar_feature_2: Windowed[str] = windowed("10m", "20m", max_staleness="1h")
    basic: str

    child_id: str
    child: ChildWindow = has_one(lambda: StreamFeaturesWindow.child_id == ChildWindow.id)


@features
class WindowType:
    uid: str = feature(primary=True)
    str_window: Windowed[str] = windowed("10m")
    int_window: Windowed[int] = windowed("10m")


@online
def with_children(
    r: StreamFeaturesWindow.scalar_feature(window="10m"),
    r1: StreamFeaturesWindow.child.childfeat["20m"],
    r2: StreamFeaturesWindow.child.grand.grandchildfeat("10m"),
) -> StreamFeaturesWindow.basic:
    print(r, r2, r1)
    return ""


def test_windowed_underlying_type():
    assert unwrap_feature(WindowType.str_window).typ.underlying._kind == str
    assert unwrap_feature(WindowType.int_window).typ.underlying._kind == int


def test_has_one_windows():
    assert resolver(with_children).inputs[0].root_fqn == "stream_features_window.scalar_feature__600__"
    assert resolver(with_children).inputs[1].root_fqn == "stream_features_window.child.childfeat__1200__"
    assert resolver(with_children).inputs[2].root_fqn == "stream_features_window.child.grand.grandchildfeat__600__"


class KafkaMessage(BaseModel):
    val_a: str


s = KafkaSource(bootstrap_server="bootstrap-server", topic="topic")


class TopicMessage(BaseModel):
    val_a: str
    val_a: str
    val_a: str


@stream(source=s)
def fn(
    message: List[TopicMessage],
) -> Features[StreamFeaturesWindow.uid, StreamFeaturesWindow.scalar_feature, StreamFeaturesWindow.scalar_feature_2]:
    return StreamFeaturesWindow(
        uid="123",
        scalar_feature="xyz",
        scalar_feature_2="abc",
    )


def resolver(x: Any) -> TypeGuard[OnlineResolver]:
    return cast(OnlineResolver, x)


@online
def accessing_via_brackets(r: StreamFeaturesWindow.scalar_feature["10m"]) -> StreamFeaturesWindow.basic:
    pass


def test_missing_window_error_message():
    with pytest.raises(TypeError) as e:

        @online
        def accessing_via_brackets(r: StreamFeaturesWindow.scalar_feature["40m"]) -> StreamFeaturesWindow.basic:
            pass

    assert str(e.value) == (
        "Unsupported window duration '40m' for 'stream_features_window.scalar_feature'. Durations '600s', '1200s' are supported."
    )


def test_windowed_inputs():
    assert resolver(accessing_via_brackets).inputs[0].fqn == "stream_features_window.scalar_feature__600__"
    assert resolver(with_children).inputs[0].fqn == "stream_features_window.scalar_feature__600__"


def test_windowed_durations_are_set():
    unwrapped = unwrap_feature(StreamFeaturesWindow.scalar_feature)
    assert isinstance(unwrapped, Feature)
    assert unwrapped.is_windowed
    assert not unwrapped.is_windowed_pseudofeature
    assert list(unwrapped.window_durations) == [600, 1200]
    with pytest.raises(ValueError):
        getattr(unwrapped, "window_duration")


def test_windowed_pseudofeature_duration_is_set():
    unwrapped = unwrap_feature(StreamFeaturesWindow.scalar_feature["10m"])
    assert isinstance(unwrapped, Feature)
    assert not unwrapped.is_windowed
    assert unwrapped.is_windowed_pseudofeature
    assert len(unwrapped.window_durations) == 0
    assert unwrapped.window_duration == 600


def test_resolver_requiring_all_windows():
    with pytest.raises(ValueError):

        @online
        def badboi(r: StreamFeaturesWindow.scalar_feature) -> StreamFeaturesWindow.basic:
            pass


def test_require_whole_thing():
    with pytest.raises(ValueError):

        @online
        def badboi(r: StreamFeaturesWindow.scalar_feature) -> StreamFeaturesWindow.basic:
            pass


def test_no_type_annotation_window_error():
    with pytest.raises(TypeError) as e:

        @features
        class BadWindow:
            a = windowed("10m")

    assert str(e.value) == "Windowed feature 'bad_window.a' is missing an annotation, like 'Windowed[str]'"


def test_missing_bucketes():
    with pytest.raises(TypeError) as e:

        @features
        class BadWindow:
            a: Windowed[int]

    assert (
        str(e.value)
        == "Windowed feature 'bad_window.a' is missing windows. To create a windowed feature, use 'a: Windowed[int] = windowed('10m', '30m')."
    )


def test_no_stream_features_from_online():

    with pytest.raises(TypeError):

        @online
        def online_resolver_stream() -> StreamFeaturesWindow.scalar_feature:
            pass

    with pytest.raises(TypeError):

        @online
        def online_df_stream() -> DataFrame[StreamFeaturesWindow.uid, StreamFeaturesWindow.scalar_feature]:
            pass


@features
class ContinuousFeatureClass:
    c_feat: Windowed[int] = windowed("10m", mode="continuous")
    t_feat: Windowed[int] = windowed("10m", mode="tumbling")


def test_window_mode():
    assert ContinuousFeatureClass.c_feat["10m"]._chalk_feature._window_mode == "continuous"
    assert ContinuousFeatureClass.t_feat["10m"]._chalk_feature._window_mode == "tumbling"


def test_streaming_resolvers_do_not_specify_windows():
    with pytest.raises(TypeError):

        @stream(source=s)
        def stream_resolver_scalar() -> StreamFeaturesWindow.uid["10m"]:
            pass

    with pytest.raises(TypeError):

        @stream(source=s)
        def stream_df_resolver() -> DataFrame[StreamFeaturesWindow.uid["10m"]]:
            pass
