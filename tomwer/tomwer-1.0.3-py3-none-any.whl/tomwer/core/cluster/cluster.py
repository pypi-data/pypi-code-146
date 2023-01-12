# coding: utf-8
# /*##########################################################################
# Copyright (C) 2017-2021 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
#############################################################################*/

"""
Contains processing relative to a `Slurmcluster`
"""

__authors__ = ["H.Payno"]
__license__ = "MIT"
__date__ = "12/10/2021"


from tomwer.core.settings import SlurmSettings as _SlurmSettings


class SlurmClusterConfiguration:
    """Object shipping the configuration of a slurm cluster"""

    def __init__(
        self,
        n_cpu_per_task=_SlurmSettings.N_CORES_PER_TASK,
        n_tasks=_SlurmSettings.N_TASKS,
        memory=_SlurmSettings.MEMORY_PER_WORKER,
        queue=_SlurmSettings.PARTIION,
        n_gpus=_SlurmSettings.N_GPUS_PER_WORKER,
        project_name=_SlurmSettings.PROJECT_NAME,
        walltime=_SlurmSettings.DEFAULT_WALLTIME,
        python_venv=_SlurmSettings.PYTHON_VENV,
    ) -> None:
        self._n_cpu_per_task = n_cpu_per_task
        self._n_task = n_tasks
        self._memory = memory
        self._queue = queue
        self._n_gpus = n_gpus
        self._project_name = project_name
        self._walltime = walltime
        self._python_venv = python_venv

    @property
    def n_cpu_per_task(self):
        return self._n_cpu_per_task

    @property
    def n_task(self):
        return self._n_task

    @property
    def memory(self):
        return self._memory

    @property
    def queue(self):
        return self._queue

    @property
    def n_gpus(self):
        return self._n_gpus

    @property
    def project_name(self):
        return self._project_name

    @property
    def walltime(self):
        return self._walltime

    @property
    def python_venv(self):
        return self._python_venv

    @property
    def port_range(self) -> tuple:
        """port range as (start:int, strop:int, step: int)"""
        return self._port_range

    @property
    def dashboard_port(self):
        return self._dashboard_port

    def to_dict(self) -> dict:
        return {
            "cpu-per-task": self.n_cpu_per_task,
            "n_tasks": self.n_task,
            "memory": self.memory,
            "partition": self.queue,
            "n_gpus": self.n_gpus,
            "job_name": self.project_name,
            "walltime": self.walltime,
            "python_venv": self.python_venv,
        }

    @staticmethod
    def from_dict(dict_: dict):
        return SlurmClusterConfiguration().load_from_dict(dict_=dict_)

    def load_from_dict(self, dict_: dict):
        if "cpu-per-task" in dict_:
            self._n_cpu_per_task = dict_["cpu-per-task"]
        if "n_tasks" in dict_:
            self._n_task = dict_["n_tasks"]
        if "memory" in dict_:
            self._memory = dict_["memory"]
        if "partition" in dict_:
            self._queue = dict_["partition"]
        if "n_gpus" in dict_:
            self._n_gpus = dict_["n_gpus"]
        if "job_name" in dict_:
            self._project_name = dict_["job_name"]
        if "walltime" in dict_:
            self._walltime = dict_["walltime"]
        if "python_venv" in dict_:
            self._python_venv = dict_["python_venv"]
        if "port_range" in dict_:
            self._port_range = dict_["port_range"]
        if "dashboard_port" in dict_:
            self._dashboard_port = dict_["dashboard_port"]
        return self
