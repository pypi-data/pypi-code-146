"""
This module implements the TasksScheduler object which provides
timer capabilities to other components.
"""
# ============================ imports =========================================
from typing import Optional, List, Callable, Tuple, Dict
from dataclasses import dataclass
from txp.common.config import settings
from txp.common.configuration import SamplingWindow
from txp.common.configuration.job import JobConfig, JobTask
from txp.devices.devices_manager import DevicesManager
import enum
import datetime
import threading
import time
import schedule
import logging
import copy

log = logging.getLogger(__name__)

log.setLevel(settings.txp.general_log_level)


@dataclass
class ScheduleTask:
    """The encapsulation of an Scheduled Task that can be ingested and executed by the TasksScheduler.

    It contains all the information required to configure the schedule task in time.

    And also requires from client classes to configure a callable that will be executed
    as "action" of the schedule time when the time comes. This allows for the TaskScheduler to deal
    only with time handling, while decoupling the actions performed over time as a responsibility
    of the client classes.

    """

    start_date: datetime.date  # Start time date with the format "%Y-%m-%d %H:%M:%S"
    end_date: datetime.date
    start_time: datetime.time
    end_time: datetime.time
    active_week_days: List
    callback: Callable
    callback_args: Tuple = ()


class TasksScheduler:
    """The TasksScheduler object provides an API for client classes to schedule
    tasks in time.

    A ScheduleTask contains the following attributes that will be interpreted accordingly:
        - A Start Date, which represents the specific Date and Time when a task will be
            executed for the first time.
            The Start Date format is specified in the configuration: "%Y-%m-%d %H:%M:%S"

        - Frequency: A Frequency enumerated value which indicates the frequency on which the task
        will be repeated.

        - Callback: A Callable name (method, function) provided by the client class to be the action executed
            in the scheduled task.

        - Callback Arguments: A tuple of positional arguments to forward to the Callback.
    """

    def __init__(self, name: str):
        """
        Args:
            name: Set a name to the TaskScheduler instance. This is useful for logging.
            tasks: The List of Tasks to be scheduled.
        """
        self._name = name
        self._scheduler_run_thread: Optional[threading.Thread] = None
        self._stop_event: threading.Event = None
        self._scheduler: schedule.Scheduler = schedule.Scheduler()

    def schedule_daily_callback(self, callback, start_time: str) -> None:
        """Schedule an arbitrary callback to be executed daily at start time.
        """
        log.info(f"Scheduler set daily scheduled callback to run at: {start_time}")
        self._scheduler.every().day.at(start_time).do(callback)

    def schedule_task_once(self, task: ScheduleTask, daily: bool = True, log_info: bool = True) -> None:
        """Schedule the tasks in the schedule.Scheduler instance
        to run just only once.

        The task callback is wrapped around a closure which returns
        the schedule.CancelJob value. This is done to execute the
        scheduled task only once.

        https://schedule.readthedocs.io/en/stable/examples.html#run-a-job-once
        """

        def run_just_once():
            task.callback(*task.callback_args)
            return schedule.CancelJob

        desired_daily_time_str = task.start_time.strftime("%H:%M:%S")

        if daily:
            self._scheduler.every().day.at(desired_daily_time_str).do(run_just_once)
        else:
            self._scheduler.every().second.do(run_just_once)

        scheduled_tasks = self._scheduler.jobs
        if scheduled_tasks and log_info:
            scheduled_task_datetime = scheduled_tasks[-1].next_run

            log.info(
                f"{self._name} new task to run "
                f"the {scheduled_task_datetime.date()} at {scheduled_task_datetime.time()} hours"
            )

    def is_schedule_required(self, task: ScheduleTask) -> bool:
        """Returns True if the task requires to be schedule give the current day.

        Currently only validates if the Date is valid.
        """
        # Validate the ongoing date
        current_datetime = datetime.datetime.now()
        current_date = datetime.datetime.now().date()
        valid_date = (
            (task.start_date == current_date)
            or (current_date < task.end_date)
            or (current_date == task.end_date)
        )

        # Validate the week day
        current_week_day = datetime.datetime.now().weekday()
        valid_week_day = bool(task.active_week_days[current_week_day])

        # Validate the hour
        task_datetime = datetime.datetime.combine(
             task.start_date, task.start_time
        )

        if task_datetime.date() > current_datetime.date():  # Potentially, next day.
            valid_time = True
        else:
            valid_time = task_datetime.time() >= current_datetime.time()

        return valid_week_day and valid_date and valid_time

    def is_task_currently_active(self, task: ScheduleTask) -> bool:
        """Returns True if the task requires to be schedule and started now,
        because it's currently active given the configuration."""
        current_date = datetime.datetime.now().date()
        valid_date = (
            (task.start_date == current_date)
            or (current_date < task.end_date)
            or (current_date == task.end_date)
        )

        now = datetime.datetime.now()
        valid_hour = (
            task.start_time < now.time() < task.end_time
        )

        # Validate the week day
        current_week_day = datetime.datetime.now().weekday()
        valid_week_day = bool(task.active_week_days[current_week_day])

        return valid_week_day and valid_date and valid_hour

    def _run_schedule(self):
        log_counter = 0
        while True:
            if self._stop_event.is_set():
                log.info("Stopping scheduled tasks")
                self._scheduler.clear()
                break

            self._scheduler.run_pending()
            next_run = self._scheduler.next_run
            if (
                next_run
                and (next_run - datetime.datetime.now()).total_seconds() > 0
                and log_counter > 100
            ):
                log.info(
                    f"{self._name} task scheduler next run will be at: {self._scheduler.next_run}"
                )
                log_counter = 0

            elif next_run is None and log_counter > 100:
                log.info(
                    "{self._name} task scheduler has no more scheduled tasks pending"
                )

            log_counter = log_counter + 1
            time.sleep(settings.gateway.tasks_scheduler.check_stop_event_interval)

    def start(self) -> None:
        """Starts the execution of the tasks contained in the scheduler in
        a separate thread.

        This call will return immediately.
        """

        if (
            self._scheduler_run_thread is not None
            and self._scheduler_run_thread.is_alive()
        ):
            raise RuntimeError("The scheduled already has been started")

        self._stop_event = threading.Event()
        self._scheduler_run_thread = threading.Thread(
            target=self._run_schedule,
            name="scheduler_run_thread",
            daemon=True,
        )

        self._scheduler_run_thread.start()
        log.debug("TaskScheduler scheduling thread started")

    def stop(self) -> None:
        """Stops the scheduler execution of tasks.

        It gives guarantee to stop the execution of future tasks after
        the current one has been executed.
        """
        if (
            self._scheduler_run_thread is None
            or not self._scheduler_run_thread.is_alive()
        ):
            raise RuntimeError(
                "Calling to Stop scheduler, but no scheduler as been started."
            )

        self._stop_event.set()
        log.info("Requesting to stop scheduling thread")

    def is_running_tasks(self) -> bool:
        """Returns True if the scheduler is currently busy with the processing
        of scheduling tasks. That means, the self._scheduler_run_thread is actively running"""
        return self._scheduler is not None and self._scheduler_run_thread.is_alive()

    def get_scheduled_tasks_dict(self) -> Dict:
        """Return a dictionary of the scheduled tasks to be executed.

        Returns:
            A Dictionary of scheduled tasks to be executed. The values are
            datetime values.
        """
        jobs = self._scheduler.jobs
        jobs = dict(map(lambda tpl: (tpl[0], tpl[1].next_run), enumerate(jobs)))
        return jobs
