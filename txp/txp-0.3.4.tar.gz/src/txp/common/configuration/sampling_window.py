import time
from typing import Dict
from txp.common.protos import gateway_config_pb2 as gateway_config_proto


class SamplingWindow:
    """Configuration values for the sampling cadence of Edge devices.
    The sampling cadence defines how to handle data collected by edge
    devices according to time.
    The sampling cadence contemplates the following configuration parameters:
        Observation time:
            time where a full sampling is collected, which can include device collected
            data and human-in-the-loop generated data.
        Sampling time:
            the period of time within an observation time where device collected data should be considered.
        Dead time:
            the period of time within an observation time where edge devices aren't collecting data,
            or it is being discarded.

    A SamplingWindow refers to the Machine identifiers of the machine(s) that are configured with
    that sampling window.
    """

    def __init__(self, observation_time: int, sampling_time: int, observation_timestamp=None):
        """
        Args:
            observation_time (int): The Observation time value.
            sampling_time (int): The Sampling time value.
            machines_ids(str): The MachineMetadata IDs associated with this
                sampling window.
        """
        self._observation_timestamp = observation_timestamp
        self._observation_time: int = int(observation_time)
        self._sampling_time: int = int(sampling_time)
        self._dead_time: int = abs(observation_time - sampling_time)

        # Set at runtime for the sampling windows task context
        self._gateway_task_id: int = 0
        self._sampling_window_index: int = 0
        self._number_of_sampling_windows: int = 0

    @property
    def observation_time(self) -> int:
        return self._observation_time

    @property
    def gateway_task_id(self) -> int:
        return self._gateway_task_id

    @property
    def sampling_window_index(self) -> int:
        return self._sampling_window_index

    @property
    def number_of_sampling_windows(self) -> int:
        return self._number_of_sampling_windows

    @gateway_task_id.setter
    def gateway_task_id(self, task_id: int) -> None:
        self._gateway_task_id = task_id

    @sampling_window_index.setter
    def sampling_window_index(self, index: int) -> None:
        self._sampling_window_index = index

    @number_of_sampling_windows.setter
    def number_of_sampling_windows(self, num_sampling_windows: int) -> None:
        self._number_of_sampling_windows = num_sampling_windows

    @property
    def sampling_time(self) -> int:
        return self._sampling_time

    @property
    def observation_timestamp(self) -> int:
        return self._observation_timestamp

    @observation_timestamp.setter
    def observation_timestamp(self, timestamp):
        self._observation_timestamp = timestamp

    @property
    def dead_time(self) -> int:
        return self._dead_time

    @staticmethod
    def build_from_proto(
        proto: gateway_config_proto.SamplingWindowProto,
    ) -> "SamplingWindow":
        """Returns the class instance from the proto value.

        Args:
            proto: The SamplingWindowProto to build the class instance from.

        Raises:
            ValueError: if the received proto is not an instance of SamplingWindowProto.
        """
        if isinstance(proto, gateway_config_proto.SamplingWindowProto):
            sw = SamplingWindow(
                proto.observation_time, proto.sampling_time, proto.observation_timestamp,
            )
            sw.number_of_sampling_windows = proto.number_of_sampling_windows
            sw.sampling_window_index = proto.sampling_window_index
            sw.gateway_task_id = proto.gateway_task_id
            return sw

        raise ValueError(
            "Trying to build SamplingWindow from proto, but the proto instance is unknown"
        )

    def get_proto(self) -> gateway_config_proto.SamplingWindowProto:
        """Return the SamplingWindowProto instance for this SamplingWindow"""
        proto = gateway_config_proto.SamplingWindowProto(
            observation_time=self.observation_time,
            sampling_time=self.sampling_time,
            observation_timestamp=self.observation_timestamp,
            gateway_task_id=self.gateway_task_id,
            sampling_window_index=self.sampling_window_index,
            number_of_sampling_windows=self.number_of_sampling_windows
        )
        return proto

    def reprJSON(self) -> Dict:
        """Returns a Dict easily serializable to JSON"""
        return dict(observation_time=self.observation_time,
                    sampling_time=self.sampling_time,
                    observation_timestamp=self.observation_timestamp,
                    gateway_task_id=self.gateway_task_id,
                    sampling_window_index=self.sampling_window_index,
                    number_of_sampling_windows=self.number_of_sampling_windows
                    )
