# Copyright 2021-2023 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-3.0-or-later
import argparse
from enum import Enum
import itertools
import json
import logging
from pathlib import Path
from queue import Queue
import os
import signal
import threading
import time
import toml


# We don't need the distinction between background (bg) and foreground (fg)
from ansi.colour import fg as colour

from .exceptions import (
    ConfigurationError,
    GitLabUnavailableError,
    GitLabUnexpectedError,
    JobLaunchTimeout,
    PaasProvisioningError,
    PaasResourceError,
)
from .job import JobHandle
from .runner import PaasRunner

logger = logging.getLogger(__name__)


QUOTA_CONFIG_KEY = 'quota_computation'
MAX_CONCURRENCY_CONFIG_KEY = 'concurrent'


class JobEventType(Enum):
    LAUNCHING = 0
    """Job launch process has started.

    No provisioning or actual deployment have already occurred at the
    time this event is emitted.
    """

    LAUNCHED = 1
    """The job is fully running, as it can be seen from the coordinator
    """

    LAUNCH_FAILED = 2

    FINISHED = 3
    """The job is done.

    It is in particular supposed to have reported its result to coordinator
    """

    COORDINATOR_REPORT_FAILED = 4
    """Used in failure of reporting a job result to coordinator from here.

    Typically, such reporting happens only in cases of launch failures. Once
    a job is launched, it takes responsibility over the reporting to
    coordinator.
    """

    LAUNCH_REQUEST = 5
    """Used by the coordinator poll loop to request a launch.

    The corresponding message is a tuple of length 3 instead of 2.
    """

    DECOMMISSIONED = 6
    """Used to notify success of decommission for the resource of a job handle.
    """


WAKEUP_MESSAGE = object()


COORDINATOR_REPORT_LAUNCH_FAILURES_RETRY_DELAY = 30
FINAL_THREAD_SHUTDOWN_TIMEOUT = 60


SLEEP_STEP_DURATION = 2
"""
Maximum amout of time for any thread to sleep without checking for signals.

Some polling threads may sleep for a long time between their true activity.

On the
other hand, they still must check regularly for shutdown requests and the
like. Hence actual sleep time will be cut in steps of the given duration, for
signal checking wake-ups.
"""


