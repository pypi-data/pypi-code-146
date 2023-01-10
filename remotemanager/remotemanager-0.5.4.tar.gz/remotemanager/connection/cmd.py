import os
import subprocess
import getpass
import time
import warnings

from remotemanager.storage.sendablemixin import SendableMixin
from remotemanager.logging import LoggingMixin


def _process_redirect_file(file):
    if file is not None:
        return os.path.abspath(file)
    return None


def _clean_output(output):
    """
    Wrapper for the string.strip() method, allowing None

    Args:
        output:
            string (or None) to be handled

    Returns (str, None):
        cleaned cmd output
    """
    if output is None:
        return None
    return output.strip()


class CMD(SendableMixin, LoggingMixin):
    """
    This class stores a command to be executed, and the returned stdout, stderr

    Args:
        cmd (str):
            command to be executed
        asynchronous (bool):
            execute commands asynchronously
            defaults to False
        stdout (str):
            optional file to redirect stdout to
        stderr (str):
            optional file to redirect stderr to
        timeout (int):
            time to wait before issuing a timeout
        max_timeouts (int):
            number of times to attempt communication in case of a timeout
        force_file (bool):
            always use the fexec method if True
    """
    _temp_file = 'tmp_cmd.sh'

    def __init__(self,
                 cmd: str,
                 asynchronous: bool = False,
                 stdout: str = None,
                 stderr: str = None,
                 timeout: int = 5,
                 max_timeouts: int = 3,
                 raise_errors: bool = True,
                 force_file: bool = False):
        self._cmd = cmd
        self._subprocess = None
        self._async = asynchronous
        self._force_file = force_file
        self._redirect = {'stdout': _process_redirect_file(stdout),
                          'stderr': _process_redirect_file(stderr),
                          'execfile': None}

        if not asynchronous:
            initmsg = 'creating a new CMD instance'
        else:
            initmsg = 'creating a new asynchronous CMD instance'

        self._logger.info(initmsg)

        # timeout info
        self.timeout = timeout
        self.max_timeouts = max_timeouts
        self._timeout_current_tries = 0

        # prefer to raise an error, or continue
        self._raise_errors = raise_errors

        # supplementary data for post-exec
        self._cached = False
        self._stdout = None
        self._stderr = None
        self._whoami = None
        self._pwd = None
        self._pid = None

    def __repr__(self):
        stdout = self.stdout if self.stdout is not None else ''
        return stdout

    @property
    def sent(self) -> str:
        """
        The command passed at initialisation
        """
        return self._cmd.__repr__()

    @property
    def asynchronous(self) -> bool:
        """
        True if commands are to be executed asynchronously
        """
        return self._async

    @property
    def is_redirected(self) -> bool:
        """
        True if the cmd is redirected to a file
        """
        return any([self._redirect['stdout'], self._redirect['stderr']])

    @property
    def stdout(self) -> str:
        """
        Directly returns the stdout from the cmd execution. Attempts
        to communicate with the subprocess in the case of an async run.

        Returns None if the command has not been executed yet.

        Returns (str):
            the stdout from the command execution
        """
        return self.communicate()['stdout']

    @property
    def stderr(self) -> str:
        """
        Directly returns the stderr from the cmd execution. Attempts
        to communicate with the subprocess in the case of an async run.

        Returns None if the command has not been executed yet.

        Returns (str):
            the stdout from the command execution
        """
        return self.communicate(ignore_errors=True)['stderr']

    @property
    def pwd(self) -> str:
        """
        Present working directory at command execution

        Returns None if the command has not been executed yet.

        Returns (str):
            working dir of command execution
        """
        return self._pwd

    @property
    def whoami(self) -> str:
        """
        Present user at command execution

        Returns None if the command has not been executed yet.

        Returns (str):
            username who executed the command
        """
        return self._whoami

    @property
    def pid(self) -> int:
        """
        The Process ID of the spawned process

        Returns None if the command has not been executed yet.

        Returns (int):
            the PID of the spawned shell for this command
        """
        return self._pid

    @property
    def returncode(self) -> int:
        """
        Attempt to retrieve the returncode of the subprocess. This call will
        not disturb an asynchronous run, returning None

        Returns (int, None):
                The exit status of the subprocess, None if it is still running.
                None otherwise.
        """
        return self._subprocess.returncode

    @property
    def is_finished(self) -> bool:
        """
        Returns True if this command has finished execution. This will NOT talk
        to the process, as to not disturb async runs, so will always return
        False in those instances

        Returns (bool):
                True if the command has completed
        """
        return self.returncode is not None

    @property
    def succeeded(self) -> bool:
        """
        True if the command successfully executed

        Returns:
            None if not finished, True if returncode is 0
        """
        if not self.is_finished:
            return None
        return self.returncode == 0

    def exec(self) -> None:
        """
        Executes the command, storing execution info and in the
        case of a non-async run; returned values

        Returns:
            None
        """
        self._whoami = getpass.getuser()
        self._pwd = os.getcwd()

        if self.is_redirected:
            out = self._redirect['stdout']
            err = self._redirect['stderr']
            stdout = open(out, 'w+') if out is not None else None
            stderr = open(err, 'w+') if err is not None else None
        else:
            stdout = subprocess.PIPE
            stderr = subprocess.PIPE

        if self._force_file:
            return self._fexec(stdout, stderr)

        try:
            self._exec(stdout, stderr)
        except OSError as E:
            msg = 'Encountered an OSError on exec, attempting file exec'
            warnings.warn(msg)
            self._logger.warning(E)
            self._logger.warning(msg)
            self._fexec(stdout, stderr)

    def _exec(self,
              stdout,
              stderr) -> None:
        """
        Directly executes the command

        Args:
            stdout:
                stdout passthrough
            stderr:
                stderr passthrough

        Returns:
            None
        """
        self._logger.debug(f'executing command in {self.pwd}')
        self._logger.debug(f'"{self._cmd}"')

        hostexec = '/bin/bash' if os.name != 'nt' else None

        self._subprocess = subprocess.Popen(self._cmd,
                                            stdout=stdout,
                                            stderr=stderr,
                                            shell=True,
                                            text=True,
                                            executable=hostexec)
        self._pid = self._subprocess.pid
        if not self._async and not self.is_redirected:
            self._logger.debug('in-exec communication triggered')
            self.communicate()

    def _fexec(self,
               stdout,
               stderr) -> None:
        """
        Executes the command by first writing it to a file

        Args:
            stdout:
                stdout passthrough
            stderr:
                stderr passthrough

        Returns:
            None
        """
        file = CMD._temp_file
        with open(file, 'w+') as o:
            o.write(self._cmd)

        self._redirect['execfile'] = file

        self._subprocess = subprocess.Popen(f'bash {file}',
                                            stdout=stdout,
                                            stderr=stderr,
                                            shell=True,
                                            universal_newlines=True,
                                            executable='/bin/bash')
        self._pid = self._subprocess.pid

        if not self._async and not self.is_redirected:
            self._logger.debug('in-exec communication triggered')
            self.communicate()

    def communicate(self,
                    use_cache: bool = True,
                    ignore_errors: bool = False) -> dict:
        """
        Communicates with the subprocess, returning the stdout and stderr in
        a dict

        Args:
            use_cache (bool):
                use cached value if it is available
            ignore_errors (bool):
                do not raise error regardless of base setting

        Returns (dict):
                {'stdout': stdout, 'stderr': stderr}
        """
        if self._cached and use_cache:
            self._logger.info('using cached return values')
            return {'stdout': _clean_output(self._stdout),
                    'stderr': _clean_output(self._stderr)}
        elif not self.is_redirected:
            self._logger.info(f'communicating with process {self.pid}')
            std, err = self._communicate()
        else:
            self._logger.info('files are redirected, attempting to read')
            outfile = self._redirect['stdout']
            errfile = self._redirect['stderr']

            if outfile is not None:
                self._logger.debug(f'reading file {outfile}')
                with open(outfile, 'r') as o:
                    std = o.read().strip()
            else:
                self._logger.debug('outfile is None')
                std = None

            if errfile is not None:
                self._logger.debug(f'reading file {errfile}')
                with open(errfile, 'r') as e:
                    err = e.read().strip()
            else:
                self._logger.debug('errfile is None')
                err = None

        self._stdout = std
        self._stderr = err

        def format_output(string):
            if string is None:
                return

            if len(string.split('\n')) <= 1:
                return string

            return '\n'.join([f'  {line}' for line in string.split('\n')])

        self._logger.info(f'stdout from exec: |\n{format_output(std)}')
        if err:
            self._logger.warning(f'stderr from exec: |\n{format_output(err)}')

        if std or err:  # skip if all None
            self._logger.debug('caching results')
            self._cached = True

        if self._redirect['execfile']:
            tf = self._redirect['execfile']
            try:
                os.remove(tf)
                self._redirect['execfile'] = None
                self._logger.info(f'removed temp file {tf}')
            except FileNotFoundError:
                self._logger.info(f'temp file {tf} not found')
                pass

        if self._raise_errors \
                and not ignore_errors \
                and err is not None \
                and err != '':
            raise RuntimeError(f'received the following stderr: \n{err}')

        return {'stdout': _clean_output(std),
                'stderr': _clean_output(err)}

    def _communicate(self):
        """
        Attempt to communicate with the process, handling timeout

        Issues a Popen.communicate() with a timeout
        If this fails, will wait for (timeout * number of tries) seconds and
        try again. This continues until max_timeouts has been reached

        Returns (str, str):
            stdout, stderr
        """
        timeout = self.timeout
        self._timeout_current_tries += 1
        try:
            stdout, stderr = self._subprocess.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            print(f'({self._timeout_current_tries}/{self.max_timeouts}) '
                  f'communication attempt failed after {timeout}s',
                  end='... ')

            if isinstance(self.max_timeouts, int) \
                    and 0 < self.max_timeouts <= self._timeout_current_tries:
                print('could not communicate, killing for safety')
                self.kill()
                raise RuntimeError('could not communicate with process')

            waittime = timeout * self._timeout_current_tries

            print(f'waiting {waittime}s and trying again')
            time.sleep(waittime)

            return self._communicate()

        return stdout, stderr

    def kill(self) -> None:
        """
        Kill the process associated with this command, if one exists

        Returns:
            None
        """
        self._logger.info('received termination call')
        if self._subprocess is not None:
            self._logger.debug('_subprocess exists, sending kill()')
            self._subprocess.kill()
            self._logger.debug('polling process...')
            self._subprocess.poll()
            self._logger.debug('polling complete')
            return None
        self._logger.debug('process has not been launched yet')
