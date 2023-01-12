# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import os
from azureml.train.automl.runtime._dask.constants import Constants
from azureml.train.automl.runtime._dask.dask_processes.dask_process_controller import DaskProcessController


class DaskWorker:
    """Handles Dask worker  operations."""

    def __init__(self):
        self._worker_process = DaskProcessController()

    def start(self,
              scheduler_ip: str,
              worker_per_core: bool = True) -> None:
        """Start the worker."""

        proc_count = 1
        thread_count = 1
        parallel_count = 1

        cpu_count = os.cpu_count()
        if cpu_count is not None:
            parallel_count = int(max(1, cpu_count / 4))

        if worker_per_core:
            proc_count = parallel_count
        else:
            thread_count = parallel_count

        memory_per_worker = float(1 / proc_count)

        self._worker_process.start_process(
            'dask-worker',
            ['tcp://{}:{}'.format(scheduler_ip, Constants.SCHEDULER_PORT)],
            {
                'nprocs': str(proc_count),
                'nthreads': str(thread_count),
                'memory-limit': str(memory_per_worker),
                'death-timeout': '30'
            }
        )

    def wait(self) -> None:
        """Wait for the worker to termminate."""
        self._worker_process.wait()
