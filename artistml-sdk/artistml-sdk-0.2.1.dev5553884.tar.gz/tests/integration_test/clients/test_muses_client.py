import tempfile
from copy import deepcopy

from kfp import compiler
from kfp import dsl

from artistml_sdk.apis.common.v1.types_pb2 import CommonFilter
from artistml_sdk.apis.common.v1.types_pb2 import CommonOption
from artistml_sdk.apis.muses.v1.method_pb2 import Method
from artistml_sdk.apis.muses.v1.run_pb2 import Run
from artistml_sdk.clients import MusesClient
from artistml_sdk.clients import TagClient
from artistml_sdk.gateway import kfp_client
from artistml_sdk.gateway import muses_client
from artistml_sdk.gateway import tag_client
from artistml_sdk.lib import config
from artistml_sdk.lib import write_message

muses_host = config.test.get_val(
    "server",
    "gateway",
    "muses",
    "host",
)
muses_port = config.test.get_val(
    "server",
    "gateway",
    "muses",
    "grpcPort",
)
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

kfp_host = config.test.get_val(
    "kfp",
    "host",
)
kfp_port = config.test.get_val(
    "kfp",
    "port",
)

kfp_client.set_endpoint(endpoint=f"http://{kfp_host}:{kfp_port}")
muses_client.set_endpoint(endpoint=f"{muses_host}:{muses_port}")
tag_client.set_endpoint(endpoint=f"{tag_host}:{tag_port}")
client = MusesClient()
tag_client_ = TagClient()

cmplr = compiler.Compiler()


@dsl.component
def addition_component(num1: int, num2: int) -> int:
    return num1 + num2


@dsl.pipeline(name='addition-pipeline-ksice')
def addition_pipeline(a: int, b: int, c: int = 10):
    add_task_1 = addition_component(num1=a, num2=b)
    add_task_2 = addition_component(num1=add_task_1.output, num2=c)


def test_create_component():
    resp = client.create_component_from_function(addition_component)
    component = resp.details
    component.id = 0
    resp = client.create_component(component)
    assert resp.details.id > 0
    # test get component
    assert client.get_component(
        resp.details.id).details.name == resp.details.name
    # test update component
    name = resp.details.name
    resp.details.name = name + "-renamed"
    assert client.update_component(
        resp.details).details.name == name + "-renamed"
    # test delete component
    assert client.delete_component(
        resp.details.id).details.name == name + "-renamed"


def test_create_component_from_file():
    resp = client.create_component_from_function(addition_component)
    component = resp.details
    component.id = 0
    _, filepath = tempfile.mkstemp(suffix=".yaml")
    write_message(component, filepath)
    resp = client.create_component_from_file(filepath)
    assert resp.details.id > 0
    # test list component
    assert len(client.list_components().details.items) > 0


def test_create_component_from_function():
    resp = client.create_component_from_function(addition_component)
    assert resp.details.id > 0
    # test delete components
    assert len(
        client.delete_components(common_filter=CommonFilter(
            column_name="create_at",
            high_time="2052-11-29 18:12:12",
            low_time="2022-11-22 17:12:12"), ).details, ) > 0


def test_create_component_from_kfp_file():
    _, filepath = tempfile.mkstemp(suffix=".yaml")
    cmplr.compile(addition_component, package_path=filepath)
    resp = client.create_component_from_kfp_file(filepath)
    assert resp.details.id > 0


def test_method_crud():
    resp = client.create_component_from_function(addition_component)
    component_1 = resp.details
    component_2 = deepcopy(component_1)
    component_2.id = 0
    component_2.name = component_2.name + "-renamed"
    tag = tag_client_.create_tag(name="sylvan",
                                 icon="http://icon.com",
                                 fontColor="red",
                                 inheritFrom=0).details
    m = Method(
        name="test-method-1",
        description="test create method",
        infer_api="http://example.com",
        components={c.name: c
                    for c in [component_1, component_2]},
        tags=[tag],
    )
    resp = client.create_method(m)
    assert resp.details.id > 0

    _, filepath = tempfile.mkstemp(suffix=".yaml")
    m.name = "test-method-2"
    write_message(m, filepath)
    resp = client.create_method_from_file(filepath)
    assert resp.details.id > 0
    # test list method
    assert len(client.list_methods().details.items) > 0
    # test update method
    resp.details.name = "test-method-3"
    assert client.update_method(resp.details, ).details.name == "test-method-3"
    assert client.delete_method(
        id=resp.details.id).details.name == "test-method-3"