class PaasDispatcher:
    """Main backing class for the Heptapod PAAS Runner.

    This is a multi-threaded system that polls the coordinators on
    a regular basis to acquire jobs and starts auxiliary threads to launch
    them.

    Threads:

    - :attr:`event_processing_thread`: permanent thread that listens for
      events, maintains the mutable state and starts auxiliary threads.
      Even if shutdown is required, it waits for the auxiliary threads before
      exiting. The auxiliary threads are themselves supposed to finish as
      soon as possible if shutdown is required (e.g, by breaking out of
      retry loops etc.).
    - :attr:`launched_jobs_progress_threads`: jobs (running on the PAAS
      system) report their status directoy to the coordinator. This threads
      polls the coordinator regularly to check if they are finished and
      sends appropriate events.
    - laucher threads: spawned by the event processing thread, they are
      responsible for all provisioning and startup of jobs. They report
      back with events.

    Mutable state attributes:

    - :attr:`potential_concurrency`: number of parallel jobs we'll have
      if all those the coordinator gave us get launched successfully.
      Gets compared to :attr:`max_concurrency`.

    - :attr:`potential_weight`: total weight of the jobs currently running
      or being launched (handed over by the coordinators).
      Gets compared to :attr:`weighted_quota`.

    - :attr:`shutdown_required`: boolean regularly checked by threads to
      terminate early if set. Must be set by :meth:`shutdown()` except in
      tests.

    - Job collections

      These all use :class:`JobHandle` directly or as keys.
      An important design invariant to maintain is that the event processing
      threads has write monopoly on them once it is started.

      + :attr:`pending_jobs` is a mapping from job handles to full job
        descriptions sent by the coordinator
      + :attr:`launched_jobs` contains all jobs currently fully launched
        and not yet known to be finished
      + :attr:`launch_errors`: self-explanatory

    """

    def __init__(self, config):
        self.init_runners(config)
        self.init_state_file(config)
        self.init_max_concurrency(config)
        self.init_intervals(config)
        self.finished_jobs_keep_resources = config.get(
            'paas_finished_jobs_keep_resources', False)

        self.reporting_queue = Queue()

        self.potential_weight = 0
        self.potential_concurrency = 0
        self.max_pending_jobs = config.get('paas_max_concurrent_provisioning',
                                           10)

        # job collections
        self.launch_errors = []
        self.launched_jobs = set()
        self.pending_jobs = {}
        self.to_decommission = set()

        self.launched_jobs_progress_thread = None
        self.event_processing_thread = None

        self.shutdown_required = False
        # Total number of jobs launched, successfully or not, incremented
        # when certainty about launch status has been obtained (in particular
        # does not count retries). Mostly useful for tests.
        self.total_job_launches = 0

    def init_runners(self, config):
        """Return an immutable iterable of Runner instances.

        Immutability will be helpful to avoid bugs in the requeueing loop.
        """
        # TODO catch, log then ignore init errors (perhaps in classmethod,
        # returnning None, then)
        runners = (PaasRunner.create(conf) for conf in config['runners'])
        self.runners = {runner.unique_name: runner for runner in runners}

    def init_intervals(self, config):
        self.poll_interval = config.get('check_interval', 3)
        self.job_progress_interval = config.get('job_progress_poll_interval',
                                                30)

    def runner_by_human_name(self, name):
        """Lookup runner by its human-readable name.

        The human-readable name is the `name` entry in the runner
        configuration. It is not to be confused with the runner's unique name
        (derived from its token). To lookup by `unique_name`, simply use
        the :attr:`runners` :class:dict:.

        Since unicity of the human-readable name is not formally guaranteed,
        this is a first-match logic.

        :raises KeyError: if no runner with the given human-readable name
           could be found.
        """
        for runner in self.runners.values():
            if runner.config['name'] == name:
                return runner
        raise KeyError(name)

    def init_max_concurrency(self, config):
        """Set :attr:`max_concurrency` and :attr:`weighted_quota` from config.

        Upstream GitLab Runner default value for the `concurrent` configuration
        item is 1, which doesn't make sense for a runner backed by a whole
        cloud infrastructure, so we're setting a higher, yet moderate default.
        """
        self.max_concurrency = config.get(MAX_CONCURRENCY_CONFIG_KEY, 50)
        try:
            quota = config[QUOTA_CONFIG_KEY]
        except KeyError:
            raise ConfigurationError(
                f"The {QUOTA_CONFIG_KEY} section is mandatory")

        runner_name = quota['reference_runner']
        flavor_name = quota['reference_flavor']
        njobs = quota['reference_jobs_count']
        runner = self.runner_by_human_name(runner_name)
        flavor = runner.available_flavors[flavor_name]
        self.weighted_quota = flavor.weight * njobs
        logger.warning(
            "Maximum concurrency set to %d; weighted quota set to %.1f "
            "(weight of %d jobs with flavor %s of the %r runner)",
            self.max_concurrency, self.weighted_quota,
            njobs, flavor_name, runner_name,
        )

    def init_state_file(self, config):
        path = config.get('state_file')
        if path is not None:
            path = Path(path)
        self.state_file_path = path

    def wait_all_threads(self, timeout=FINAL_THREAD_SHUTDOWN_TIMEOUT):
        logger.info("Waiting (at most %s seconds) for all "
                    "threads to finish and report back before exit",
                    timeout)

        # because the event_processing_thread waits for launcher threads
        # to finish, there's no need to wait for them directly (avoids
        # keeping a list, and related race conditions).
        for thread in (
                self.launched_jobs_progress_thread,
                self.event_processing_thread,
        ):
            if thread is not None:
                thread.join(timeout=timeout)
                if thread.is_alive():
                    logger.warning("Thread %r is still alive after "
                                   "giving it %d seconds to shut down",
                                   thread.name, timeout)

    def interruptible_sleep(self, duration, debug=''):
        """Sleep for the given duration unless there is a shutdown request.

        it will take up to :const:`SLEEP_STEP_DURATION` to detect the
        shutdown request.

        :return: whether a shutdown request was dectected
        """
        while duration > 0:
            if self.shutdown_required:
                return True
            logger.debug("interruptible sleep duration=%s %s",
                         duration, debug)
            time.sleep(min(SLEEP_STEP_DURATION, duration))
            duration -= SLEEP_STEP_DURATION
        return self.shutdown_required

    def process_events(self):
        launcher_threads_count = 0
        while not self.shutdown_required or launcher_threads_count:
            msg = self.reporting_queue.get()
            if msg is WAKEUP_MESSAGE:
                continue

            job_handle, status = msg[:2]
            if status is JobEventType.LAUNCH_REQUEST:
                job_data = msg[2]
                # With most of the time spent in subprocess and HTTP calls,
                # GIL expected to become a bottleneck in the long term only
                self.start_launcher_thread(job_handle, job_data)
            if status is JobEventType.LAUNCHING:
                # potential concurrency updated by the poll loop
                launcher_threads_count += 1
                logger.info("Launching %s (expected weight %.1f)",
                            job_handle, job_handle.expected_weight)
            elif status is JobEventType.LAUNCHED:
                correction = job_handle.weight_correction()
                logger.log(
                    logging.DEBUG if correction == 0 else logging.WARNING,
                    "Launched %s weight correction: %.1f",
                    job_handle, correction)
                self.potential_weight += correction
                launcher_threads_count -= 1
                self.launched_jobs.add(job_handle)
                self.pending_jobs.pop(job_handle, None)
                self.total_job_launches += 1
                logger.info("Successfullly launched %s (final weight %.1f)",
                            job_handle, job_handle.paas_resource.weight)
            elif status is JobEventType.LAUNCH_FAILED:
                self.potential_concurrency -= 1
                self.potential_weight -= job_handle.expected_weight
                launcher_threads_count -= 1
                self.pending_jobs.pop(job_handle, None)
                logger.error("Failed to launch %s", job_handle)
                self.total_job_launches += 1
                self.launch_errors.append(job_handle)
            elif status is JobEventType.COORDINATOR_REPORT_FAILED:
                # event supersedes LAUNCH_FAILED (adds info that reporting
                # the failure itself failed)
                self.potential_concurrency -= 1
                self.potential_weight -= job_handle.expected_weight
                launcher_threads_count -= 1
            elif status is JobEventType.FINISHED:
                logger.info("Finished %s, according to "
                            "coordinator.", job_handle)
                self.launched_jobs.discard(job_handle)
                if not self.finished_jobs_keep_resources:
                    self.to_decommission.add(job_handle)
                    self.start_decommission_thread(job_handle)
            elif status is JobEventType.DECOMMISSIONED:
                self.potential_concurrency -= 1
                self.potential_weight -= job_handle.paas_resource.weight
                self.to_decommission.discard(job_handle)
                logger.info("Resource for %s successfully decommissioned",
                            job_handle)

    def launch_job(self, job_handle, job_data):
        """Provision and start job for runner, reporting on queue

        Job arguments are very redundant to avoid needless back-and-forth
        conversions. These are, from source to most refined and partial:

        :param dict job_data: full job specification (not JSON serialized)
        :param JobHandle job_handle: representation of the job, can be
          recreated from ``job_data``.
        """

        reporting_queue = self.reporting_queue
        reporting_queue.put((job_handle, JobEventType.LAUNCHING))
        success = False

        runner = self.runners[job_handle.runner_name]
        try:
            # if job is from a previous process interrupted while the job
            # was waiting for full launch, it can have a PAAS resource, and
            # even have been launched already (with full launch not yet
            # acknowledged at the time of interruption)
            app = job_handle.paas_resource
            if app is None:
                app = runner.provision(job_data)
                job_handle.paas_resource = app
            if not app.launched:
                runner.launch(app, job_data)
        except PaasProvisioningError as exc:
            logger.error("Provisioning failed for %s"
                         "(action=%r, code=%r, transport code=%r, details=%r)",
                         job_handle,
                         exc.action, exc.code, exc.transport_code,
                         exc.error_details)
            runner.job_append_trace(job_handle,
                                    colour.red(exc.error_details) + '\n')
        except PaasResourceError as exc:
            logger.error("Launching failed for %s, error on resource %r "
                         "(action=%r, code=%r, transport code=%r, details=%r)",
                         job_handle, exc.resource_id,
                         exc.action, exc.code, exc.transport_code,
                         exc.error_details)
            runner.job_append_trace(job_handle,
                                    colour.red(exc.error_details) + '\n')
        except Exception:
            logger.exception("Unexpected exception for %s", job_handle)
        else:
            try:
                if not runner.job_wait_trace(
                        job_data['job_info']['project_id'],
                        job_handle,
                        interruptible_sleep=self.interruptible_sleep
                ):
                    return
            except JobLaunchTimeout as exc:
                _, timeout = exc.args
                logger.error("No activity after launch for %s (timeout "
                             "set to %d seconds)", job_handle, timeout)
                # TODO if the job is finished (cancelled etc), then GitLab
                # will probably return a 40x error on this.
                runner.job_append_trace(
                    job_handle,
                    colour.red(f"Job not active (no log) after {timeout} "
                               f"seconds" + '\n')
                )
            else:
                success = True

        if success:
            in_process_status = JobEventType.LAUNCHED
        else:
            # script_failure is formally incorrect, but it triggers no special
            # banner rendering, whereas all other currently available values
            # (as of Heptapod 0.34.0) display a banner with
            # inappropriate messages (e.g., please retry).
            # `runner_system_failure` should be the one for
            # temporary provisioning errors, though.
            in_process_status = self.report_coordinator_job_failed(
                job_handle, reason='script_failure')
        reporting_queue.put((job_handle, in_process_status))

    def decommission(self, job_handle):
        resource = job_handle.paas_resource
        runner = self.runners[job_handle.runner_name]
        if resource is None:
            logger.error("Decommission triggered for %s, that does not "
                         "have a PAAS resource.", job_handle)
            return

        logger.info("Now decomissioning resource %r for %s",
                    resource.app_id, job_handle)
        try:
            runner.decommission(resource)
        except PaasResourceError as exc:
            logger.error("Error in decommission for %s: %r",
                         job_handle, exc)
        else:
            self.reporting_queue.put(
                (job_handle, JobEventType.DECOMMISSIONED))

    def report_coordinator_job_failed(self, job_handle, reason):
        """Report failure with exception catching and retry logic.

        :returns: the appropriate :class:JobEventType: that caller should emit.
        """
        runner = self.runners[job_handle.runner_name]
        attempt = 0
        max_attempts = 3
        delay = COORDINATOR_REPORT_LAUNCH_FAILURES_RETRY_DELAY
        while attempt < max_attempts:
            attempt += 1
            try:
                runner.report_coordinator_job_failed(job_handle, reason)
                logger.warning("Successfully reported %s as failed to launch",
                               job_handle)
                return JobEventType.LAUNCH_FAILED
            except Exception:
                logger.exception("Exception while attempting to report "
                                 "failure to launch %s to coordinator "
                                 "(attempt %d/%d). Will retry in %d seconds",
                                 job_handle, attempt, max_attempts, delay)
                if self.interruptible_sleep(delay, debug='launch_job'):
                    logger.warning("General shutdown required, stop "
                                   "retrying to launch %s", job_handle)
                    # failure to report could be due to some misconfiguration
                    # that could precisely motivation for a restart, let's
                    # keep in pending jobs so that a new process can retry
                    # the whole launching and reporting
                    break
        return JobEventType.COORDINATOR_REPORT_FAILED

    def max_pending_jobs_reached(self):
        """Tell if the maximum of pending (being launched) jobs is reached.

        This is not intended to be thread-safe, hence fully exact. It is more
        of a soft limit: it should not matter if there is one or even a couple
        of jobs acquired and not yet acknowledged by the event processing
        thread.
        """
        launching = len(self.pending_jobs)
        reached = launching >= self.max_pending_jobs
        if reached:
            logger.info("Maximum number %d of jobs being launched reached "
                        "(total %d). "
                        "Will resume polling coordinators when enough "
                        "are fully launched.",
                        self.max_pending_jobs, launching)
        return reached

    def poll_all_launch(self):
        """Poll for all runners and launch jobs.

        Each runner is polled until it doesn't get jobs to run any more.
        """
        logger.debug("poll_all_launch starting")
        event_queue = self.reporting_queue
        polling_runners = list(self.runners.values())

        while (polling_runners
               and not self.shutdown_required
               and not self.max_pending_jobs_reached()
               ):
            logger.debug("Current potential weight: %.1f, concurrency: %d",
                         self.potential_weight, self.potential_concurrency)
            next_runners = []
            for runner in polling_runners:
                headroom = self.weighted_quota - self.potential_weight
                logger.debug("Current weight headroom before polling runner: "
                             "%d (current weight of running or launching "
                             "jobs is %d, maximum configured weight is %d)",
                             headroom,
                             self.potential_weight,
                             self.max_concurrency)
                if headroom < runner.min_requestable_weight:
                    logger.info(
                        "Runner %s: not polling because the smallest weight "
                        "that can be a priori requested from coordinator is "
                        "%d, above current headroom %d (current weight "
                        "of running or launching jobs is %d, "
                        "maximum configured weight is %d)",
                        runner,
                        runner.min_requestable_weight,
                        headroom,
                        self.potential_weight,
                        self.weighted_quota)
                    continue

                if self.potential_concurrency >= self.max_concurrency:
                    continue

                logger.debug("Requesting job from runner %s",
                             runner.unique_name)
                job_json = runner.request_job(max_weight=headroom)
                if job_json is None:
                    continue

                job_data = json.loads(job_json)
                weight = runner.expected_weight(job_data)
                job_handle = JobHandle(job_id=job_data['id'],
                                       runner_name=runner.unique_name,
                                       expected_weight=weight,
                                       token=job_data['token'])
                # need to immediately update potential concurrency and weight.
                # Doing it in a thread would make it possible to acquire a
                # new job before those limits take the present one into
                # account, hence overflowing them.
                self.pending_jobs[job_handle] = job_data
                self.potential_weight += weight
                self.potential_concurrency += 1
                event_queue.put(
                    (job_handle, JobEventType.LAUNCH_REQUEST, job_data))
                # requeue for immediate repolling
                next_runners.append(runner)

            polling_runners = next_runners

    def start_launcher_thread(self, job_handle, job_data):
        launcher = threading.Thread(
            daemon=True,
            target=lambda: self.launch_job(job_handle, job_data))
        launcher.name = 'launcher-%s-%d' % (job_handle.runner_name,
                                            job_handle.job_id)
        launcher.start()

    def start_initial_threads(self):
        """Start threads for processing of initial (just loaded) state.

        Only to be used right after pending jobs have been loaded,
        and before the start of the polling loop, to avoid duplicating
        launcher threads already started by the polling loop.
        """
        # The threads we are launching can start right away mutating
        # the collections (especially in tests where waiting times can be 0).
        # Let's avoid being impaired by that:
        pending = tuple(self.pending_jobs.items())
        to_decomm = tuple(self.to_decommission)

        for job_handle, job_data in pending:
            self.start_launcher_thread(job_handle, job_data)
        for job_handle in to_decomm:
            self.start_decommission_thread(job_handle)

    def start_decommission_thread(self, job_handle):
        decom = threading.Thread(
            daemon=True,
            target=lambda: self.decommission(job_handle))
        decom.name = 'decommission-%s-%d' % (job_handle.runner_name,
                                             job_handle.job_id)
        decom.start()

    def poll_launched_jobs_progress_once(self):
        """Call coordinator to enquire about progress of launched jobs.

        This is notably useful to track down the number of currently running
        jobs.
        """
        # normally, only the reporting thread would mutate the `launched_jobs`
        # attributes, and removals are even done only upon signal from
        # this method (currently launched in a single thread).
        # Still, we can be sure of thread safety by copying to an immutable
        # structure before iteration.
        for job_handle in tuple(self.launched_jobs):
            logger.debug("Polling progress for %r", job_handle)
            runner_name = job_handle.runner_name
            runner = self.runners[runner_name]
            try:
                finished = runner.is_job_finished(job_handle)
            except GitLabUnavailableError as exc:
                # warning only because this is likely to be a temporary
                # condition
                logger.warning("Runner %r, coordinator not available, "
                               "could not poll job progress "
                               "(got %r on URL %r)",
                               runner_name, exc.message, exc.url)
            except GitLabUnexpectedError as exc:
                logger.error("Runner %r, got HTTP error %d from coordinator "
                             "while polling job progress. URL was %r, "
                             "message is %r", runner_name,
                             exc.status_code, exc.url, exc.message)
            except Exception:  # the thread must not crash
                logger.exception("Unexpected exception while polling "
                                 "coordinator for progress of %s", job_handle)
            else:
                if finished:
                    logger.warning("%r is FINISHED", job_handle)
                    self.reporting_queue.put((job_handle,
                                              JobEventType.FINISHED))

    def start_launched_jobs_progress_thread(self):
        def progress_loop():
            logger.info("Thread to poll coordinator about progress of "
                        "launched jobs started, polling every %d seconds",
                        self.poll_interval)
            while True:
                self.poll_launched_jobs_progress_once()
                if self.interruptible_sleep(self.poll_interval,
                                            debug="poll job progress"):
                    return

        thread = self.launched_jobs_progress_thread = threading.Thread(
            target=progress_loop, daemon=True)
        thread.name = "launched-jobs-progress"
        thread.start()

    def start_event_processing_thread(self):
        thread = self.event_processing_thread = threading.Thread(
            target=self.process_events, daemon=True)
        thread.name = "event-processing"
        thread.start()

    def poll_loop(self, max_cycles=None):
        """Repeatedly poll the coordinators.

        :param interval: time to wait between polling cycles if jobs limits
           are not reached
        :param interval_when_saturated: time to wait between polling cycles
           if jobs limits are reached.
        :param max_cycles: if not specified, this method never stops by
           itself. Otherwise,  the polling stops after the given
           number of cycles (note that this is not the number of time each
           coordinator gets polled.)
        """
        poll_cycles = 0
        infinite = max_cycles is None

        while infinite or poll_cycles < max_cycles:
            self.poll_all_launch()
            # No runners got job, sleep before polling coordinator again
            # TODO Slightly incorrect: we have spent some time polling for busy
            # runners, and that could become non negligible compared to the
            # wanted delay for some non-busy ones.
            # This could be fixed by another layer of threading (per
            # runner) to handle that, but that will be good enough for now.
            # Also, waiting times should be per coordinator

            if (
                    self.potential_concurrency >= self.max_concurrency
                    or self.potential_weight >= self.weighted_quota
            ):
                interval = self.job_progress_interval
                logger.info(
                    "No (more) jobs to process and max concurrency %d "
                    "or weighted quota %.1f is reached, with current %d jobs "
                    "running or being launched for a total weight of %.1f; "
                    "will poll again in %d seconds if back under limits ",
                    self.max_concurrency, self.weighted_quota,
                    self.potential_concurrency, self.potential_weight,
                    interval
                )
            else:
                interval = self.poll_interval
                logger.debug("No (more) job to process, "
                             "polling for all runners again in %d seconds",
                             interval)

            poll_cycles += 1
            if self.interruptible_sleep(interval, debug='new job loop'):
                break
        return poll_cycles

    def shutdown_signal(self, signum, frame):
        logger.warning("Caught signal %s. Triggering graceful shutdown",
                       signum)
        self.shutdown()

    def shutdown(self):
        if self.shutdown_required:
            return

        self.shutdown_required = True
        # make sure the event processing thread reconsiders the
        # shutdown flag even if there is no other remaining thread
        # to report back to it.
        self.reporting_queue.put(WAKEUP_MESSAGE)

    def log_state_signal(self, signum, frame):
        logger.warning("launched jobs=%r, pending jobs=%r,"
                       "to_decommission=%r, launch_errors=%r, "
                       "weight of acquired jobs=%.1f, weight quota=%.1f, "
                       "total acquired jobs=%d, max_concurrency=%d",
                       self.launched_jobs,
                       list(self.pending_jobs),
                       list(self.to_decommission),
                       self.launch_errors,
                       self.potential_weight,
                       self.weighted_quota,
                       self.potential_concurrency,
                       self.max_concurrency,
                       )

    def load_job_handle(self, data):
        runner = self.runners.get(data['runner_name'])
        return JobHandle.load(runner, data)

    def load_state(self):
        path = self.state_file_path
        if not path.exists():
            logger.info('State file "%s" does not exist. Nothing to load.',
                        path)
            return

        logger.info("Loading state from '%s'", path)
        with open(path) as fobj:
            state = json.load(fobj)

        self.launched_jobs = set(self.load_job_handle(job)
                                 for job in state['launched'])
        self.pending_jobs = {self.load_job_handle(job): data
                             for job, data in state['pending']
                             }
        self.to_decommission = set(
            self.load_job_handle(job)
            for job in state.get('to_decommission', ()))
        self.potential_concurrency = (len(state['launched'])
                                      + len(state['pending']))
        self.potential_weight = sum(
            jh.actual_or_expected_weight()
            for jh in itertools.chain(self.launched_jobs, self.pending_jobs)
        )

        logger.info("Initialized state from '%s'. Currently tracking %d "
                    "running jobs and having %d pending jobs to launch and "
                    "%d resources to decommission",
                    path, len(self.launched_jobs),
                    len(self.pending_jobs),
                    len(self.to_decommission),
                    )
        logger.debug("Full set of running jobs as loaded from '%s': %r",
                     path, self.launched_jobs)
        logger.debug("Full set of pending jobs as loaded from '%s': %r",
                     path, self.launched_jobs)

        os.unlink(path)

    def save_state(self):
        path = self.state_file_path
        logger.info("Saving state to '%s'", path)
        state = dict(launched=[jh.dump() for jh in self.launched_jobs],
                     to_decommission=[jh.dump()
                                      for jh in self.to_decommission],
                     pending=[(jh.dump(), job_data)
                              for jh, job_data in self.pending_jobs.items()])
        path.touch(mode=0o600, exist_ok=True)
        with open(path, 'w') as fobj:
            json.dump(state, fobj)
        logger.info("Saved state to '%s'", path)


