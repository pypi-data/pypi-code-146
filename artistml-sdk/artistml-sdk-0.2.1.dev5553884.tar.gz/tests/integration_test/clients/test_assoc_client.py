from artistml_sdk.apis.assoc.v1.assoc_service_pb2 import Assoc
from artistml_sdk.apis.assoc.v1.assoc_service_pb2 import AssocType
from artistml_sdk.apis.common.v1.types_pb2 import CommonOption
from artistml_sdk.clients import AssocClient
from artistml_sdk.gateway import assoc_client
from artistml_sdk.lib import config

assoc_host = config.test.get_val(
    "server",
    "gateway",
    "assoc",
    "host",
)
assoc_port = config.test.get_val(
    "server",
    "gateway",
    "assoc",
    "grpcPort",
)

assoc_client.set_endpoint(endpoint=f"{assoc_host}:{assoc_port}")
client = AssocClient()


def test_assoc():
    from_id = 1
    to_id = 2
    a_type = AssocType.ASSOC_TYPE_CREATED_BY
    resp = client.create_assoc(from_id=from_id, to_id=to_id, a_type=a_type)
    assert resp.details.id > 0
    resp = client.get_assoc(from_id=from_id, to_id=to_id, a_type=a_type)
    assert resp.details.id > 0
    new_a_type = AssocType.ASSOC_TYPE_CREATED_WITH
    resp = client.update_assoc(
        from_id=from_id,
        to_id=to_id,
        a_type=a_type,
        assoc=Assoc(from_id=from_id, to_id=to_id, a_type=new_a_type),
    )
    assert resp.details.id > 0
    resp = client.get_assoc(from_id=from_id, to_id=to_id, a_type=new_a_type)
    assert resp.details.id > 0
    resp = client.count_assoc(from_id=from_id, a_type=a_type)
    assert resp.details != None
    resp = client.list_assoc(common_option=CommonOption(page=1, size=10))
    assert len(resp.details.items) > 0
    resp = client.delete_assoc(from_id=from_id, to_id=to_id, a_type=new_a_type)
    assert resp.details.id > 0
    resp = client.get_assoc(from_id=from_id, to_id=to_id, a_type=new_a_type)
    assert resp.details.id == 0