def test_create_flow():
    resp = client.create_flow_from_function(addition_pipeline)
    flow = resp.details
    flow.id = 0
    resp = client.create_flow(flow)
    assert resp.details.id > 0
    # test get flow
    assert client.get_flow(resp.details.id).details.name == resp.details.name
    # test update flow
    name = resp.details.name
    resp.details.name = name + "-renamed"
    assert client.update_flow(resp.details).details.name == name + "-renamed"
    # test delete flow
    assert client.delete_flow(
        resp.details.id).details.name == name + "-renamed"


def test_create_flow_from_file():
    resp = client.create_flow_from_function(addition_pipeline)
    flow = resp.details
    flow.id = 0
    _, filepath = tempfile.mkstemp(suffix=".yaml")
    write_message(flow, filepath)
    resp = client.create_flow_from_file(filepath)
    assert resp.details.id > 0
    # test list flow
    assert len(client.list_flows().details.items) > 0


def test_create_flow_from_function():
    resp = client.create_flow_from_function(addition_pipeline)
    assert resp.details.id > 0
    # test delete flows
    assert len(
        client.delete_flows(common_filter=CommonFilter(
            column_name="create_at",
            high_time="2052-11-29 18:12:12",
            low_time="2022-11-22 17:12:12"), ).details, ) > 0


def test_create_flow_from_kfp_file():
    _, filepath = tempfile.mkstemp(suffix=".yaml")
    cmplr.compile(addition_pipeline, package_path=filepath)
    resp = client.create_flow_from_kfp_file(filepath)
    assert resp.details.id > 0


def test_create_run():
    resp = client.create_flow_from_function(addition_pipeline)
    flow = resp.details
    flow.id = 0
    resp = client.create_flow(flow)
    assert resp.details.id > 0
    resp = client.create_run(run=Run(flow_id=resp.details.id, name='test_run'))
    assert resp.details.id > 0
    resp = client.get_run(id=resp.details.id, )
    assert resp.details.id > 0
    id = resp.details.id
    resp = client.list_runs(
        common_option=CommonOption(page=1, size=10),
        common_filter=None,
        option_filter=None,
    )
    assert len(resp.details.items) > 0
    resp = client.delete_run(id=id)
    assert resp.details.id > 0
    resp = client.get_run(id=resp.details.id, )
    assert resp.details.id == 0


def test_create_run_from_file():
    resp = client.create_flow_from_function(addition_pipeline)
    flow = resp.details
    flow.id = 0
    _, filepath = tempfile.mkstemp(suffix=".yaml")
    write_message(flow, filepath)
    resp = client.create_run_from_file(
        yaml_path=filepath,
        trigger=None,
        runtime_config=None,
    )
    assert resp.details.id > 0


def test_create_run_from_function():
    resp = client.create_run_from_function(
        func=addition_pipeline,
        trigger=None,
        runtime_config=None,
    )
    assert resp.details.id > 0


def test_create_run_from_kfp_file():
    _, filepath = tempfile.mkstemp(suffix=".yaml")
    cmplr.compile(addition_pipeline, package_path=filepath)
    resp = client.create_run_from_kfp_file(
        yaml_path=filepath,
        trigger=None,
        runtime_config=None,
    )
    assert resp.details.id > 0


def test_get_run_result():
    resp = client.create_flow_from_function(addition_pipeline)
    flow = resp.details
    flow.id = 0
    resp = client.create_flow(flow)
    assert resp.details.id > 0
    resp = client.create_run(run=Run(flow_id=resp.details.id, name='test_run'))
    assert resp.details.id > 0
    resp = client.get_run_result(
        run_id=resp.details.run_detail.run.id,
        timeout=100,
    )
    assert resp.to_dict() is not None
