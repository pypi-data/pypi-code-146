import pytest

from chalk.streams import KafkaSource


@pytest.fixture
def source():
    return KafkaSource(topic="topic", bootstrap_server="bootstrap-server")


def test_sasl_mechanism_default(source: KafkaSource):
    assert source.sasl_mechanism == "PLAIN"


def test_security_protocol_default(source: KafkaSource):
    assert source.security_protocol == "PLAINTEXT"


def test_cliend_id_prefixdefault(source: KafkaSource):
    assert source.client_id_prefix == "chalk/"


def test_group_id_default(source: KafkaSource):
    assert source.group_id_prefix == "chalk/"
