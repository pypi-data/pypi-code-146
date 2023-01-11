# -*- coding: utf-8 -*-
# Copyright © 2023 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import threading
from contrast.agent import scope
from contrast.agent.settings import Settings
from contrast.reporting.teamserver_messages import ServerActivity
from contrast.reporting import ReportingClient
from contrast.utils.decorators import fail_loudly
from contrast.utils import service_util
from contrast.extern import structlog as logging

logger = logging.getLogger("contrast")
SERVER_SETTING_THREAD_NAME = "ContrastServerSettings"


class ServerSettingsPoll(threading.Thread):
    def __init__(self):
        self.stopped = False
        self.settings_interval_ms = Settings().config.server_settings_poll_interval
        # Agent should not ping too frequently
        if self.settings_interval_ms < 10000:
            self.settings_interval_ms = 10000

        self.reporting_client = ReportingClient()

        super().__init__()
        # A thread must have had __init__ called, but not start, to set daemon
        self.daemon = True
        self.name = SERVER_SETTING_THREAD_NAME

    def start(self):
        self.stopped = False
        super().start()

    @property
    def settings_interval_sec(self):
        return self.settings_interval_ms / 1000

    def run(self):
        # Ensure the server settings thread runs in scope because it is
        # initialized before our thread.start patch is applied.
        with scope.contrast_scope():
            logger.debug("Establishing Server Settings Thread")

            while not self.stopped and Settings().is_agent_config_enabled():
                self.send_server_settings()
                service_util.sleep(self.settings_interval_sec)

    @fail_loudly("Error sending a server settings message")
    def send_server_settings(self):
        """
        We're currently hitting the Server Activity endpoint to get our server
        features/ settings. This NG style endpoint will eventually be replaced
        with the true v1 Server Settings endpoint, so naming around it reflects
        that. The Server Activity message is always empty, so we're already
        only using it for settings, not reporting. The content of the message
        is for now deprecated java-only features.
        """
        if Settings().config is None:
            return
        self.reporting_client.send_message(ServerActivity())
