# -*- coding: utf-8 -*-
# Copyright © 2023 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import threading

import contrast
from contrast.agent.heartbeat import HEARTBEAT_THREAD_NAME
from contrast.agent.server_settings_poll import SERVER_SETTING_THREAD_NAME
from contrast.agent.telemetry import Telemetry, TELEMETRY_THREAD_NAME
from contrast.reporting.reporting_client import (
    ReportingClient,
    REPORTING_CLIENT_THREAD_NAME,
)
from contrast.agent.settings import Settings
from contrast.utils.decorators import fail_quietly

from contrast.extern import structlog as logging

logger = logging.getLogger("contrast")

LOG_MSG = "%s thread wasn't running - restarting it now"

# The lock here is to prevent a race condition when restarting background threads.
# We need to ensure that only one thread at once can get the list of running threads and
# act accordingly based on that list.
MODULE_LOCK = threading.Lock()


@fail_quietly("failed to check background threads")
def ensure_running(middleware):
    """
    Check that long-running agent background threads are running in the current process.
    Restart any threads that appear to have been killed.

    This occurs most often when a webserver that preloads the application forks its
    master process to spawn workers. In this case, any threads started in the master
    process don't transfer over to workers, so they need to be restarted.
    """
    logger.debug("checking background threads")

    with MODULE_LOCK:
        # PERF: this is a critical section (inside of a lock). Be mindful!
        threads_by_name = {t.name: t for t in threading.enumerate()}
        _check_telemetry(threads_by_name)
        _check_heartbeat(threads_by_name)
        _check_server_settings_poll(threads_by_name)
        _check_reporting_client(threads_by_name, middleware)


def _check_telemetry(threads_by_name):
    # PERF: this is a critical section (inside of a lock). Be mindful!
    thread = threads_by_name.get(TELEMETRY_THREAD_NAME)
    if thread is not None or contrast.telemetry_disabled():
        return

    logger.debug(LOG_MSG, TELEMETRY_THREAD_NAME)
    contrast.TELEMETRY = Telemetry()
    contrast.TELEMETRY.start()


def _check_heartbeat(threads_by_name):
    # PERF: this is a critical section (inside of a lock). Be mindful!
    thread = threads_by_name.get(HEARTBEAT_THREAD_NAME)
    if thread is not None:
        return

    settings = Settings()
    logger.debug(LOG_MSG, HEARTBEAT_THREAD_NAME)
    settings.heartbeat = None
    settings.establish_heartbeat()


def _check_server_settings_poll(threads_by_name):
    # PERF: this is a critical section (inside of a lock). Be mindful!
    thread = threads_by_name.get(SERVER_SETTING_THREAD_NAME)
    if thread is not None:
        return

    settings = Settings()
    logger.debug(LOG_MSG, SERVER_SETTING_THREAD_NAME)
    settings.server_settings_poll = None
    settings.establish_server_settings_poll()


def _check_reporting_client(threads_by_name, middleware):
    # PERF: this is a critical section (inside of a lock). Be mindful!

    # something about ReportingClient being a singleton prevents it from being named
    # correctly (sometimes). The attempt to find the thread here is slower but necessary
    # TODO: PYT-1960 Revert this back to lookup by thread name only
    thread = {type(t): t for t in threads_by_name.values()}.get(ReportingClient)
    if thread is not None:
        return

    # the reporting client thread should always be running; there are no conditions here

    logger.debug(LOG_MSG, REPORTING_CLIENT_THREAD_NAME)
    ReportingClient.clear_instance()
    middleware.reporting_client = ReportingClient()
    middleware.reporting_client.start()
