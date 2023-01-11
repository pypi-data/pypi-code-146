# requirements
# google-cloud-pubsub==1.7.0
import json
import time
from random import random

import numpy as np
import txp.common.utils.firestore_utils
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
import subprocess
import os
import signal
import pytest
from txp.common.utils import metrics
import google.cloud.firestore as firestore
from google.cloud import bigquery
from google.oauth2 import service_account
from scipy.fft import fft

pipeline_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
cloud_path = os.path.dirname(os.path.dirname(os.path.dirname(pipeline_path)))
common_path = os.path.join(os.path.dirname(cloud_path), "common")

CREDENTIALS_PATH = os.path.join(os.path.join(common_path, "credentials"),
                                "pub_sub_to_bigquery_credentials.json")
PROJECT_ID = "tranxpert-mvp"
TOPIC_ID = "txp-telemetry-realtime-local-test"
credentials = service_account.Credentials.from_service_account_file(CREDENTIALS_PATH)
bigquery_client = bigquery.Client(credentials=credentials, project=credentials.project_id)

FFT_TABLE = "tranxpert-mvp:testdataset.fft"
TIME_TABLE = "tranxpert-mvp:testdataset.time"
PSD_TABLE = "tranxpert-mvp:testdataset.psd"
TIME_METRICS_TABLE = "tranxpert-mvp:testdataset.time_metrics"
FFT_METRICS_TABLE = "tranxpert-mvp:testdataset.fft_metrics"
PSD_METRICS_TABLE = "tranxpert-mvp:testdataset.psd_metrics"
EPSILON = 10e-4


# --- PubSub Utils Classes
class PubSubPublisher:
    def __init__(self, credentials_path, project_id, topic_id):
        cred = jwt.Credentials.from_service_account_info(
            json.load(open(credentials_path)),
            audience="https://pubsub.googleapis.com/google.pubsub.v1.Publisher"
        )
        self.project_id = project_id
        self.topic_id = topic_id
        self.publisher = pubsub_v1.PublisherClient(credentials=cred)
        self.topic_path = self.publisher.topic_path(self.project_id, self.topic_id)

    def publish(self, data, gateway_id):
        result = self.publisher.publish(self.topic_path, data, gatewayId=gateway_id)
        return result


def publish(edge, sampling_params, host, q_proxy):
    publisher = PubSubPublisher(CREDENTIALS_PATH, PROJECT_ID, TOPIC_ID)
    sampling_params.sampling_window.observation_timestamp = time.time_ns()
    firestore_db = firestore.Client(credentials=credentials, project=credentials.project_id)
    config_id = \
        txp.common.utils.firestore_utils.pull_current_configuration_from_firestore(firestore_db, "labshowroom-001").to_dict()['configuration_id']

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
    sent_signals = []
    while not q_proxy.is_empty():
        package = q_proxy.get_package()
        package_timestamp, package_part_index = package.metadata.package_id.split("_")
        for s in package.signals:
            sent_signals.append({
                "package_timestamp": package_timestamp,
                "signal_timestamp": s.timestamp,
                "perception_name": s.perception_name(),
                "edge_logical_id": package.metadata.edge_descriptor.logical_id,
                "data": s.samples
            })
        proto = package.get_proto()
        encoded_payload = base64.b64encode(proto.SerializeToString())
        publisher.publish(encoded_payload, "test-mockup-gateway")
        time.sleep(random())
    return sent_signals


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
    params.sampling_window.observation_timestamp = time.time_ns()
    params.sampling_window.sampling_window_index = 0
    params.sampling_window.number_of_sampling_windows = 1
    params.sampling_window.gateway_task_id = 0
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


def get_time_signal(descriptor, client):
    select_query = f"""
           SELECT * FROM `{TIME_TABLE.replace(":", ".")}` 
           WHERE edge_logical_id = "{descriptor["edge_logical_id"]}" 
                 AND package_timestamp = {descriptor["package_timestamp"]}
                 AND perception_name = "{descriptor["perception_name"]}" 
                 AND signal_timestamp = {descriptor["signal_timestamp"]}
           """
    query_result_dataframe = (client.query(select_query).result().to_dataframe())
    signals = []
    for index, row in query_result_dataframe.iterrows():
        signals.append({
            "package_timestamp": row["package_timestamp"],
            "signal_timestamp": row["signal_timestamp"],
            "perception_name": row["perception_name"],
            "edge_logical_id": row["edge_logical_id"],
            "data": np.array([np.array(dimension["values"]) for dimension in row["data"]])
        })
    return signals


