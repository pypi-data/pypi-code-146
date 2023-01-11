"""
This module contains the concrete implementation case of Driver for the
Voyager 3 device.
Technical details about the device can be found in the following document:
https://tranxpert.atlassian.net/wiki/spaces/TD/pages/230817807/Tranxpert+MVP+Monitoring+Proposal#Several-Voyager-3-working-together.
"""

# ============================ imports =========================================
import queue
import threading
import time
from typing import Dict, Tuple, List

from txp.devices.drivers.voyager.smartmesh_dongle import SmartMeshDongle
from txp.devices.drivers.driver import Driver, EdgeParameterNotFoundError
from txp.common.edge import EdgeDescriptor
from txp.devices.package_queue import PackageQueueProxy
from txp.common.edge import VibrationAccelerationSignal

from txp.common.config import settings
import logging

log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)

# ==============================================================================
# Voyager driver implementation
# ==============================================================================
class VoyagerDriver(Driver):
    """Implementation of the Voyager 3 vibration sensor driver.

    The Voyager Driver is a logical unit configured in The IoT management.
    Operational physical units are mapped to the logical configuration by using
    a Logical ID -> Mac Address mapping. This allows the system to rotate and re assign
    physical sensors without problems.
    """

    def __init__(
            self,
            edge_descriptor: EdgeDescriptor,
            gateway_packages_queue: PackageQueueProxy,
            smartmesh_manager: SmartMeshDongle,
            on_driver_state_changed: callable,
            host_clock_notification_queue: queue.Queue
    ):
        """
        Note: This Driver receives a MAC address, which is added and passed down by the Gateway operative
        configuration. The MAC address is not known by the Cloud configuration.

        Args
            edge_descriptor: The Edge Descriptor for this Driver.
            gateway_packages_queue: The Gateway Package Queue to put produced packages.
            smartmesh_manager: The SmartMesh manager that interact with the physical device.
            on_driver_state_changed: Function used to notify driver state changes.
        """
        Driver.__init__(self, edge_descriptor, gateway_packages_queue,
                        on_driver_state_changed, on_driver_state_changed, host_clock_notification_queue)
        # The Voyager receives 3 perception dimensions with adc_num_samples length

        if self.PERCEPTION_DIMENSIONS_FIELD not in self.perceptions[VibrationAccelerationSignal.perception_name()]:
            log.error(
                f"VoyagerDriver: {self.PERCEPTION_DIMENSIONS_FIELD} not received in "
                f"{VibrationAccelerationSignal.perception_name()} perception configuration"
            )
            raise EdgeParameterNotFoundError(
                f"VoyagerDriver: {self.PERCEPTION_DIMENSIONS_FIELD} not received in "
                f"{VibrationAccelerationSignal.perception_name()} perception configuration"
            )

        if len(self.perceptions[VibrationAccelerationSignal.perception_name()][self.PERCEPTION_DIMENSIONS_FIELD]) != 2:
            log.error(
                f"VoyagerDriver: {self.PERCEPTION_DIMENSIONS_FIELD} in {VibrationAccelerationSignal.perception_name()} "
                f"perception should have length 2"
            )
            raise EdgeParameterNotFoundError(
                f"VoyagerDriver: {self.PERCEPTION_DIMENSIONS_FIELD} in {VibrationAccelerationSignal.perception_name()} "
                f"perception should have length 2"
            )

        if self.PERCEPTION_SAMPLING_FREQUENCY_FIELD not in self.perceptions[VibrationAccelerationSignal.perception_name()]:
            log.error(
                f"VoyagerDriver: {self.PERCEPTION_SAMPLING_FREQUENCY_FIELD} not received "
                f"{VibrationAccelerationSignal.perception_name()} perception configuration"
            )
            raise EdgeParameterNotFoundError(
                f"VoyagerDriver: {self.PERCEPTION_SAMPLING_FREQUENCY_FIELD} not received "
                f"{VibrationAccelerationSignal.perception_name()} perception configuration"
            )

        self.sampling_frequency = int(self.perceptions[VibrationAccelerationSignal.perception_name()][self.PERCEPTION_SAMPLING_FREQUENCY_FIELD])

        self._signal_shape: Tuple[int, int] = (
            int(self.perceptions[VibrationAccelerationSignal.perception_name()][self.PERCEPTION_DIMENSIONS_FIELD][0]),
            int(self.perceptions[VibrationAccelerationSignal.perception_name()][self.PERCEPTION_DIMENSIONS_FIELD][1]),
        )
        """
        _signal_shape: Internal attribute to control the VibrationSignal dimensions.
        """

        self._manager: SmartMeshDongle = smartmesh_manager
        self.mac: Tuple = self._parse_mac_string(self._physical_id)
        self._mote_packets_queue: queue.PriorityQueue = queue.PriorityQueue()
        """
        _samples_queue: A queue provided to the Voyager SmartMesh manager to put 
            received notification packets, with the timestamp as priority.

            Since the Manager runs in the same DriversHost process as the Driver instance, 
            a threa-safe PriorityQueue can be shared.
        """

        self.setup_mote()

        self._lock = threading.Lock()

        # Internal control attributes
        self._data_valid = False
        self._rx_cnt = 0
        self._x_offset = 0
        self._y_offset = 0
        self._z_offset = 0
        self._offset_removed = {"x": False, "y": False, "z": False}

        # data buffer for num_samples for raw samples and num_samples/2 for fft magnitude
        self._data1 = int(
            (3 * self._manager.adc_num_samples / 2) + self._manager.adc_param_len
        ) * [0]
        self._data2 = int(
            (3 * self._manager.adc_num_samples / 2) + self._manager.adc_param_len
        ) * [0]

        # Ping-pong buffer, _data_order[0] = currently filling
        self._data_order = (self._data1, self._data2)
        self.scale = [0.75, 0.75, 0.75]

        self.remove_offsets = False
        self.offset = 0  # Default offset for all axis


    @staticmethod
    def _parse_mac_string(mac_str: str) -> Tuple:
        """Parse the expected mac string in hex to Tuple.

        Example:
            "00-17-0d-00-00-71-c6-48" to (0, 23, 13, 0, 0, 113, 198, 72)

        Returns:
            The tuple for the MAC address.
        """
        mac_string = mac_str.split("-")
        mac = tuple(int(i, 16) for i in mac_string)

        return mac

    @staticmethod
    def _pretty_mac(mac) -> str:
        """Parses mote mac tuple into is corresponding string

        Args:
            mac: mac id tuple
        Returns:
            Mac string.
        """
        pMac = "-".join(["%02x" % b for b in mac])
        return pMac

    def observation_pulse(self) -> int:
        60

    @classmethod
    def device_name(cls) -> str:
        return "Voyager"

    @classmethod
    def is_virtual(cls) -> bool:
        return False

    def setup_mote(self):
        frequency_msg = str(self.sampling_frequency).ljust(8, 'x')
        alarm_msg = "0xxxxxxx"
        axis_sel_msg = "111xxxxx"
        message = frequency_msg + alarm_msg + axis_sel_msg

        self._manager.send_to_mote(self.mac, message)

    def get_latest_valid_measure(self, with_offset=False):
        """Uses threading lock to return current frame of raw, fft and
        axis data.

        Args:
            with_offset(bool): If True, returns the raw and fft data without the
            offset removed.
        Returns:
            A tuple with the raw, fft and axis information from the last completed measure
            received by the smarthmesh manager.
        """
        if not self._data_valid:  # _handle_bytes has not yet been called
            return (None, None, None)

        with self._lock:
            params = self._data_order[1][0]  # Info on axis - x,y,z
            raw = self._data_order[1][2: self._manager.adc_num_samples]
            fft = self._data_order[1][
                  self._manager.adc_num_samples + self._manager.adc_param_len:
                  ]

        x_set = (int(params & 0x00F0)) == 144
        y_set = (int(params & 0x00F0)) == 160
        z_set = (int(params & 0x00F0)) == 192

        if x_set:
            ax = "x"
            self.offset = self._x_offset
        elif y_set:
            ax = "y"
            self.offset = self._y_offset
        elif z_set:
            ax = "z"
            self.offset = self._z_offset

        raw_avg = sum(raw) / len(raw)

        if with_offset:
            # raw = [ADC_gain * (x - ADC_offset) for x in raw]
            pass  # Just return raw codes
        else:
            raw = [
                (self._manager.ADC_gain * (x - self._manager.ADC_offset - self.offset))
                for x in raw
            ]

        raw_avg = sum(raw) / len(raw)
        # print("{} axis: Average G Value = {}".format(ax, raw_avg))

        fft = [2 * self._manager.ADC_gain * x for x in fft]

        return raw, fft, ax

    def connect_device(self):
        """The manager connects devices on its own. This 'connection' registers
        the driver _mote_packets_queue in the Manager.
        """
        self._device_connected()  # State transition.

    def disconnect_device(self):
        """Nothing to disconnect. The manager takes care of dealing with
        connected and unconnected devices.
        """
        self._manager.unregister_device(self.mac)
        self._device_disconnected()

    def _start_sampling_collect(
            self
    ) -> List["Signals"]:
        """This method will collect the samples obtained from the edge device and will
        produce the system Signals to send the package to the gateway.

        This method should collect samples that belong to the defined Sampling Time.

        Args:
            sampling_time_finished: event to check when the sampling time has finished.
        Returns:
            A list of VibrationSignal collected by the Voyager.
        """
        signals = []
        measures: Dict[str, list] = {}

        self._manager.register_driver(self.mac, self._mote_packets_queue)

        while True:
            if self._handle_packet():
                raw, fft, ax = self.get_latest_valid_measure()
                measures[ax] = raw

            if len(measures.keys()) == self._signal_shape[0]:
                signal = VibrationAccelerationSignal.build_signal_from_lists(
                    [measures.get('x'), measures.get('y'), measures.get('z')],
                    self._signal_shape,
                    self.sampling_frequency,
                    self._manager.adc_num_samples,
                )

                measures.clear()
                signals.append(signal)

                if len(signals) == 1:
                    break

        return signals

    def _stop_sampling_collect(self):
        """This method will stop the sampling collection in the driver implementation.
        """
        self._manager.unregister_device(self.mac)

    def _handle_packet(self) -> bool:
        """Handles the smartmesh data packages received by the smartmesh manager.
        The Voyager 3, splits one axis measurement in 17 smartmesh packages.

        Returns:
            True if a measurement was completed; otherwise False.
        """
        signal_ready = False
        timeout_in_sec = 2

        try:
            signal_ready = self._handle_bytes(self._mote_packets_queue.get(True, timeout_in_sec)[1])
        except queue.Empty:
            pass

        return signal_ready

    def _handle_bytes(self, bytes) -> bool:
        """Alings incoming SmartMesh bytes to form frames for analysis.
        Raw and fft variables are filled when method completes.

        Args:
            bytes: 90 byte packet passed down from handle_packet.
        Returns:
            True if a measurement was completed; otherwise False.
        """

        try:
            cur_data = self._data_order[0]
            data_len = len(bytes) / 2
            msb_set = bytes[1] == 255  # MSB of first word is alignment bit

            if self._rx_cnt + data_len > len(
                    cur_data
            ):  # Restart if we get more data in a frame than expected
                log.debug(
                    f"[{self.logical_id} {self._rx_cnt}] Restarting after data overflow"
                )
                self._rx_cnt = 0

            if (
                    self._rx_cnt > 0 and msb_set
            ):  # Restart if we get an alignment bit in the middle of a frame
                log.debug(f"[{self.logical_id}] Restarting after partial frame")
                log.debug(f"Rx_cnt {self._rx_cnt}, cur_data {len(cur_data)}")
                self._rx_cnt = 0

            if self._rx_cnt == 0 and not msb_set:  # Align to the start of a new frame
                log.debug(f"[{self.logical_id}] Waiting for start of new frame")
                return  # Continue count until full frame is reached

            self._lock.acquire()

            for i in range(0, len(bytes), 2):
                cur_data[self._rx_cnt] = (bytes[i + 1] << 8) | bytes[
                    i
                ]  # Convert from bytes to words
                self._rx_cnt = self._rx_cnt + 1

            frame_got = False  # True if we have entered the next if statement, avoids double release of lock
            # Are we done with frame?
            if self._rx_cnt == len(cur_data):
                self._data_order = (self._data_order[1], self._data_order[0])
                self._data_valid = True
                self._rx_cnt = 0
                self._lock.release()
                frame_got = True

                raw, fft, ax = self.get_latest_valid_measure()
                log.debug(
                    f"Got complete frame @ {time.process_time()} -- Axis: {ax} -- Mote ID: {self.logical_id}"
                )

                if self.remove_offsets:
                    self._remove_offset()
                    if self._offset_removed.values() == [True, True, True]:
                        self.remove_offsets = False

            if not frame_got:  # Ensure threading lock not released twice
                self._lock.release()
        except Exception as e:
            logging.error(e, exc_info=True)

        return frame_got

    def _remove_offset(self):
        """Updates mote offset variables for each axis, x, y, z by calculating mean for each.
        This function must be called just one time and the offset calculated will be applied
        to the measure on get_latest_valid_measure(with_offset=True).
        Recommended by the provider as calibration mechanims.
        """
        if not self._data_valid:  # _handle_bytes has not yet been called
            return

        raw_w_offset, fft, ax = self.get_latest_valid_measure(with_offset=True)

        if ax == "x" and self._offset_removed[ax] == False:
            self._x_avg0G = sum(raw_w_offset) / len(raw_w_offset)
            self._x_offset = self._x_avg0G - self._manager.ADC_offset
            self._offset_removed[ax] = True
            log.debug("Removing {} from X axis codes".format(self._x_offset))

        if ax == "y" and self._offset_removed[ax] == False:
            self._y_avg0G = sum(raw_w_offset) / len(raw_w_offset)
            self._y_offset = self._y_avg0G - self._manager.ADC_offset
            self._offset_removed[ax] = True
            log.debug("Removing {} from Y axis codes".format(self._y_offset))

        if ax == "z" and self._offset_removed["x"] and self._offset_removed["y"]:
            # Make sure x and y have been offset before Z
            self._z_offset = (
                                     self._x_avg0G + self._y_avg0G
                             ) / 2 - self._manager.ADC_offset
            self._offset_removed[ax] = True
            log.debug("Removing {} from Z axis codes".format(self._z_offset))
