import logging
from typing import List, Dict
import txp.common.utils.metrics as metrics
from scipy.fft import fft
import numpy as np
import apache_beam as beam
from txp.common import edge
from google.cloud import firestore
from txp.common.utils import firestore_utils
import txp.common.utils.bigquery_utils as bq_utils
from google.cloud import bigquery


_VALID_DEVICES = {"Icomox"}


def compute_rms_smooth(data: List, window_size: int = 8):
    """Receives a parsed perception dimensions values.

    Returns a List of BigQuery column ready value.
    """
    rms_data_axis = []
    for index, single_axis_sample in enumerate(data):
        rms_data_axis.append({"values": [], "index": index})
        n = len(rms_data_axis)
        rms_data_axis[n - 1]["values"] = metrics.rolling_rms(
            np.asarray(single_axis_sample)
        ).tolist()
    return rms_data_axis


def compute_fft(data: List[Dict]):
    """Compute the FFT on the array of values.

    It returns a list with the BigQuery column ready values
    """
    fft_data = []
    for dimension_signal_sample in data:
        fft_data.append({"values": [], "index": dimension_signal_sample["index"]})
        n = len(fft_data)
        for z in fft(dimension_signal_sample["values"]):
            fft_data[n - 1]["values"].append(
                {"real": float(z.real), "imag": float(z.imag)}
            )

    return fft_data


def compute_rpm(mag_axis_data):
    """
    TODO: Required information motor specific should be pulled down from persistence layer.
    """
    from iCOMOXSDK.sensors import BMM150

    rpm_axis = []
    BMM150_quantile_for_noise_floor_estimator = 0.25
    BMM150_minimum_SNR_for_speed_detection_dB = 20
    BMM150_ = BMM150.class_BMM150(
        quantile_for_noise_floor_estimator=BMM150_quantile_for_noise_floor_estimator,
        minimum_SNR_for_speed_detection_dB=BMM150_minimum_SNR_for_speed_detection_dB,
    )

    for axis in mag_axis_data:
        ASYNC_MOTOR_number_of_poles_pairs = 2
        ASYNC_MOTOR_slip_factor_percentages = 0.0
        network_frequency_Hz = BMM150_.maximum_of_PSD(axis)
        synchronous_frequency_Hz = (
            network_frequency_Hz / ASYNC_MOTOR_number_of_poles_pairs
        )
        rotor_frequency_Hz = synchronous_frequency_Hz * (
            1 - ASYNC_MOTOR_slip_factor_percentages / 100
        )
        rpm = rotor_frequency_Hz * 60
        rpm_axis.append(rpm)
    return rpm_axis


class VibrationProcessing(beam.DoFn):
    """This step is used to generate the RMS smoothed wave given an input signal.

    It's the first step required to generate the vibration data analysis.
    """

    def to_runner_api_parameter(self, unused_context):
        return "beam:transforms:custom_parsing:custom_v0", None

    def is_valid_device(self, element) -> bool:
        return element["device_type"] in _VALID_DEVICES

    def get_signal_data(self, elements, signal_type):
        data = None
        for e in elements:
            if e["perception_name"] == signal_type.perception_name():
                logging.info(f"Vibration processing found signal for {signal_type.perception_name()}")
                data = e["data"]
        if not data:
            return None

        fmt_data = [
            list(dimension["values"]) for dimension in data
        ]

        return fmt_data

    def get_edge_from_db(self, db_client: firestore.Client, element: Dict):
        edge_doc = firestore_utils.get_edge_from_firestore(
            element["configuration_id"],
            element["tenant_id"],
            element["edge_logical_id"],
            db_client
        )
        return edge_doc

    def get_machine_id_by_edge(self, db_client: firestore.Client, element: Dict, edge_ref):
        machine = firestore_utils.get_machine_from_firestore_by_edge(
            db_client, element["tenant_id"], edge_ref
        )

        if not machine:
            logging.warning(
                f"Could not find machine for the package received from "
                f"{element['edge_logical_id']}"
            )
            machine_id = ""

        else:
            logging.info(
                f"The package received belongs to the machine: {machine['machine_id']}"
            )
            machine_id = machine["machine_id"]

        return machine_id

    def get_bigquery_row(self, element, machine_id, magnetometer_data, temperature_data):
        perception_data = [list(dimension["values"]) for dimension in element["data"]]
        rms_data_axis = compute_rms_smooth(perception_data)
        fft_data = compute_fft(rms_data_axis)
        rmp_data = compute_rpm(magnetometer_data)

        data_formatted = []
        for i, dimension_signal_sample in enumerate(perception_data):
            data_formatted.append(
                {"values": list(dimension_signal_sample), "index": i}
            )
            i += 1

        return {
            "signal": data_formatted,
            "rms_smoothed_signal": rms_data_axis,
            "fft": fft_data,
            "rpm": rmp_data,
            "temperature": temperature_data[0][0],
            "failure_frequencies": [],
            "perception_name": element["perception_name"],
            "edge_logical_id": element["edge_logical_id"],
            "asset_id": machine_id,
            "configuration_id": element["configuration_id"],
            "observation_timestamp": element["observation_timestamp"],
            "tenant_id": element["tenant_id"],
            "partition_timestamp": element["partition_timestamp"],
            "observation_time_secs": element["sampling_window_observation_time"]
        }

    def process(
        self, elements, timestamp=beam.DoFn.TimestampParam, window=beam.DoFn.WindowParam
    ):
        # Get first element for metadata access
        element = elements[0]
        # Only process Vibration data from Icomox box
        if not self.is_valid_device(element):
            logging.info(
                f"Decive of {element['device_type']} is not "
                f"valid for Vibration Processing step."
            )
            return

        # Todo: here we should pull from DB the window size for the given motor/sensor.

        magnetometer_data = self.get_signal_data(elements, edge.MagnetometerSignal)
        temperature_data = self.get_signal_data(elements, edge.TemperatureSignal)
        firestore_client = firestore.Client()
        edge_doc = self.get_edge_from_db(firestore_client, element)
        machine_id = self.get_machine_id_by_edge(firestore_client, element, edge_doc.reference)

        for e in elements:
            if e["perception_name"] not in {
                edge.VibrationSpeedSignal.perception_name(),
                edge.VibrationAccelerationSignal.perception_name(),
            }:
                continue
            logging.info(
                f"Processing vibration step for {e['perception_name']} from edge: {e['edge_logical_id']}"
            )
            bigquery_row = self.get_bigquery_row(
                e, machine_id, magnetometer_data, temperature_data
            )

            logging.info(
                f"Yielding vibration steps result for {e['perception_name']} from edge: {e['edge_logical_id']}"
            )

            yield bigquery_row
