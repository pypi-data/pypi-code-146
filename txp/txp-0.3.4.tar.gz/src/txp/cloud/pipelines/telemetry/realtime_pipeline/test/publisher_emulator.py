# requirements
# google-cloud-pubsub==1.7.0
import json
import time
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

# --- Base variables and auth path
CREDENTIALS_PATH = "../../../../../common/credentials/pub_sub_to_bigquery_credentials.json"
PROJECT_ID = "tranxpert-mvp"
TOPIC_ID = "txp-telemetry-realtime-test"


# --- PubSub Utils Classes
class PubSubPublisher:
    def __init__(self, credentials_path, project_id, topic_id):
        credentials = jwt.Credentials.from_service_account_info(
            json.load(open(credentials_path)),
            audience="https://pubsub.googleapis.com/google.pubsub.v1.Publisher"
        )
        self.project_id = project_id
        self.topic_id = topic_id
        self.publisher = pubsub_v1.PublisherClient(credentials=credentials)
        self.topic_path = self.publisher.topic_path(self.project_id, self.topic_id)

    def publish(self, data: str, gateway_id):
        result = self.publisher.publish(self.topic_path, data, gatewayId=gateway_id)
        return result


# --- Main publishing script
def main(edge, sampling_params, host, q_proxy):
    publisher = PubSubPublisher(CREDENTIALS_PATH, PROJECT_ID, TOPIC_ID)

    task1 = SamplingTask("92", sampling_params, "tranxpert-mvp")
    host.receive_sampling_tasks(
        {
            edge.logical_id: task1
        }
    )
    host.start_sampling_windows()
    host.drivers[0].enable_observation_pulse()
    time.sleep(30)
    host.drivers[0].stop_sampling_windows()
    time.sleep(20)
    assert not q_proxy.is_empty()
    while not q_proxy.is_empty():
        package = q_proxy.get_package()
        proto = package.get_proto()
        encoded_payload = base64.b64encode(proto.SerializeToString())
        publisher.publish(encoded_payload, "test-mockup-gateway")
        time.sleep(30)


class CustomManager(BaseManager):
    """Multiprocessing Manager to register a PackageQueue as mock to the Gateway's queue."""
    pass


CustomManager.register("PackageQueue", PackageQueue, proxytype=PackageQueueProxy)


def host_discovered_identifiers():
    return [
        "001B638445E6",
        "001B638445E7",
        "001B638445E8"
    ]


def edge_descriptors():
    mock_1_descriptor: EdgeDescriptor = EdgeDescriptor(
        "mock_1",
        MockDriver.device_name(),
        str(EdgeType.STREAM_ONLY_DEVICE),
        {
            MockDriver._PHYSICAL_ID_PARAM_FIELD: "001B638445E6"
        },
        {
            "VibrationMock": {
                "dimensions": [1, 1024],
                "sampling_frequency": 100,
                "components_per_dimension": [
                    {
                        "components":
                        # 1 dimension, only 1 element in this list.
                            [
                                # Spectral components for this dimension.
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
                "mode": 2
            },
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
    """Returns a managed Queue to share acorss process.

    It mocks the states queue used by the DeviceManager to track
    the states of the DriversHost drivers.
    """
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
        **{"discovered_identifiers": host_discovered_identifiers}
    )
    h.connect()
    return h


if __name__ == "__main__":
    q_proxy = queue_proxy()
    states_q = states_queue()
    host = mock_host(q_proxy, states_q)
    host._add_drivers(edge_descriptors())
    main(edge_descriptors()[0], sampling_parameters(), host, q_proxy)
