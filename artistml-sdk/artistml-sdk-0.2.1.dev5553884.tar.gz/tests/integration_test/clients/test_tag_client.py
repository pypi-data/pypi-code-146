import random

from artistml_sdk.clients import TagClient
from artistml_sdk.gateway import tag_client
from artistml_sdk.lib import config

tag_host = config.test.get_val(
    "server",
    "gateway",
    "tag",
    "host",
)
tag_port = config.test.get_val(
    "server",
    "gateway",
    "tag",
    "grpcPort",
)

tag_client.set_endpoint(endpoint=f"{tag_host}:{tag_port}")
client = TagClient()


def test_create_tag():
    name = "ksice" + str(random.randint(1, 10))
    resp = client.create_tag(name, "huaji", "red", None)
    assert resp.details.id > 0
    id = resp.details.id
    resp = client.get_tag(resp.details.id)
    assert resp.details.id == resp.details.id
    resp = client.list_tag()
    assert len(resp.details.items) > 0
    resp = client.list_tag(name=name)
    assert len(resp.details.items) > 0
    resp = client.delete_tag(id)
    assert resp.details.id > 0


# resp = client.get_tag(resp.details.id)
