import os
import sys
import logging
import subprocess
from typing import List


def run(cmd: List[str]) -> str:
    """Execute external program.

    :params cmd: Command to execute.

    :return: Output from stdout.
    """

    log = logging.getLogger('rich')

    try:
        proc = subprocess.Popen(cmd,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                encoding='utf-8')

        stdout, stderr = proc.communicate()

        if proc.returncode != 0:
            log.error(stderr)
            log.error(f'Return code: {proc.returncode}')
            sys.exit(1)
    except OSError as e:
        print(e)
        log.error(stderr)
        log.error('Failed to execute command.')
        sys.exit(1)

    return stdout


def check_dependencies(programs: List[str], exit_on_fail: bool = True):
    """Check if programs are on the system path.

    :param programs: Names of executable programs.
    :param exit_on_fail: Exit program with error code -1 if any program in not on path.

    :return: True if all programs are on path, else False.
    """

    for program in programs:
        if not check_on_path(program, exit_on_fail):
            return False

    return True


def check_on_path(program: str, exit_on_fail: bool = True):
    """Check if program is on the system path.

    :param programs: Names of executable programs.
    :param exit_on_fail: Exit program with error code -1 if any program in not on path.

    :return: True if all program is on path, else False.
    """

    if which(program):
        return True

    if exit_on_fail:
        print(f'{program} is not on the system path.')
        sys.exit(1)

    return False


def which(program: str):
    """Return path to program.

    This is a Python implementation of the linux
    command 'which'.

    http://stackoverflow.com/questions/377017/test-if-executable-exists-in-python

    :param programs: Names of executable programs.

    :return: Path to executable, or None if it isn't on the path.
    """

    fpath, _fname = os.path.split(program)
    if fpath:
        if is_executable(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_executable(exe_file):
                return exe_file

    return None


def is_executable(fpath: str):
    """Check if file is executable.

    :param fpath: Path to file.

    :return: True if executable, else False.
    """

    return os.path.isfile(fpath) and os.access(fpath, os.X_OK)
