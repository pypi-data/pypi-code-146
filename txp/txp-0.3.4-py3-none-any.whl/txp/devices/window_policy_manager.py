import threading
from txp.common.configuration.job import JobTask
from txp.common.edge import EdgeDescriptor
from txp.devices.devices_manager import DevicesManager
from datetime import datetime
from txp.common.configuration import datetime_utils
import time
from typing import List, Dict, Tuple, Set
from math import gcd
from functools import reduce
from txp.common.config import settings
import copy
import enum
import logging

from txp.devices.sampling_task import SamplingTask

log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)


class _WindowPolicyEnum(enum.Enum):
    """This policy is used by the WindowPolicyManager to decide what actions
    to take when an edge doesn't reports the expected accomplished clock pulses.

    Below there's an explanation of the policies:
        - no_wait: The Asset observation clock will not do anything about a delay of
            a driver. It will only log the WARNING messages.
        - wait_x_time: The observation clock will wait for the driver to catch up
            given a configuration timeout.
    """

    NO_WAIT = "no_wait"
    WAIT_X_TIME = "wait_x_time"


class WindowPolicyManager(threading.Thread):
    """This WindowPolicyManager conceptualizes the unit of control to check the drivers
    sampling cadence within the sampling windows of a job task.

    The Manager knows about:
        - The total number of sampling windows to execute, given the job task start time
            and end time.
        - The total number of clocks to execute in each of the mentioned sampling windows
            to execute.

    Based on those values, the manager will check and determine what policies to
    apply to the sampling cadence of the drivers.
    """
    def __init__(
        self,
        identifier: str,
        configuration_id: str,
        tenant_id: str,
        asset_task: JobTask,
        edges_logical_ids: List[str],
        devices_manager: DevicesManager,
        cancel_sampling: threading.Event,
    ):
        """
        Args:
            configuration_id: The configuration id received by the Gateway.
            asset_task: The JobTask to execute in this WindowPolicyManager.
            edges_logical_ids: The list of drivers logical IDs involved in the task
                to observe the asset.
            devices_manager: The DevicesManager singleton used in the system.
        """
        super(WindowPolicyManager, self).__init__(name=identifier, daemon=True)

        # Task context
        self._configuration_id = configuration_id
        self._tenant_id = tenant_id
        self._task: JobTask = asset_task
        self._logical_ids: List[str] = edges_logical_ids
        self._devices_manager_service: DevicesManager = devices_manager
        self._logical_ids: List[str] = [
            logical_id
            for logical_id in edges_logical_ids
            if not self._devices_manager_service.is_actuator_device(logical_id)
        ]
        self._clock_pulse_value: int = self._get_manager_clock_value()
        self._canceled: threading.Event = cancel_sampling
        self._force_stop_event: threading.Event = threading.Event()
        self._gateway_task_id: int = 0

        # Control attributes
        self._current_clock: int = 0
        self._current_window: int = 0
        self._clocks_per_window: int = self._get_total_clocks_per_window()

        current_time = datetime.now().time()

        # If the task was already "started", update to the current time
        if (
            current_time.hour > self._task.parameters.start_time.hour or
            current_time.minute > self._task.parameters.start_time.minute
        ):
            self._task.parameters.start_time = current_time

        self._num_windows: int = datetime_utils.get_num_windows_in_task(
            self._task.parameters
        )

        if self._num_windows < 0:
            log.error(
                f"There was an error computing the number of "
                f"sampling windows: {self._num_windows}"
            )
            log.warning(
                f"Asset Observation Clock set to perform 0 sampling windows after error"
            )

        elif self._num_windows == 0:
            log.warning(
                f"Total number of sampling windows in task is zero(0)."
                f"This might be caused by a configuration error. Check "
                f"the driver task configuration"
            )

        self._window_start_time: datetime = None
        self._dead_time_counter: int = 0

        # Stats attributes used in unit testing
        self._total_num_pulses_executed: int = 0

        # Policies Handling initialization
        self._policies: Dict = {
            _WindowPolicyEnum.NO_WAIT: self._no_wait_policy_apply,
            _WindowPolicyEnum.WAIT_X_TIME: self._wait_x_time_policy_apply,
        }

        try:
            self._policy = _WindowPolicyEnum(
                settings.gateway.sampling.default_observation_policy
            )
            log.debug(
                f"{self.__class__.__name__} policy configured to: {self._policy.name}"
            )
        except:
            log.warning(
                f"{self.__class__.__name__} could not parse the settings policy. "
                f"Fallback policy to {_WindowPolicyEnum.NO_WAIT.name}"
            )
            self._policy = _WindowPolicyEnum.NO_WAIT

    def force_stop(self) -> None:
        self._force_stop_event.set()

    def _get_manager_clock_value(self) -> int:
        """Returns the clock pulse value to base the synchronisation of this sampling window
        manager.

        The clock pulse value is the greatest common divisor of all the members


        The clock pulse value determines the period of time used by this SamplingWindowManager
        to execute control policies on the sampling cadence of the drivers used in the job task.
        """
        drivers_clock_pulses = [
            self._devices_manager_service.get_driver_observation_pulse(logical_id)
            for logical_id in self._logical_ids
        ]

        gcd_value = reduce(gcd, drivers_clock_pulses)

        return gcd_value

    def _get_total_clocks_per_window(self) -> int:
        """Returns the total clocks to be executed in each one of the
        sampling windows."""
        total_clock_pulses = int(
            self._task.parameters.sampling_window.sampling_time
            / self._clock_pulse_value
        )

        if not total_clock_pulses:
            log.error(
                f"{self.__class__.name} clock has 0 ticks to execute. Sampling time is less than minimal"
                " drivers observation pulse."
            )

        return total_clock_pulses

    def _apply_clock_control(self):
        """Returns the expected packages to be received in the clock pulse

        When this method gets called, each driver will have its own account
        of expected packages given by the equation:
            expected_packages = (clock value * current clock) / driver clock value.

        This equation allows the control to be relative, and it helps to deal with
        real world time which is shared by the operative system on its own.
        """
        completed_clocks_per_driver = self._get_completed_clocks_per_drivers()
        delayed_drivers: List[str] = []

        for logical_id in self._logical_ids:
            expected_packages = self._get_num_expected_packages(logical_id)

            if (
                self._devices_manager_service.is_virtual_driver(logical_id)
                and self._current_clock != self._clocks_per_window
            ):
                log.debug(
                    "Edge is virtual. Virtual edges are checked at the end of the clock."
                )
                continue  # process next edge

            if (
                expected_packages != completed_clocks_per_driver[logical_id]
            ):  # The driver is late. Adding Driver to delayed drivers.
                delayed_drivers.append(logical_id)
                log.debug(f"Driver {logical_id} is delayed. "
                          f"Expected clocks: {expected_packages} - "
                          f"Received clocks: {completed_clocks_per_driver[logical_id]}")

            else:
                log.debug(
                    f"Driver {logical_id} is synchronized with the expected pulses."
                    f"Expected pulses: {expected_packages} - "
                    f"Received pulses: {completed_clocks_per_driver[logical_id]}"
                )

        # Apply policy for the delayed drivers
        if delayed_drivers:
            log.info("Applying Windows policy to delayed drivers.")
            self._policies[self._policy](delayed_drivers)
        else:
            log.info(f"Clock pulse {self._current_clock} for window {self._current_window} "
                     f"finished without delayed drivers.")

    def _get_completed_clocks_per_drivers(self):
        return self._devices_manager_service.get_drivers_completed_clock(
            self._logical_ids
        )

    def _get_edges_to_enable_in_next_clock(self) -> List[str]:
        """Returns the list of edges logical ids to enable in the next clock pulse."""
        if self._current_clock == 1:
            edges_to_enable = self._logical_ids

        else:
            elapsed_sampling_time = self._current_clock * self._clock_pulse_value
            leftover_sampling_time = self._task.parameters.sampling_window.sampling_time - elapsed_sampling_time
            log.debug(f"Leftover time in sampling time available to enable drivers: {leftover_sampling_time}")
            edges_to_enable = [
                logical_id for logical_id in self._logical_ids if
                (
                    self._devices_manager_service.get_driver_observation_pulse(logical_id) <= leftover_sampling_time
                    and (self._clock_pulse_value * self._current_clock) %
                    self._devices_manager_service.get_driver_observation_pulse(logical_id) == 0
                    and not self._devices_manager_service.is_virtual_driver(logical_id)
                )
            ]

        log.info(f"Edges to be enabled in next clock control: {edges_to_enable}")
        return edges_to_enable

    def _get_num_expected_packages(self, edge_logical_id: str) -> int:
        """Returns the number of expected packages of the given edge
        logical id for the current clock pulse value."""
        return int(
            (self._clock_pulse_value * self._current_clock)
            / self._devices_manager_service.get_driver_observation_pulse(
                edge_logical_id
            )
        )

    def _send_drivers_tasks(self) -> None:
        """Sends the sampling tasks to the Drivers that monitors the asset"""
        tasks: List[Tuple] = []

        # Adds the observation_id to the packages sent to the edges.
        task_copy = copy.copy(self._task)
        task_copy.parameters.sampling_window.observation_timestamp = time.time_ns()
        task_copy.parameters.sampling_window.sampling_window_index = self._current_window - 1
        task_copy.parameters.sampling_window.number_of_sampling_windows = self._num_windows
        task_copy.parameters.sampling_window.gateway_task_id = self._gateway_task_id

        for logical_id in self._logical_ids:
            log.debug(
                f"Computing Sampling tasks to send to driver {logical_id} in the next "
                f"asset sampling window."
            )
            if self._devices_manager_service.is_virtual_driver(logical_id):
                log.debug(
                    f"Driver {logical_id} is virtual edge. Assuming 1 sampling task to send"
                )
                sampling_task: SamplingTask = SamplingTask(
                    self._configuration_id, task_copy.parameters,
                    self._tenant_id
                )
                tasks.append((logical_id, sampling_task))

            else:
                num_clock_pulses: int = int(
                    self._task.parameters.sampling_window.sampling_time
                    / self._devices_manager_service.get_driver_observation_pulse(
                        logical_id
                    )
                )
                driver_task_list = [
                    (
                        logical_id,
                        SamplingTask(self._configuration_id, task_copy.parameters, self._tenant_id),
                    )
                ]
                driver_tasks_list = driver_task_list * num_clock_pulses
                log.debug(
                    f"Driver {logical_id} will receive {len(driver_tasks_list)} sampling tasks"
                )
                tasks = tasks + driver_tasks_list

        self._devices_manager_service.receive_sampling_tasks_list(tasks)

    def run(self) -> None:
        # Clock control loop for the Task Sampling windows
        log.info(
            f"{self.__class__.name} clock for {self._task.machines} has {self._clocks_per_window} pulses "
            f"to execute per window"
        )
        log.info(f"Total number of sampling windows in task {self._num_windows}")

        log.info(
            f"{self.__class__.name} for {self._task.machines} has a minimal "
            f"clock pulse of {self._clock_pulse_value}"
        )

        self._gateway_task_id = time.time_ns()

        while True:
            if self._current_window == self._num_windows:
                log.info(f"{self.__class__.name} clock completed its task.")
                break

            if self._force_stop_event.is_set():
                log.warning(f"Force stop requested on WindowPolicyManager task execution")
                break

            self._current_window += 1
            self._current_clock = 0
            self._dead_time_counter = 0
            self._send_drivers_tasks()
            self._devices_manager_service.start_sampling_windows(
                self._logical_ids, self._task.parameters.predicates
            )
            self._window_start_time = datetime.now()
            log.debug(f"New clock execution started at {self._window_start_time}")
            self._devices_manager_service.clear_drivers_completed_clocks(
                self._logical_ids
            )

            window_sampling_time_start = datetime.now()
            while True:
                if self._current_clock == self._clocks_per_window:
                    log.info(
                        "Sampling Window execution completed successfully by observation clock"
                    )
                    break

                if self._force_stop_event.is_set():
                    log.warning(f"Force stop requested on WindowPolicyManager task execution")
                    break

                self._current_clock += 1
                log.info(
                    f"Window manager will execute the next clock pulse: {self._current_clock}"
                )
                self._devices_manager_service.enable_drivers_clock_pulse(
                    self._get_edges_to_enable_in_next_clock()
                )

                clock_pulse_start = datetime.now()
                while (
                    datetime.now() - clock_pulse_start
                ).total_seconds() < self._clock_pulse_value:
                    time.sleep(.1)
                    if self._canceled.is_set():
                        log.debug(
                            "Work task canceled because the cancel event was triggered."
                        )
                        self._devices_manager_service.stop_sampling_windows(
                            self._logical_ids
                        )
                        return

                    if self._force_stop_event.is_set():
                        log.warning(f"Force stop requested on WindowPolicyManager task execution")
                        break

                self._apply_clock_control()
                self._total_num_pulses_executed += 1

                self._devices_manager_service.get_drivers_completed_clock(
                    self._logical_ids
                )

            log.info(f"Sampling Window dead time execution started")
            self._devices_manager_service.notify_sampling_window_completed(self._logical_ids)

            # Waits for possible remaining sampling time
            while ((datetime.now() - window_sampling_time_start).total_seconds()
                   < self._task.parameters.sampling_window.sampling_time):
                time.sleep(1)

            remaining_dead_time = (
                self._task.parameters.sampling_window.dead_time
                - self._dead_time_counter
            )
            if remaining_dead_time < 0:
                log.warning(
                    f"Dead time was exceeded by the policy by {remaining_dead_time} secs. "
                    f"The system configuration should "
                    "be reviewed"
                )
            else:
                log.info(
                    f"Window Dead time remaining time to wait: {remaining_dead_time}"
                )
                clock_pulse_start = datetime.now()
                while not (datetime.now() - clock_pulse_start).total_seconds() >= abs(
                    remaining_dead_time
                ):
                    time.sleep(1)
                    if self._canceled.is_set():
                        log.debug(
                            "Work task canceled because the cancel event was triggered."
                        )
                        break

                    if self._force_stop_event.is_set():
                        log.warning(f"Force stop requested on WindowPolicyManager task execution")
                        break

            self._devices_manager_service.stop_sampling_windows(
                self._logical_ids
            )
            log.info("Sampling Window dead time execution completed successfully")

    def _no_wait_policy_apply(self, logical_ids: List[str]) -> None:
        """Applies the no_wait policy for the reported driver"""
        for logical_id in logical_ids:
            log.warning(
                f"Driver {logical_id} was reported as delayed, but configured policy "
                f"don't do nothing."
            )

    def _wait_x_time_policy_apply(self, logical_ids: List[str]) -> None:
        """Applies the wait_x_time policy for the reported driver.

        It will block the current thread for the configured value of x.
        If the driver catch up, then it will return immediately.
        """
        x = settings.gateway.sampling.wait_x_time_seconds_interval
        start = datetime.now()
        while (datetime.now() - start).total_seconds() < x:
            time.sleep(1)
            if self._force_stop_event.is_set() or self._canceled.is_set():
                break

        completed_clocks_per_driver = (
            self._devices_manager_service.get_drivers_completed_clock(self._logical_ids)
        )
        end = datetime.now()
        elapsed = (end - start).total_seconds()
        self._dead_time_counter += elapsed

        for logical_id in logical_ids:
            expected_num_samplings = self._get_num_expected_packages(logical_id)

            if expected_num_samplings == completed_clocks_per_driver[logical_id]:
                log.info(
                    f"Driver {logical_id} did catch up after policy: "
                    f"Expected clocks: {expected_num_samplings} - "
                    f"Reported clocks: {completed_clocks_per_driver[logical_id]}"
                )

            else:
                log.info(
                    f"The driver {logical_id} did not catch up after policy. Requesting the driver"
                    f"to stop its collection."
                )
                self._devices_manager_service.disable_drivers_clock_pulse([logical_id])

        # TODO: policies dead time count could be handled elegantly with a decorator
        log.debug(
            f"Applying policy {_WindowPolicyEnum.WAIT_X_TIME.name} "
            f"took {elapsed} from windows dead time"
        )
