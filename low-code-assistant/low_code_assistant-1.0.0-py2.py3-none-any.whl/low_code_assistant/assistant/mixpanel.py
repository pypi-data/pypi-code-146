import json
import logging
import os
import threading
import time
import uuid
from abc import ABC, abstractmethod
from typing import Dict, Optional
from urllib.parse import quote

import ipyvuetify as vy
import requests
import traitlets

from low_code_assistant import __version__
from low_code_assistant.domino_api import get_domino_api
from low_code_assistant.settings import settings

logger = logging.getLogger("low_code_assistant")


class IMixpanel(ABC):
    @abstractmethod
    def track(self, event: str, props: Optional[Dict] = None):
        pass

    def identify(self, unique_id: str):
        pass

    def track_with_defaults(self, event: str, properties: Optional[Dict] = None):
        props: Dict = {
            "LCA_version": __version__,
            "Domino_version": get_domino_api().get_domino_version(),
            "LCA_language": "python",
            **(properties or {}),
        }
        self.track(f"LCA {event}", props)


class NopMixpanel(IMixpanel):
    def track(self, event: str, props: Optional[Dict] = None):
        pass

    def identify(self, unique_id: str):
        pass


class MixpanelWidget(vy.VuetifyTemplate):
    template_file = (__file__, "mixpanel.vue")

    project_token = traitlets.Unicode().tag(sync=True)
    debug = traitlets.Bool(False).tag(sync=True)
    initialized = traitlets.Bool(False).tag(sync=True)
    unreachable_in_frontend = traitlets.Bool(False).tag(sync=True)
    frontend_props = traitlets.Dict().tag(sync=True)

    def track(self, event: str, props: Optional[Dict] = None):
        self.send({"method": "track", "args": [event, props]})

    def identify(self, unique_id: str):
        self.send({"method": "identify", "args": [unique_id]})


class FrontendMixpanel(IMixpanel):
    def __init__(self, w: MixpanelWidget):
        self.w = w

    def track(self, event: str, props: Optional[Dict] = None):
        self.w.track(event, props)

    def identify(self, unique_id: str):
        self.w.identify(unique_id)


class BackendMixpanel(IMixpanel):
    def __init__(self, project_token: str, frontend_props: Dict):
        self.project_token = project_token
        self.frontend_props = frontend_props
        self.unique_id = str(uuid.uuid4())
        self.user_id = None
        self.fail_count = 0
        self.lock = threading.Lock()

        try:
            info = get_domino_api().get_user_info()
            self.user_id = info["id"] if info else None
        except Exception as e:
            if settings.low_code_assistant_dev:
                logger.info(e)

    def track(self, event: str, props: Optional[Dict] = None):

        event_item = {
            "event": event,
            "properties": {
                "token": self.project_token,
                "time": int(round(time.time() * 1000)),
                "distinct_id": self.user_id or self.unique_id,
                "$insert_id": str(uuid.uuid4()),
                **(self.frontend_props or {}),
                **({"$user_id": self.user_id} if self.user_id else {}),
                **(props or {}),
            },
        }

        def run():
            try:
                requests.post(
                    "https://api.mixpanel.com/track/",
                    headers={"content-type": "application/x-www-form-urlencoded"},
                    data=f"data={quote(json.dumps([event_item]))}",
                    timeout=1,
                )
                with self.lock:
                    self.fail_count = 0
            except Exception as e:
                with self.lock:
                    self.fail_count += 1
                if settings.low_code_assistant_dev:
                    logger.info(e)

        with self.lock:
            if self.fail_count < 3:
                threading.Thread(target=run).start()

    def identify(self, unique_id: str):
        pass


mixpanel_widget = None
server_software = os.environ.get("SERVER_SOFTWARE", "")

if not (server_software and server_software.startswith("solara")):
    mixpanel_widget = MixpanelWidget(project_token="a442c4dbf420b59cdac95cfb07f57cbb", debug=False)

api: IMixpanel = FrontendMixpanel(mixpanel_widget) if mixpanel_widget else NopMixpanel()

if mixpanel_widget:

    def init(change):
        if change["new"]:
            info = get_domino_api().get_user_info()
            if info:
                unique_id = info["id"] if info else None
                if unique_id:
                    api.identify(unique_id)
            api.track_with_defaults("initialized")

    mixpanel_widget.observe(init, names="initialized")

    def unreachable(change):
        if change["new"]:
            global api
            if mixpanel_widget:
                api = BackendMixpanel(mixpanel_widget.project_token, mixpanel_widget.frontend_props)
                api.track_with_defaults("initialized")

    mixpanel_widget.observe(unreachable, names="unreachable_in_frontend")
