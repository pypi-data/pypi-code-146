# -*- coding: utf-8 -*-
# Copyright © 2023 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import threading
from contrast.agent import scope
from contrast.agent.settings import Settings
from contrast.utils.decorators import fail_loudly
from contrast.utils import service_util
from contrast.utils.timer import now_ms

from contrast.extern import structlog as logging

logger = logging.getLogger("contrast")
HEARTBEAT_THREAD_NAME = "ContrastHeartbeat"


class Heartbeat(threading.Thread):
    def __init__(self):
        self.stopped = False
        self.heartbeat_interval_ms = (
            Settings().config.application_activity_polling_interval
        )
        # Agent should not ping too frequently
        if self.heartbeat_interval_ms < 10000:
            self.heartbeat_interval_ms = 10000

        super().__init__()
        # A thread must have had __init__ called, but not start, to set daemon
        self.daemon = True
        self.name = HEARTBEAT_THREAD_NAME

    def start(self):
        self.stopped = False
        super().start()

    @property
    def settings_interval_sec(self):
        return self.heartbeat_interval_ms / 1000

    def run(self):
        # Ensure the heartbeat thread runs in scope because it is initialized
        # before our thread.start patch is applied.
        with scope.contrast_scope():
            logger.debug("Establishing heartbeat")

            while not self.stopped and Settings().is_agent_config_enabled():
                self.send_heartbeat()
                service_util.sleep(self.settings_interval_sec)

    @fail_loudly("Error sending a heartbeat message")
    def send_heartbeat(self):
        from contrast.agent import service_client

        heartbeat_interval_ms = self.heartbeat_interval_ms
        settings = Settings()
        # only send after we have not updated after the last interval time set in the config
        if (
            settings.last_update_service is not None
            and (now_ms() - settings.last_update_service) > heartbeat_interval_ms
        ):
            if settings.config.is_service_bypassed:
                if Settings().config is None:
                    return

                from contrast.reporting import ReportingClient
                from contrast.reporting.teamserver_messages import HeartBeat

                client = ReportingClient()
                client.send_message(HeartBeat())
            else:
                service_client.send_heartbeat_message()
