from time import sleep

from rick.base import Di
from rick.mixin import Injectable, Runnable

from pokie.constants import DI_CONFIG


class IdleJob(Injectable, Runnable):
    DEFAULT_IDLE_INTERVAL = 15  # 15s between runs

    def __init__(self, di: Di):
        super().__init__(di)
        cfg = di.get(DI_CONFIG)
        self.interval = int(cfg.get("job_idle_interval", self.DEFAULT_IDLE_INTERVAL))

    def run(self, di: Di):
        sleep(self.interval)
