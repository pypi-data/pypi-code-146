"""
This module contains the concrete implementation case of Driver for the
Icomox POE device.
"""

# ============================ imports =========================================
import queue
import threading
from typing import Tuple, List

from txp.devices.drivers.driver import Driver, EdgeParameterNotFoundError, DriverState
from txp.devices.drivers.icomox.icomox_datahandling import getIcomoxMessageType, getSignalSamples, IcomoxMessageType, \
    IcomoxSensorMassageType, sendSetConfigurationCommand
from txp.common.edge import EdgeDescriptor
from txp.devices.package_queue import PackageQueueProxy
from txp.common.edge import VibrationSpeedSignal, VibrationAccelerationSignal, MicrophoneSignal, MagnetometerSignal, TemperatureSignal, \
    Signal

from txp.common.config import settings
import logging

log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)

# ==============================================================================
# Icomox driver implementation
# ==============================================================================
class IcomoxDriver(Driver):
    """Implementation of the Icomox POE driver.

    The Icomox Driver is a logical unit configured in the IoT management.
    Operational physical units are mapped to the logical configuration by using
    a Logical ID -> Mac Address mapping. This allows the system to rotate and re assign
    physical sensors without problems.
    """

    def __init__(
            self,
            edge_descriptor: EdgeDescriptor,
            gateway_packages_queue: PackageQueueProxy,
            packages_from_host_queue: queue.PriorityQueue,
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
        """
        Driver.__init__(self, edge_descriptor, gateway_packages_queue,
                        on_driver_state_changed, host_clock_notification_queue)
        self._parameters_validation(edge_descriptor)
        self._setup_signals()
        """
        _signal_shape: Internal attribute to control the VibrationSignal dimensions.
        """
        self._edge_packets_queue: queue.PriorityQueue = packages_from_host_queue
        """
        _samples_queue: A queue provided to the listener to handle packages pending to be processed
        with the timestamp as priority.
        """

        self.setup_edge()

        self._lock = threading.Lock()

    def _parameters_validation(self, edge_descriptor):
        self._vibration_adxl356_sensor_parameters_validation(edge_descriptor)
        self._vibration_adxl362_sensor_parameters_validation(edge_descriptor)
        self._magnetometer_bmm150_sensor_parameters_validation(edge_descriptor)
        self._microphone_IM69D130_sensor_parameters_validation(edge_descriptor)

    def _vibration_adxl362_sensor_parameters_validation(self, edge_descriptor):
        if (self.PERCEPTION_DIMENSIONS_FIELD not
                in edge_descriptor.perceptions[VibrationSpeedSignal.perception_name()]):
            log.error(
                f"IcomoxDriver: {self.PERCEPTION_DIMENSIONS_FIELD} not received"
                f"in {VibrationAccelerationSignal.perception_name()} perception configuration."
            )
            raise EdgeParameterNotFoundError(
                f"IcomoxDriver: {self.PERCEPTION_DIMENSIONS_FIELD} not received"
                f"in {VibrationAccelerationSignal.perception_name()} perception configuration."
            )
        if len(self.perceptions[VibrationSpeedSignal.perception_name()][self.PERCEPTION_DIMENSIONS_FIELD]) != 2:
            log.error(
                f"IcomoxDriver: {self.PERCEPTION_DIMENSIONS_FIELD} for {VibrationSpeedSignal.perception_name()}"
                f"should be of length 2"
            )
            raise EdgeParameterNotFoundError(
                f"IcomoxDriver: {self.PERCEPTION_DIMENSIONS_FIELD} for {VibrationSpeedSignal.perception_name()}"
                f"should be of length 2"
            )
        if self.PERCEPTION_SAMPLING_FREQUENCY_FIELD not in self.perceptions[VibrationSpeedSignal.perception_name()]:
            log.error(
                f"IcomoxDriver: {self.PERCEPTION_SAMPLING_FREQUENCY_FIELD} not received "
                f"in {VibrationSpeedSignal.perception_name()} perception configurtion."
            )
            raise EdgeParameterNotFoundError(
                f"IcomoxDriver: {self.PERCEPTION_SAMPLING_FREQUENCY_FIELD} not received "
                f"in {VibrationSpeedSignal.perception_name()} perception configurtion."
            )

    def _build_vibration_signal_adlx356_sensor_from_samples(self,samples, sampling_frequency=3611.11, sampling_resolution=16):
        signal_shape: Tuple[int, int] = (
            int(self.perceptions[VibrationAccelerationSignal.perception_name()][self.PERCEPTION_DIMENSIONS_FIELD][0]),
            int(self.perceptions[VibrationAccelerationSignal.perception_name()][self.PERCEPTION_DIMENSIONS_FIELD][1])
        )
        return VibrationAccelerationSignal.build_signal_from_lists(
            samples,
            signal_shape,
            sampling_frequency,
            sampling_resolution,
        )

    def _build_vibration_signal_adlx362_sensor_from_samples(self,samples, sampling_frequency=399.60, sampling_resolution=16):
        signal_shape: Tuple[int, int] = (
            int(self.perceptions[VibrationSpeedSignal.perception_name()][self.PERCEPTION_DIMENSIONS_FIELD][0]),
            int(self.perceptions[VibrationSpeedSignal.perception_name()][self.PERCEPTION_DIMENSIONS_FIELD][1])
        )
        return VibrationSpeedSignal.build_signal_from_lists(
            samples,
            signal_shape,
            sampling_frequency,
            sampling_resolution,
        )

    def _build_magnetometer_signal_bmm150_sensor_from_samples(self,samples, sampling_frequency=334.36, sampling_resolution=16):
        signal_shape: Tuple[int, int] = (
            int(self.perceptions[MagnetometerSignal.perception_name()][self.PERCEPTION_DIMENSIONS_FIELD][0]),
            int(self.perceptions[MagnetometerSignal.perception_name()][self.PERCEPTION_DIMENSIONS_FIELD][1]),
        )
        return MagnetometerSignal.build_signal_from_lists(
            samples,
            signal_shape,
            sampling_frequency,
            sampling_resolution,
        )

    def _build_microphone_signal_im69d130_sensor_from_samples(self,samples, sampling_frequency=20312, sampling_resolution=16):
        signal_shape: Tuple[int, int] = (
            int(self.perceptions[MicrophoneSignal.perception_name()][self.PERCEPTION_DIMENSIONS_FIELD][0]),
            int(self.perceptions[MicrophoneSignal.perception_name()][self.PERCEPTION_DIMENSIONS_FIELD][1]),
        )
        return MicrophoneSignal.build_signal_from_lists(
            samples,
            signal_shape,
            sampling_frequency,
            sampling_resolution,
        )

    def _build_temperature_signal_adt7410_sensor_from_samples(self,temperature):
        return TemperatureSignal.build_signal_from_value(temperature, signal_frequency=None)

    @classmethod
    def device_name(cls) -> str:
        return "Icomox"

    @classmethod
    def is_virtual(cls) -> bool:
        return False

    def observation_pulse(self) -> int:
        """The Icomox device can sample from each one of its perspectives each second.

        As a consequence, 12 seconds is enough time to collect samples from all the perspectives.
        """
        return 10

    def setup_edge(self):
        pass

    def connect_device(self):
        """
        All connection states is handled by the icomox_driver_host module for the nature of the communication
        it is always initiated by the icomox client via tcp ip. driver never initiates the communication.
        """
        pass

    def disconnect_device(self):
        """
        All connection states is handled by the icomox_driver_host module for the nature of the communication
        it is always initiated by the icomox client via tcp ip. driver never initiates the communication.
        """
        pass

    def _flush_packets_queue(self):
        while not self._edge_packets_queue.empty():
            self._edge_packets_queue.get()

    def _start_sampling_collect(
            self
    ) -> List["Signal"]:
        """This method will collect the samples obtained from the edge device and will
        produce the system Signals to send the package to the gateway.

        This method should collect samples that belong to the defined Sampling Time.

        Args:
            sampling_time_finished: event to check when the sampling time has finished.
        Returns:
            A list of Signals collected by the Icomox.
        """

        signals = []

        transmiting = False
        received_sensors = set()
        self._flush_packets_queue()
        while True:
            try:
                if not transmiting:
                    sendSetConfigurationCommand(self.get_complete_device_id().physical_id,True)
                    transmiting = True
                timeout_in_sec = 0.5
                msg = self._edge_packets_queue.get(True, timeout_in_sec)[1]
                log.debug("Message for Icomox POE received. UniqueId: {}".format(self.get_complete_device_id().physical_id))
                message_type = getIcomoxMessageType(msg)
                if message_type == IcomoxMessageType.REPORT_MESSAGE:
                    sensor_type = self._process_report_message(msg, signals)
                    received_sensors.add(sensor_type)
                elif message_type == IcomoxMessageType.API_MESSAGE:
                    self._process_api_message(msg)

            except queue.Empty as e:
                log.debug(f"Icomox Driver catched: {e}")
                pass
            except Exception as ex:
                pass

            if len(received_sensors.intersection({
                IcomoxSensorMassageType.VIBRATION_SENSOR_ADXL356,
                IcomoxSensorMassageType.VIBRATION_SENSOR_ADXL362,
                IcomoxSensorMassageType.MAGNETOMETER_SENSOR_BMM150,
                IcomoxSensorMassageType.MICROPHONE_SENSOR_IM69D130,
                IcomoxSensorMassageType.TEMPERATURE_SENSOR_ADT7410
            })) == 5:
                return signals

            if self._stop_current_pulse_signal.is_set():
                return []

    def _stop_sampling_collect(self):
        """This method will stop the sampling collection in the driver implementation.
        """
        if self.driver_state == DriverState.CONNECTED or self.driver_state == DriverState.SAMPLING:
            sendSetConfigurationCommand(self.get_complete_device_id().physical_id,False)
        else:
            log.warning("{} state is {}. couldn't turn of data sending".format(self.logical_id, self.driver_state))


    def _process_report_message(self, msg, signals) -> IcomoxSensorMassageType:
        signalType, samples = getSignalSamples(msg)
        log.debug("driver {} signal received {} and message lenght is {} samples lenth is {}".format(self.device_name(),signalType,len(msg),len(samples)))
        if signalType == IcomoxSensorMassageType.VIBRATION_SENSOR_ADXL362:
            self._process_vibration_signal_adlx362(samples, signals)
        elif signalType == IcomoxSensorMassageType.VIBRATION_SENSOR_ADXL356:
            self._process_vibration_signal_adlx356(samples, signals)
        elif signalType == IcomoxSensorMassageType.MAGNETOMETER_SENSOR_BMM150:
            self._process_magnetometer_signal_bmm150(samples, signals)
        elif signalType == IcomoxSensorMassageType.MICROPHONE_SENSOR_IM69D130:
            self._process_microphone_signal_im69d130(samples, signals)
        elif signalType == IcomoxSensorMassageType.TEMPERATURE_SENSOR_ADT7410:
            self._process_temperature_signal_adt7410(samples, signals)

        log.debug(f"Icomox {self.logical_id} received a signal {signalType.name}")

        return signalType

    def _process_temperature_signal_adt7410(self, samples, signals):
        if samples is not None:
            signal = TemperatureSignal.build_signal_from_value(
                samples[0],
                0
            )
            signals.append(signal)
        else:
            log.error('Icomox RAW data is corrupted')

    def _process_microphone_signal_im69d130(self, samples, signals):
        if samples is not None:
            signal = MicrophoneSignal.build_signal_from_lists(
                samples,
                self._signal_shape_im69d130,
                self._sampling_frequency_im69d130,
                16,
            )
            signals.append(signal)
        else:
            log.error('Icomox RAW data is corrupted')

    def _process_magnetometer_signal_bmm150(self, samples, signals):
        if samples is not None:
            signal = MagnetometerSignal.build_signal_from_lists(
                samples,
                self._signal_shape_bmm150,
                self._sampling_frequency_bmm150,
                16,
            )
            signals.append(signal)
        else:
            log.error('Icomox RAW data is corrupted')

    def _process_vibration_signal_adlx356(self, samples, signals):
        if samples is not None:
            signal = VibrationAccelerationSignal.build_signal_from_lists(
                samples,
                self._signal_shape_adlx356,
                self._sampling_frequency_adlx356,
                16,
            )
            signals.append(signal)
        else:
            log.error('Icomox RAW data is corrupted')

    def _process_vibration_signal_adlx362(self, samples, signals):
        if samples is not None:
            signal = VibrationSpeedSignal.build_signal_from_lists(
                samples,
                self._signal_shape_adlx362,
                self._sampling_frequency_adlx362,
                16,
            )
            signals.append(signal)
        else:
            log.error('Icomox RAW data is corrupted')

    def _magnetometer_bmm150_sensor_parameters_validation(self, edge_descriptor):
        if self.PERCEPTION_DIMENSIONS_FIELD not in self.perceptions[MagnetometerSignal.perception_name()]:
            log.error(
                f"IcomoxDriver: {self.PERCEPTION_DIMENSIONS_FIELD} not received "
                f"{self.perceptions[MagnetometerSignal.perception_name()]} perception configuration"
            )
            raise EdgeParameterNotFoundError(
                f"IcomoxDriver: {self.PERCEPTION_DIMENSIONS_FIELD} not received "
                f"{self.perceptions[MagnetometerSignal.perception_name()]} perception configuration"
            )
        if len(self.perceptions[MagnetometerSignal.perception_name()][self.PERCEPTION_DIMENSIONS_FIELD]) != 2:
            log.error(
                f"IcomoxDriver: {self.PERCEPTION_DIMENSIONS_FIELD} for {MagnetometerSignal.perception_name()} should"
                f"have length of 2"
            )
            raise EdgeParameterNotFoundError(
                f"IcomoxDriver: {self.PERCEPTION_DIMENSIONS_FIELD} for {MagnetometerSignal.perception_name()} should"
                f"have length of 2"
            )
        if self.PERCEPTION_SAMPLING_FREQUENCY_FIELD not in self.perceptions[MagnetometerSignal.perception_name()]:
            log.error(
                f"IcomoxDriver: {self.PERCEPTION_DIMENSIONS_FIELD} not received "
                f"in {self.perceptions[MagnetometerSignal.perception_name()]} perception configuration."
            )
            raise EdgeParameterNotFoundError(
                f"IcomoxDriver: {self.PERCEPTION_DIMENSIONS_FIELD} not received "
                f"in {self.perceptions[MagnetometerSignal.perception_name()]} perception configuration."
            )

    def _microphone_IM69D130_sensor_parameters_validation(self, edge_descriptor):
        if self.PERCEPTION_DIMENSIONS_FIELD not in self.perceptions[MicrophoneSignal.perception_name()]:
            log.error(
                f"IcomoxDriver: {self.PERCEPTION_DIMENSIONS_FIELD} not received "
                f"in {MicrophoneSignal.perception_name()} perception configuration."
            )
            raise EdgeParameterNotFoundError(
                f"IcomoxDriver: {self.PERCEPTION_DIMENSIONS_FIELD} not received "
                f"in {MicrophoneSignal.perception_name()} perception configuration."
            )
        if len(self.perceptions[MicrophoneSignal.perception_name()][self.PERCEPTION_DIMENSIONS_FIELD]) != 2:
            log.error(
                f"IcomoxDriver: {self.PERCEPTION_DIMENSIONS_FIELD} for {MicrophoneSignal.perception_name()} "
                f"should have a length of 2."
            )
            raise EdgeParameterNotFoundError(
                f"IcomoxDriver: {self.PERCEPTION_DIMENSIONS_FIELD} for {MicrophoneSignal.perception_name()} "
                f"should have a length of 2."
            )

    def _vibration_adxl356_sensor_parameters_validation(self, edge_descriptor):
        if (self.PERCEPTION_DIMENSIONS_FIELD not
                in edge_descriptor.perceptions[VibrationAccelerationSignal.perception_name()]):
            log.error(
                f"IcomoxDriver: {self.PERCEPTION_DIMENSIONS_FIELD} not received "
                f"in {VibrationAccelerationSignal.perception_name()} perception."
            )
            raise EdgeParameterNotFoundError(
                f"IcomoxDriver: {self.PERCEPTION_DIMENSIONS_FIELD} not received "
                f"in {VibrationAccelerationSignal.perception_name()} parameters."
            )
        if (len(edge_descriptor.perceptions[VibrationAccelerationSignal.perception_name()]
               [self.PERCEPTION_DIMENSIONS_FIELD]) != 2):
            log.error(
                f"IcomoxDriver: {self.PERCEPTION_DIMENSIONS_FIELD} in {VibrationAccelerationSignal.perception_name()} "
                f"perception should be have length 2."
            )
            raise EdgeParameterNotFoundError(
                f"IcomoxDriver: {self.PERCEPTION_DIMENSIONS_FIELD} in {VibrationAccelerationSignal.perception_name()} "
                f"perception should be have length 2."
            )
        if (self.PERCEPTION_SAMPLING_FREQUENCY_FIELD not
                in edge_descriptor.perceptions[VibrationAccelerationSignal.perception_name()]):
            log.error(
                f"IcomoxDriver: {self.PERCEPTION_SAMPLING_FREQUENCY_FIELD} not received"
                f"in {VibrationAccelerationSignal.perception_name()} parameters."
            )
            raise EdgeParameterNotFoundError(
                f"IcomoxDriver: {self.PERCEPTION_SAMPLING_FREQUENCY_FIELD} not received"
                f"in {VibrationAccelerationSignal.perception_name()} parameters."
            )

    def _process_api_message(self, msg):
        #TODO: check here which one is and flag the response to stop timer when a command is sent and is waiting for a response
        pass

    def _setup_signals(self):
        self._setup_signal_adlx356()
        self._setup_signal_adlx362()
        self._setup_signal_im69d130()
        self._setup_signal_bmm150()

    def _setup_signal_bmm150(self):
        self._signal_shape_bmm150: Tuple[int, int] = (
            int(self.perceptions[MagnetometerSignal.perception_name()][self.PERCEPTION_DIMENSIONS_FIELD][0]),
            int(self.perceptions[MagnetometerSignal.perception_name()][self.PERCEPTION_DIMENSIONS_FIELD][1]),
        )
        self._sampling_frequency_bmm150 = (self.perceptions[MagnetometerSignal.perception_name()]
            [self.PERCEPTION_SAMPLING_FREQUENCY_FIELD])

    def _setup_signal_im69d130(self):
        self._signal_shape_im69d130: Tuple[int, int] = (
            int(self.perceptions[MicrophoneSignal.perception_name()][self.PERCEPTION_DIMENSIONS_FIELD][0]),
            int(self.perceptions[MicrophoneSignal.perception_name()][self.PERCEPTION_DIMENSIONS_FIELD][1])
        )
        self._sampling_frequency_im69d130 = self.perceptions[MicrophoneSignal.perception_name()][self.PERCEPTION_SAMPLING_FREQUENCY_FIELD]

    def _setup_signal_adlx362(self):
        self._signal_shape_adlx362: Tuple[int, int] = (
            int(self.perceptions[VibrationSpeedSignal.perception_name()][self.PERCEPTION_DIMENSIONS_FIELD][0]),
            int(self.perceptions[VibrationSpeedSignal.perception_name()][self.PERCEPTION_DIMENSIONS_FIELD][1]),
        )
        self._sampling_frequency_adlx362 = (self.perceptions[VibrationSpeedSignal.perception_name()]
        [self.PERCEPTION_SAMPLING_FREQUENCY_FIELD])

    def _setup_signal_adlx356(self):
        self._signal_shape_adlx356: Tuple[int, int] = (
            int(self.perceptions[VibrationAccelerationSignal.perception_name()][self.PERCEPTION_DIMENSIONS_FIELD][0]),
            int(self.perceptions[VibrationAccelerationSignal.perception_name()][self.PERCEPTION_DIMENSIONS_FIELD][1]),
        )
        self._sampling_frequency_adlx356 = (self.perceptions[VibrationAccelerationSignal.perception_name()]
        [self.PERCEPTION_SAMPLING_FREQUENCY_FIELD])

