import logging
import subprocess


class CommandExecutor:
    """ Utility class to help execute shell commands """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def simple_exec_command(self, command: str) -> subprocess.CompletedProcess:
        self.logger.info("=== Running command '%s'", command)
        completedProcess = subprocess.run(
            ["bash", "-c", command], capture_output=True, text=True
        )

        self.logger.info('returncode: {:d}'.format(completedProcess.returncode))
        self.logger.info(
            'stdout: {:s}'.
            format(completedProcess.stdout if completedProcess.stdout else '')
        )
        self.logger.error(
            'stderr: {:s}'.
            format(completedProcess.stderr if completedProcess.stderr else '')
        )
        return completedProcess
