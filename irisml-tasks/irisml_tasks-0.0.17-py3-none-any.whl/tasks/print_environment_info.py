import dataclasses
import logging
import sys
import subprocess
import irisml.core

logger = logging.getLogger(__name__)


class Task(irisml.core.TaskBase):
    """Print various environment information to stdout/stderr.

    This task is designed for Linux environment.

    Currently this task supports:
        - pip list
        - nvidia-smi
        - cat /proc/cpuinfo
        - free
    """
    VERSION = '0.1.0'
    CACHE_ENABLED = False

    @dataclasses.dataclass
    class Config:
        show_pip_info: bool = True
        show_cuda_info: bool = True
        show_cpu_info: bool = True
        show_memory_info: bool = True

    def execute(self, inputs):
        if self.config.show_pip_info:
            self._run_command(['pip', 'list'])

        if self.config.show_cuda_info:
            self._run_command(['nvidia-smi'])

        if self.config.show_cpu_info:
            self._run_command(['cat', '/proc/cpuinfo'])

        if self.config.show_memory_info:
            self._run_command(['free'])

        sys.stdout.flush()

    def dry_run(self, inputs):
        return self.execute(inputs)

    @staticmethod
    def _run_command(args):
        try:
            c = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            print(c.stdout)
            if c.returncode != 0:
                logger.warning(f"{args} returned non-zero exit status {c.returncode}")
        except Exception as e:
            logger.warning(f"Failed to run a command {args}. {e}")
