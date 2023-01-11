from txp.devices.tasks_scheduler import TasksScheduler, ScheduleTask
from txp.common.configuration import *
from txp.common.edge.common import MachineMetadata
from txp.devices.window_policy_manager import WindowPolicyManager
from txp.devices.telemetry_sender import TelemetrySender
from txp.devices.devices_manager import DevicesManager
from txp.common.config import settings
from functools import reduce
from typing import Optional
from queue import SimpleQueue
import time
import threading
import logging
import copy

log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)


class JobTasksManager:
    """The JobTasksManager is responsibly for the logic related to sampling
    tasks and telemetry sending in a job.

    """

    def __init__(
        self,
        gateway_conf: GatewayConfig,
        telemetry_sender: TelemetrySender,
        devices_manager: DevicesManager,
        configuration_id: Optional[str],
        machines: Optional[Dict[str, MachineMetadata]],
        job_task_finished_queue: SimpleQueue
    ):
        self._gateway_conf: GatewayConfig = gateway_conf
        self._configuration_id: str = configuration_id
        self._telemetry_sender: TelemetrySender = telemetry_sender
        self._devices_manager: DevicesManager = devices_manager
        self._machines_dict: Optional[Dict[str, MachineMetadata]] = machines
        self._cancel_event = threading.Event()

        self._window_managers: Dict[str, WindowPolicyManager] = {}
        self._scheduler: TasksScheduler = None
        self._job_task_finished_queue: SimpleQueue = job_task_finished_queue

    def start(self):
        self._scheduler = TasksScheduler("JobsTaskManager")
        self._scheduler.schedule_daily_callback(self._daily_schedule_plan_callback, "00:00:10")
        self._daily_schedule_plan_callback()
        self._scheduler.start()

    def stop(self):
        # Todo: ensure that all active WindowPolicyManager's are stopped
        self._cancel_event.set()
        if self._scheduler.is_running_tasks():
            self._scheduler.stop()
            while self._scheduler.is_running_tasks():
                time.sleep(1)

        if self._telemetry_sender.is_running():
            self._telemetry_sender.stop()
            while self._telemetry_sender.is_running():
                time.sleep(1)

        self._scheduler = None

    def _daily_schedule_plan_callback(self) -> None:
        """This is a callback intended to be called everyday to check which tasks
        require to be schedule for the current day.
        """
        sampling_tasks = self._get_sampling_tasks()
        telemetry_tasks = self._get_telemetry_tasks()

        for task_beg, task_end in sampling_tasks:
            if self._scheduler.is_schedule_required(task_beg):
                self._scheduler.schedule_task_once(task_beg)
                self._scheduler.schedule_task_once(task_end)

            elif self._scheduler.is_task_currently_active(task_beg):
                immediate_task = copy.copy(task_beg)
                immediate_task.start_time = datetime.datetime.now().time().replace(
                    microsecond=0, second=0
                )
                self._scheduler.schedule_task_once(
                    immediate_task,
                    daily=False,
                    log_info=True)
                self._scheduler.schedule_task_once(
                    task_end
                )

        for task in telemetry_tasks:
            if self._scheduler.is_schedule_required(task):
                self._scheduler.schedule_task_once(task)

            # Ad Hoc logic to check if Telemetry task already started
            elif self._is_telemetry_running(task):
                immediate_task = copy.copy(task)
                immediate_task.start_time = datetime.datetime.now().time().replace(
                    microsecond=0, second=0
                )
                now = datetime.datetime.now()
                leftover_time = abs(now - datetime.datetime.combine(
                    task.end_date, task.end_time
                )).total_seconds()

                task.callback_args = (task.callback_args[1], leftover_time)

                self._scheduler.schedule_task_once(
                    immediate_task,
                    daily=False,
                    log_info=True)

    def _is_telemetry_running(self, task: ScheduleTask) -> bool:
        """Returns True if the provided telemetry Task information should be currently
        running"""
        current_date = datetime.datetime.now().date()
        valid_date = (
                (task.start_date == current_date)
                or (current_date < task.end_date)
                or (current_date == task.end_date)
        )
        now = datetime.datetime.now()
        if task.end_date > now.date():
            valid_hour = (
                    task.start_time < now.time()
            )
        else:
            valid_hour = (
                    task.start_time < now.time() < task.end_time
            )

        # Validate the week day
        current_week_day = datetime.datetime.now().weekday()
        valid_week_day = bool(task.active_week_days[current_week_day])

        return valid_week_day and valid_date and valid_hour

    def _get_sampling_tasks(
        self
    ) -> List[ScheduleTask]:
        scheduler_tasks: List[(ScheduleTask, ScheduleTask)] = []
        for task in self._gateway_conf.job.tasks:
            edges_logical_ids: List[str] = []

            for asset_id in task.machines:
                edges_logical_ids = edges_logical_ids + \
                                    self._machines_dict[asset_id].edges_ids

            # Add start of task callback to the scheduler
            thread_name = str(time.time())
            callback_args = (thread_name, self._configuration_id, copy.deepcopy(task),
                             edges_logical_ids, self._devices_manager)

            sampling_task_begin = ScheduleTask(
                    task.parameters.start_date,
                    task.parameters.end_date,
                    task.parameters.start_time,
                    task.parameters.end_time,
                    task.parameters.week_days_mask,
                    self._start_sampling_task_callback,
                    callback_args
                )

            # And end of task callback to the scheduler
            sampling_task_end = ScheduleTask(
                    task.parameters.start_date,
                    task.parameters.end_date,
                    task.parameters.end_time,
                    task.parameters.end_time,
                    task.parameters.week_days_mask,
                    self._finish_sampling_task_callback,
                    (thread_name,),
                )

            scheduler_tasks.append((sampling_task_begin, sampling_task_end))

        return scheduler_tasks

    def _get_telemetry_tasks(self) -> List[ScheduleTask]:
        """Returns a 24hrs telemetry schedule plan for the provided gateway job configuration.

        Note: The user of the method should provide the callbacks for the returned entities.

        Returns:
            List of Telemetry Tasks
        """
        # Compute relative data
        current_date = datetime.datetime.now().date()
        job_start_time = self._gateway_conf.job.parameters.start_time
        job_end_time = self._gateway_conf.job.parameters.end_time
        job_sampling_window = self._gateway_conf.job.parameters.sampling_window

        if job_end_time <= job_start_time:  # The Job end in next day
            job_end_date = current_date + datetime.timedelta(days=1)
        else:
            job_end_date = current_date

        job_start_datetime = datetime.datetime.combine(current_date, job_start_time)
        job_end_datetime = datetime.datetime.combine(job_end_date, job_end_time)

        # Compute Telemetry Tasks
        total_job_secs = (job_end_datetime - job_start_datetime).total_seconds()
        num_sampling_windows = int(
            total_job_secs / job_sampling_window.observation_time
        )  # 24 hrs to seconds
        telemetry_tasks: List[ScheduleTask] = []

        logical_ids: List[str] = reduce(
            list.__add__,
            list(
                map(
                    lambda machine_metadata: machine_metadata.edges_ids,
                    self._machines_dict.values(),
                )
            ),
        )

        for i in range(0, num_sampling_windows):
            telemetry_start_time = job_start_datetime + datetime.timedelta(
                seconds=(
                    job_sampling_window.observation_time
                    + (job_sampling_window.observation_time * i)
                    - job_sampling_window.dead_time
                )
            )
            telemetry_end_time = telemetry_start_time + datetime.timedelta(
                seconds=job_sampling_window.dead_time
            )
            secs_timeout = (telemetry_end_time - telemetry_start_time).total_seconds()
            task = ScheduleTask(
                telemetry_start_time.date(),
                telemetry_end_time.date(),
                telemetry_start_time.time(),
                telemetry_end_time.time(),
                self._gateway_conf.job.parameters.week_days_mask,
                self._telemetry_sender.start,
                (self._gateway_conf, logical_ids, secs_timeout),
            )
            telemetry_tasks.append(task)

        log.info(
            f"[{self.__class__.__name__}]: The provided Job is active for current "
            f"day {current_date.strftime('%A')}. Job information: \n\t"
            f"Date: {current_date}. Day: {current_date.strftime('%A')}.\n\t"
            f"Total Telemetry Tasks computed: {len(telemetry_tasks)}"
        )

        return telemetry_tasks

    def _start_sampling_task_callback(
            self, window_manager_id: str, configuration_id: str, task: JobTask, logical_ids: List[str],
            devices_manager: DevicesManager
    ):
        window_manager: WindowPolicyManager = WindowPolicyManager(
            window_manager_id, configuration_id, self._gateway_conf.tenant_id, task, logical_ids, devices_manager,
            self._cancel_event
        )
        window_manager.start()
        self._window_managers[window_manager_id] = window_manager
        log.info(f"{self.__class__.__name__} starting a new " f"WindowPolicyManager")

    def _finish_sampling_task_callback(self, window_manager_id: str):
        window_manager = self._window_managers[window_manager_id]
        if window_manager.is_alive():
            log.warning(
                "Job Task hasn't finished yet, Forcing stop"
            )
            window_manager.force_stop()
            
        else:
            log.info("Job Task finished successfully.")

        self._job_task_finished_queue.put(window_manager_id)

        self._window_managers.pop(window_manager_id)