def get_fft_signal(descriptor, client):
    select_query = f"""
           SELECT * FROM `{FFT_TABLE.replace(":", ".")}` 
           WHERE edge_logical_id = "{descriptor["edge_logical_id"]}" 
                 AND package_timestamp = {descriptor["package_timestamp"]}
                 AND perception_name = "{descriptor["perception_name"]}" 
                 AND signal_timestamp = {descriptor["signal_timestamp"]}
           """
    query_result_dataframe = (client.query(select_query).result().to_dataframe())
    signals = []
    for index, fft_row in query_result_dataframe.iterrows():
        fft_bigquery_per_dimension = []
        for dimension in fft_row["fft"]:
            fft_dimension = []
            for z in dimension["values"]:
                fft_dimension.append(np.complex128(complex(z["real"], z["imag"])))
            fft_bigquery_per_dimension.append(np.array(fft_dimension))
        signals.append({
            "package_timestamp": fft_row["package_timestamp"],
            "signal_timestamp": fft_row["signal_timestamp"],
            "perception_name": fft_row["perception_name"],
            "edge_logical_id": fft_row["edge_logical_id"],
            "data": fft_bigquery_per_dimension
        })
    return signals


def get_psd_signal(descriptor, client):
    select_query = f"""
           SELECT * FROM `{PSD_TABLE.replace(":", ".")}` 
           WHERE edge_logical_id = "{descriptor["edge_logical_id"]}" 
                 AND package_timestamp = {descriptor["package_timestamp"]}
                 AND perception_name = "{descriptor["perception_name"]}" 
                 AND signal_timestamp = {descriptor["signal_timestamp"]}
           """
    query_result_dataframe = (client.query(select_query).result().to_dataframe())
    signals = []
    for index, psd_row in query_result_dataframe.iterrows():
        signals.append({
            "package_timestamp": psd_row["package_timestamp"],
            "signal_timestamp": psd_row["signal_timestamp"],
            "perception_name": psd_row["perception_name"],
            "edge_logical_id": psd_row["edge_logical_id"],
            "psd": [dimension["psd"] for dimension in psd_row["data"]],
            "frequency": [dimension["frequency"] for dimension in psd_row["data"]]
        })
    return signals


def get_metrics(descriptor, dimension, client, table):
    select_query = f"""
               SELECT * FROM `{table.replace(":", ".")}` 
               WHERE edge_logical_id = "{descriptor["edge_logical_id"]}" 
                     AND package_timestamp = {descriptor["package_timestamp"]}
                     AND perception_name = "{descriptor["perception_name"]}" 
                     AND signal_timestamp = {descriptor["signal_timestamp"]}
                     AND dimension = {dimension}
               """
    query_result_dataframe = (client.query(select_query).result().to_dataframe())
    metrics_list = []
    for index, row in query_result_dataframe.iterrows():
        metrics_list.append({
            "rms": row["rms"],
            "standard_deviation": row["standard_deviation"],
            "crest_factor": row["crest_factor"]
        })
        if table == PSD_METRICS_TABLE:
            metrics_list[-1]["peak_amplitude"] = row["peak_amplitude"]
            metrics_list[-1]["peak_frequency"] = row["peak_frequency"]
        else:
            metrics_list[-1]["peak"] = row["peak"]
    return metrics_list


@pytest.fixture(scope="module")
def sent_signals():
    q_proxy = queue_proxy()
    states_q = states_queue()
    host = mock_host(q_proxy, states_q)
    host.add_drivers(edge_descriptors())
    sent_signals = publish(edge_descriptors()[0], sampling_parameters(), host, q_proxy)
    pipeline_process = subprocess.Popen(
        f"cd {pipeline_path};"
        "python realtime_pipeline.py --streaming "
        f"--input_subscription projects/tranxpert-mvp/subscriptions/{TOPIC_ID}-sub "
        f"--time_table {TIME_TABLE} "
        f"--fft_table {FFT_TABLE} "
        f"--psd_table {PSD_TABLE} "
        f"--time_metrics_table {TIME_METRICS_TABLE} "
        f"--fft_metrics_table {FFT_METRICS_TABLE} "
        f"--psd_metrics_table {PSD_METRICS_TABLE} "
        f"--model_signals_topic_name txp-model-serving-signals-local-test"
        , shell=True, preexec_fn=os.setsid)

    time.sleep(100)
    os.killpg(os.getpgid(pipeline_process.pid), signal.SIGTERM)
    time.sleep(50)
    return sent_signals


