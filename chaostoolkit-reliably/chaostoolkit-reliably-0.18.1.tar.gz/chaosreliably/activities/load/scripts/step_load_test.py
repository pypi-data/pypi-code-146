import math
import os
from typing import Any, Optional

from locust import HttpUser, LoadTestShape, TaskSet, between, task


class UserTasks(TaskSet):
    @task
    def get_root(self) -> None:
        endpoint = os.getenv("RELIABLY_LOCUST_ENDPOINT")
        headers = {}

        bearer_token = os.getenv("RELIABLY_LOCUST_ENDPOINT_TOKEN", "").strip()
        if bearer_token:
            headers["Authorization"] = f"Bearer {bearer_token}"

        self.client.get(endpoint, headers=headers)


class WebsiteUser(HttpUser):
    wait_time = between(1, 10)
    tasks = [UserTasks]


class StepLoadShape(LoadTestShape):
    step_time = int(os.getenv("RELIABLY_LOCUST_STEP_TIME", 1))
    step_load = int(os.getenv("RELIABLY_LOCUST_STEP_LOAD", 1))
    spawn_rate = int(os.getenv("RELIABLY_LOCUST_SPAWN_RATE", 1))
    time_limit = int(os.getenv("RELIABLY_LOCUST_TIME_LIMIT", 5))

    def tick(self) -> Optional[Any]:
        run_time = self.get_run_time()

        if run_time > self.time_limit:
            return None

        current_step = math.floor(run_time / self.step_time) + 1
        return (current_step * self.step_load, self.spawn_rate)
