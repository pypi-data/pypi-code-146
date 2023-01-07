from artistml_sdk.clients import EchoClient


def test_greeting_client():
    assert EchoClient.echo() == "hello!"
