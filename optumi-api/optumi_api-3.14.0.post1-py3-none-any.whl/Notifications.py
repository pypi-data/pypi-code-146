##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at https://www.optumi.com.
##


class Notifications:
    def __init__(
        self,
        channel: str = "sms",
        job_started: bool = False,
        job_failed: bool = False,
        job_completed: bool = False,
    ):
        self._channel = channel
        self._job_started = job_started
        self._job_failed = job_failed
        self._job_completed = job_completed

    @property
    def channel(self):
        return self._channel

    @property
    def job_started(self):
        return self._job_started

    @property
    def job_failed(self):
        return self._job_failed

    @property
    def job_completed(self):
        return self._job_completed

    def __str__(self):
        return (
            "job_started="
            + str(job_started)
            + ", job_failed="
            + str(job_failed)
            + ", job_completed="
            + str(job_completed)
        )
