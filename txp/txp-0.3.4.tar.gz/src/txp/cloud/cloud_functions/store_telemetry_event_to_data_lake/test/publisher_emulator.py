import json
import time
from random import random
from google.auth import jwt
from google.cloud import pubsub_v1
from txp.common.configuration import SamplingWindow
from txp.common.edge import EdgeDescriptor, EdgeType
from txp.devices.drivers.mock.mock_driver import MockDriver, MockDriversHost
import base64
from multiprocessing.managers import BaseManager
from txp.devices.package_queue import PackageQueueProxy, PackageQueue
import multiprocessing
import datetime
from txp.common.configuration import SamplingParameters
from txp.devices.sampling_task import SamplingTask
from txp.common.utils import firestore_utils as cu
import google.cloud.firestore as firestore
from google.oauth2 import service_account


CREDENTIALS_PATH = "../../../../common/credentials/pub_sub_to_bigquery_credentials.json"
PROJECT_ID = "tranxpert-mvp"
TOPIC_ID = "txp-telemetry-realtime-local-test"
credentials = service_account.Credentials.from_service_account_file(CREDENTIALS_PATH)


class PubSubPublisher:
    def __init__(self, _credentials, topic_id):
        self.publisher = pubsub_v1.PublisherClient(credentials=_credentials)
        self.topic_path = self.publisher.topic_path(credentials.project_id, topic_id)

    def publish(self, data, gateway_id):
        result = self.publisher.publish(self.topic_path, data, gatewayId=gateway_id)
        return result


def main(edge, sampling_params, host, q_proxy):
    publisher = PubSubPublisher(credentials, TOPIC_ID)
    sampling_params.sampling_window.observation_timestamp = time.time_ns()
    firestore_db = firestore.Client(credentials=credentials, project=credentials.project_id)
    config_id = \
        cu.pull_current_configuration_from_firestore(firestore_db, "labshowroom-001").to_dict()['configuration_id']
    firestore_db.close()

    task1 = SamplingTask(config_id, sampling_params, "labshowroom-001")

    host.receive_sampling_tasks(
        {
            edge.logical_id: task1
        }
    )
    host.start_sampling_windows()
    host.drivers[0].enable_observation_pulse()
    time.sleep(50)
    host.drivers[0].notify_sampling_window_completed()
    time.sleep(50)

    assert not q_proxy.is_empty()
    while not q_proxy.is_empty():
        package = q_proxy.get_package()
        proto = package.get_proto()
        encoded_payload = base64.b64encode(proto.SerializeToString())
        publisher.publish(encoded_payload, "test-mockup-gateway")
        time.sleep(random())


class CustomManager(BaseManager):
    pass


CustomManager.register("PackageQueue", PackageQueue, proxytype=PackageQueueProxy)


def edge_descriptors():
    mock_1_descriptor: EdgeDescriptor = EdgeDescriptor(
        "mock_1",
        MockDriver.device_name(),
        str(EdgeType.STREAM_ONLY_DEVICE),
        {
            MockDriver._PHYSICAL_ID_PARAM_FIELD: "001B638445E6",
            "clock_pulse": 15
        },
        {
            "VibrationMock": {
                "dimensions": [1, 1024],
                "sampling_frequency": 100000,
                "components_per_dimension": [
                    {
                        "components":
                            [
                                {
                                    "amplitude": 1,
                                    "frequency": 7.0,
                                    "phase": 0,
                                    "component_type": "sine"
                                },
                                {
                                    "amplitude": 1,
                                    "frequency": 13.0,
                                    "phase": 0,
                                    "component_type": "sine"
                                }
                            ],
                    }
                ],
                "mode": 3
            }
        },
    )
    return [mock_1_descriptor]


def sampling_parameters() -> SamplingParameters:
    params = SamplingParameters(
        SamplingWindow(10, 5),
        datetime.datetime.now().date(),
        datetime.datetime.now().date(),
        "1111111",
        datetime.datetime.now().time(),
        (datetime.datetime.now() + datetime.timedelta(seconds=15)).time(),
        []
    )
    return params


def states_queue():
    queue = multiprocessing.Manager().Queue()
    return queue


def queue_proxy() -> PackageQueueProxy:
    manager = CustomManager()
    manager.start()
    q_proxy: PackageQueueProxy = manager.PackageQueue()
    return q_proxy


def mock_host(q_proxy, states_q) -> MockDriversHost:
    h = MockDriversHost(
        q_proxy, states_q,
        **{"discovered_identifiers": ["001B638445E6", "001B638445E7", "001B638445E8"]}
    )
    h.connect()
    return h


if __name__ == "__main__":
    q_proxy = queue_proxy()
    states_q = states_queue()
    host = mock_host(q_proxy, states_q)
    host.add_drivers(edge_descriptors())
    main(edge_descriptors()[0], sampling_parameters(), host, q_proxy)