def test_time_tables(sent_signals):
    for s in sent_signals:
        cloud_signal = get_time_signal(s, bigquery_client)
        assert len(cloud_signal) == 1
        cloud_signal = cloud_signal[0]
        for i, dimension in enumerate(cloud_signal["data"]):
            assert (dimension == s["data"][i]).all()
            dimension_metrics = get_metrics(s, i, bigquery_client, TIME_METRICS_TABLE)
            assert len(dimension_metrics) == 1
            dimension_metrics = dimension_metrics[0]
            assert dimension_metrics["peak"] == metrics.peak(dimension)
            assert dimension_metrics["rms"] == metrics.rms(dimension)
            assert dimension_metrics["standard_deviation"] == metrics.standard_deviation(dimension)
            assert dimension_metrics["crest_factor"] == metrics.crest_factor(dimension)


def test_fft_tables(sent_signals):
    for s in sent_signals:
        cloud_signal = get_fft_signal(s, bigquery_client)
        assert len(cloud_signal) == 1
        cloud_signal = cloud_signal[0]
        for i, dimension in enumerate(cloud_signal["data"]):
            fft_dimension = fft(s["data"][i])
            fft_dimension = np.array([np.complex128(complex(float(z.real), float(z.imag))) for z in fft_dimension])
            assert len(fft_dimension) == len(dimension)
            for j, z in enumerate(dimension):
                assert abs(z.real - fft_dimension[j].real) <= EPSILON
                assert abs(z.imag - fft_dimension[j].imag) <= EPSILON

            dimension_metrics = get_metrics(s, i, bigquery_client, FFT_METRICS_TABLE)
            assert len(dimension_metrics) == 1
            dimension_metrics = dimension_metrics[0]
            assert dimension_metrics["peak"] == metrics.peak(dimension.real)
            assert dimension_metrics["rms"] == metrics.rms(dimension.real)
            assert dimension_metrics["standard_deviation"] == metrics.standard_deviation(dimension.real)
            assert dimension_metrics["crest_factor"] == metrics.crest_factor(dimension.real)


def test_psd_signal(sent_signals):
    for s in sent_signals:
        cloud_signal = get_psd_signal(s, bigquery_client)
        assert len(cloud_signal) == 1
        cloud_signal = cloud_signal[0]

        for i, dimension in enumerate(cloud_signal["psd"]):
            _, psd = metrics.get_psd(s["data"][i],
                                     edge_descriptors()[0].perceptions[s["perception_name"]]["sampling_frequency"])
            for j, e in enumerate(dimension):
                assert abs(psd[j] - e) <= EPSILON

        for i, dimension in enumerate(cloud_signal["frequency"]):
            f, _ = metrics.get_psd(s["data"][i],
                                   edge_descriptors()[0].perceptions[s["perception_name"]]["sampling_frequency"])
            for j, e in enumerate(dimension):
                assert abs(f[j] - e) <= EPSILON

        for i in range(0, len(cloud_signal["psd"])):
            f, psd = metrics.get_psd(s["data"][i],
                                     edge_descriptors()[0].perceptions[s["perception_name"]]["sampling_frequency"])
            integrated_psd = metrics.integrate(psd, x=f)
            dimension_metrics = get_metrics(s, i, bigquery_client, PSD_METRICS_TABLE)
            assert len(dimension_metrics) == 1
            dimension_metrics = dimension_metrics[0]
            assert abs(dimension_metrics["peak_amplitude"] - metrics.peak(psd)) < EPSILON
            assert abs(dimension_metrics["peak_frequency"] - metrics.peak(f)) < EPSILON
            assert abs(dimension_metrics["rms"] - np.sqrt(integrated_psd[-1])) < EPSILON
            assert abs(dimension_metrics["standard_deviation"] - metrics.standard_deviation(psd)) < EPSILON
            assert abs(dimension_metrics["crest_factor"] - metrics.crest_factor(psd)) < EPSILON

