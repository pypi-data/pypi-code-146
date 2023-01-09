import dataclasses

from pydantic import BaseModel

from chalk.features import Features, features
from chalk.streams import KafkaSource, KeyedState, stream


@features
class StreamFeatures:
    scalar_feature: str


class KafkaMessage(BaseModel):
    val_a: str


source = KafkaSource(bootstrap_server="bootstrap-server", topic="topic")


@dataclasses.dataclass
class MyState:
    a: int = 4


@stream(source=source)
def fn(message: KafkaMessage, s: KeyedState[MyState]) -> Features[StreamFeatures.scalar_feature]:
    return StreamFeatures(
        scalar_feature=message.val_a,
    )


def test_callable():
    assert fn(KafkaMessage(val_a="hello"), MyState()) == StreamFeatures(scalar_feature="hello")


def test_parsed_source():
    assert fn.source == source