def main(raw_args=None):
    """Console script entry point.
    """
    parser = argparse.ArgumentParser(
        description="Second prototype for the PAAS runner system"
    )
    parser.add_argument("runner_config", help="Path to Heptapod Runner "
                        "configuration file")
    parser.add_argument("--poll-interval", type=int,
                        help="DEPRECATED Time (seconds) to wait after all "
                        "available jobs "
                        "are treated before polling coordinators again.")
    parser.add_argument("--job-progress-poll-interval", type=int,
                        help="DEPRECATED Time (seconds) to wait between "
                        "coordinators "
                        "polls about progress of successfully launched jobs")
    parser.add_argument("--poll-cycles", type=int,
                        help="Number of times to poll all runners. "
                        "(useful for testing purposes)")
    parser.add_argument("--debug-signal", action='store_true',
                        help="Dump details about current state in logs "
                        "on SIGUSR1 (can contain secrets, for debugging "
                        "purposes only)")

    parser.add_argument("-l", "--logging-level", default='INFO')

    cl_args = parser.parse_args(raw_args)
    logging.basicConfig(
        level=getattr(logging, cl_args.logging_level.upper()),
        format="%(asctime)s [%(process)d] %(name)s %(levelname)s %(message)s",
    )

    with open(cl_args.runner_config) as conf_file:
        conf = toml.load(conf_file)

    if cl_args.poll_interval is not None:
        logger.warning(
            "The --poll-interval command-line option is deprecated. "
            "Please use the `check_interval` global configuration "
            "item instead."
        )
        conf['check_interval'] = cl_args.poll_interval

    job_progress_interval = cl_args.job_progress_poll_interval
    if job_progress_interval is not None:
        logger.warning(
            "The --jobs-progress-poll-interval command-line option "
            "is deprecated. "
            "Please use the `job_progress_poll_interval` global "
            "configuration item instead."
        )
        conf['job_progress_poll_interval'] = job_progress_interval

    try:
        dispatcher = PaasDispatcher(conf)
    except ConfigurationError as exc:
        logger.fatal(exc.args[0])
        return 2

    for signum in [signal.SIGINT,
                   signal.SIGTERM,
                   ]:
        signal.signal(signum, dispatcher.shutdown_signal)
    if cl_args.debug_signal:
        signal.signal(signal.SIGUSR1, dispatcher.log_state_signal)

    dispatcher.load_state()
    dispatcher.start_initial_threads()
    dispatcher.start_event_processing_thread()
    dispatcher.start_launched_jobs_progress_thread()

    try:
        done_cycles = dispatcher.poll_loop(max_cycles=cl_args.poll_cycles)
    except Exception:
        logger.exception("Uncatched exception in main thread. Will exit "
                         "right away with abnormal termination code")
        exit_code = 1
    else:
        logger.warning("Main thread will exit normally "
                       "after %d polling cycles",
                       done_cycles)
        exit_code = 0

    dispatcher.shutdown()
    dispatcher.wait_all_threads()
    logger.debug("Done waiting for permanent threads.")
    dispatcher.save_state()
    return exit_code
