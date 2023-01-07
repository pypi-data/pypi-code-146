import subprocess


def _format_command(cmd: (str, list)) -> list:
    if not isinstance(cmd, (str, list)):
        raise ValueError(f"Command needs to be either string or list - got: {type(cmd)}")

    if isinstance(cmd, list):
        return cmd

    if cmd.find(' ') != -1:
        return cmd.split(' ')

    return [cmd]


def process(cmd: (str, list), timeout_sec: int = None, shell: bool = False) -> dict:
    try:
        with subprocess.Popen(
            _format_command(cmd),
            shell=shell,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        ) as p:
            b_stdout, b_stderr = p.communicate(timeout=timeout_sec)
            stdout, stderr, rc = b_stdout.decode('utf-8').strip(), b_stderr.decode('utf-8').strip(), p.returncode

    except (subprocess.TimeoutExpired, subprocess.SubprocessError, subprocess.CalledProcessError,
            OSError, IOError) as error:
        stdout, stderr, rc = None, str(error), 1

    return dict(
        stdout=stdout,
        stderr=stderr,
        rc=rc,
    )


def process_out_err(cmd: (str, list), timeout_sec: int = None, shell: bool = False) -> tuple:
    result = process(cmd=cmd, timeout_sec=timeout_sec, shell=shell)
    return result['stdout'], result['stderr']


def process_out(cmd: (str, list), timeout_sec: int = None, shell: bool = False) -> (str, None):
    return process(cmd=cmd, timeout_sec=timeout_sec, shell=shell)['stdout']


def process_err(cmd: (str, list), timeout_sec: int = None, shell: bool = False) -> (str, None):
    return process(cmd=cmd, timeout_sec=timeout_sec, shell=shell)['stderr']


def process_rc(cmd: (str, list), timeout_sec: int = None, shell: bool = False) -> int:
    return process(cmd=cmd, timeout_sec=timeout_sec, shell=shell)['rc']
