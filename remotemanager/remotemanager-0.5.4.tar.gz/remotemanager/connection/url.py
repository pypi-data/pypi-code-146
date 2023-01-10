"""
URL base class for connecting to remote systems
"""
import logging
import os
import typing

from remotemanager.logging.utils import format_iterable
from remotemanager.connection.cmd import CMD
from remotemanager.storage.sendablemixin import SendableMixin
from remotemanager.utils import ensure_list
from remotemanager.logging import LoggingMixin
from remotemanager.logging.verbosity import Verbosity


class URL(SendableMixin, LoggingMixin):
    """
    Container to store the url info for a Remote run

    The url should contain everything pertaining to the _remote_, allowing
    Dataset to be remote-agnostic

    Arguments:
        user (str):
            username for the remote system
        host (str):
            host address of the remote system
        port (int, str):
            port to connect to for ssh tunnels
        verbose (bool):
            base-verbosity for connections
        timeout (int):
            time to wait before issuing a timeout for cmd calls
        max_timeouts (int):
            number of times to attempt cmd communication in case of a timeout
        python (str):
            string used to initiate a python instance
        raise_errors (bool):
            set false to ignore errors by default in cmd calls
        passfile (str):
            absolute path to password file for sshpass
        kwargs:
            any extra args that may end up here from a Dataset or Computer are
            discarded
    """

    _localhost = 'localhost'

    def __init__(self,
                 user: str = None,
                 host: str = None,
                 port: int = None,
                 verbose: [int, Verbosity] = None,
                 timeout: int = 5,
                 max_timeouts: int = 3,
                 python: str = 'python',
                 raise_errors: bool = True,
                 passfile: str = None,
                 **kwargs):

        self._verbose = Verbosity(verbose)

        if host is None:
            host = URL._localhost
        self._conn = {'user': user,
                      'host': host,
                      'port': port}

        self.timeout = timeout
        self.max_timeouts = max_timeouts
        self.python = python

        self._passfile = passfile
        self._raise_errors = raise_errors
        self._ssh_override = None

        self._logger.info('new url created with url details:'
                          f'{format_iterable(self._conn)}')

    @property
    def raise_errors(self):
        return self._raise_errors

    @raise_errors.setter
    def raise_errors(self, r):
        self._raise_errors = r

    @property
    def verbose(self):
        return self._verbose

    @property
    def user(self) -> str:
        """
        Currently configured username
        """
        return self._conn['user']

    @user.setter
    def user(self, user):
        """
        Set the user attribute
        """
        self._conn['user'] = user

    @property
    def host(self) -> str:
        """
        Currently configured hostname
        """
        return self._conn['host'] or URL._localhost

    @host.setter
    def host(self, host):
        """
        Set the host attribute
        """
        self._conn['host'] = host

    @property
    def userhost(self) -> str:
        """
        `user@host` string if possible, just `host` if user is not present
        """
        if self.user is None:
            return self.host
        else:
            return f'{self.user}@{self.host}'

    @property
    def port(self) -> int:
        """
        Currently configured port (defaults to 22)
        """
        port = self._conn['port'] or 22
        return port

    @property
    def ssh(self) -> str:
        """
        ssh insert for commands on this connection
        """
        if self.is_local:
            return ''

        ret = []

        if self.passfile is not None:
            ret.append(f'sshpass -f {self.passfile}')

        if not self._ssh_override:
            ret.append(f'ssh -p {self.port}')
        else:
            return self._ssh_override

        ret.append(self.userhost)

        return ' '.join(ret)

    @ssh.setter
    def ssh(self,
            newssh: str) -> None:
        """
        Allows forced override of the ssh command

        Inserting extra flags into the ssh can be done as follows:

        >>> url = URL()
        >>> print(url.ssh)
        >>> "ssh"
        >>> url.ssh = "LANG=C " + url.ssh
        >>> print(url.ssh)
        >>> "LANG=C ssh"

        Args:
            newssh (str):
                new ssh string to insert

        Returns:
            None
        """
        self._ssh_override = newssh

    def clear_ssh_override(self):
        """
        Wipe any override applied to ssh. Can also be done by setting
        url.ssh = None

        Returns:
            None
        """
        self._ssh_override = None

    @property
    def passfile(self):
        if self._passfile is None:
            return

        p = self._passfile.replace('~', os.environ['HOME'])
        if not os.path.isfile(p):
            raise RuntimeError(f'could not find password file at '
                               f'{self._passfile}')

        return self._passfile

    @property
    def is_tunnel(self):
        """
        Uses the presence of an assigned port to determine if we are tunnelling
        or not

        Returns (bool):
           True if this is a tunnelled connection
        """
        return self._conn['port'] is not None

    @property
    def is_local(self):
        """
        True if this connection is purely local
        """
        host = self.host
        if host == URL._localhost:
            return True
        elif host.startswith('127.'):
            return True
        return False

    def cmd(self,
            cmd: str,
            asynchronous: bool = False,
            local: [bool, None] = None,
            stdout: str = None,
            stderr: str = None,
            timeout: int = None,
            max_timeouts: int = None,
            raise_errors: bool = None,
            dry_run: bool = False) -> typing.Union[CMD, str]:
        """
        Creates and executes a command

        Args:
            asynchronous (bool):
                run this command asynchronously
            cmd (str):
                command to execute
            local (bool, None):
                force a local or remote execution. Defaults to None
            stdout (str):
                optional file to redirect stdout to
            stderr (str):
                optional file to redirect stderr to
            timeout (int):
                time to wait before issuing a timeout
            max_timeouts (int):
                number of times to attempt communication in case of a timeout
            raise_errors (bool):
                override for global setting. Raise any stderr if encountered
            dry_run (bool):
                don't exec the command if True, just returns the string

        Returns (CMD):
            returned command instance
        """
        if local is not None and not local:
            self._logger.info('forced remote call; appending ssh to cmd')
            cmd = f"{self.ssh} '{cmd}'"
        elif local is None and not self.is_local:
            self._logger.info('implicit remote call; appending ssh to cmd')
            cmd = f"{self.ssh} '{cmd}'"
        if raise_errors is None:
            raise_errors = self._raise_errors

        timeout = self.timeout \
            if timeout is None else timeout
        max_timeouts = self.max_timeouts \
            if max_timeouts is None else max_timeouts

        if dry_run:
            return cmd.strip()

        thiscmd = CMD(cmd.strip(),
                      asynchronous=asynchronous,
                      stdout=stdout,
                      stderr=stderr,
                      timeout=timeout,
                      max_timeouts=max_timeouts,
                      raise_errors=raise_errors)
        thiscmd.exec()

        return thiscmd

    @property
    def utils(self):
        """
        Handle for the URLUtils module
        """
        if self.is_missing('_urlutils'):
            self._urlutils = URLUtils(self)
        return self._urlutils


class URLUtils:
    """
    Extra functions to go with the URL class, called via URL.utils

    As it requires a parent `URL` to function, and is instantiated with a
    `URL`, there is little to no purpose to using this class exclusively

    Arguments:
        parent (URL):
            parent class to provide utils to
    """
    def __init__(self, parent: URL):

        self._logger = logging.getLogger(__name__ + '.URLUtils')
        self._logger.info(f'creating a utils extension to parent: {parent}')

        self._parent = parent

    def file_mtime(self,
                   files: list,
                   local: bool = None,
                   python: bool = False) -> dict:
        """
        Check file modification times of [files]

        Args:
            files (list):
                list of paths to files
            local (bool):
                force a local search
            python (bool):
                ensure python style search is used

        Returns (dict):
            {file: mtime (unix)} dictionary
        """

        self._logger.info(f'performing stat on files: {files}')
        if local is None:
            local = self._parent.is_local

        files = ensure_list(files)
        times, error = self._file_mtime(files, local, python)
        self._logger.info('received:')
        self._logger.info(times)
        self._logger.info(error)
        output = {}
        for file in files:
            if file in times:
                output[file] = times[file]

            else:
                output[file] = None

        return output

    def _file_mtime(self,
                    files: list,
                    local: bool = None,
                    python: bool = False):
        """
        Perform the "stat -c %Y" command on a list of files,
        returning the result. Uses a python command backup if this fails

        Args:
            files (list):
                list of files to check
            local (bool):
                force a local search
            python (bool):
                force the python override

        Returns:
            (list): list of file unix times
        """
        sep = ','

        def stat():
            self._logger.debug('attempting raw stat command on files')
            basecmd = f'stat -c %n{sep}%Y'
            if len(files) == 1:
                cmd = f'{basecmd} {files[0]}'
            else:
                cmd = f'{basecmd} {{' + ','.join(files) + '}'

            ret = self._parent.cmd(cmd,
                                   local=local,
                                   raise_errors=False)

            times = {}
            for line in ret.stdout.split('\n'):
                try:
                    times[line.split(sep)[0]] = int(float(line.split(sep)[1]))
                except IndexError:
                    pass

            return times, ret.stderr.split('\n'), ret.returncode, ret.stderr

        def pystat():
            self._logger.debug('attempting python stat on files')
            ex = f"""import os
files={files}
for f in files:
\ttry: print(f'{{f}}{sep}{{os.stat(f).st_mtime}}') 
\texcept FileNotFoundError: print(f)"""

            cmd = f'{self._parent.python} -c "{ex}"'

            ret = self._parent.cmd(cmd,
                                   local=local,
                                   raise_errors=False)

            times = {}
            error = []
            for line in ret.stdout.split('\n'):
                try:
                    times[line.split(sep)[0]] = int(float(line.split(sep)[1]))
                except IndexError:
                    error.append(line.strip())

            return times, error

        files = ensure_list(files)

        if not python:
            t, e, returncode, stderr = stat()
            if returncode in [126, 127] or 'illegal option' in stderr:
                self._logger.warning('stat failed, falling back on python')
                return pystat()

            return t, e

        return pystat()

    def file_presence(self,
                      files: list,
                      local: bool = None) -> dict:
        """
        Search for a list of files, returning a boolean presence dict

        Args:
            files (list):
                list of paths to files
            local (bool):
                force a local search

        Returns (dict):
            {file: present} dictionary
        """
        self._logger.info(f'checking for presence of files: {files}')
        if local is None:
            local = self._parent.is_local

        files = ensure_list(files)

        times = self.file_mtime(files,
                                local=local)

        return {f: times[f] is not None for f in files}

    def search_folder(self,
                      files: list,
                      folder: str,
                      local: bool = None) -> dict:
        """
        Search `folder` for `files`, returning a boolean presence dict

        Arguments:
            files (list):
                list of filenames to check for. Optionally, a string for a
                single file
            folder (str):
                folder to scan
            local (bool):
                perform the scan locally (or remotely)

        Returns (dict):
            {file: present} dictionary
        """
        if local is None:
            local = self._parent.is_local
        fpath = os.path.abspath(folder)  # not locally available ?

        self._logger.debug(f'scanning folder {fpath}')
        self._logger.debug('searching for files:')
        self._logger.debug(f'{format_iterable(files)}')

        ls_return = self.ls(fpath, local=local, as_list=True)

        scan = [os.path.basename(f) for f in ls_return]

        self._logger.debug('scan sees:')
        self._logger.debug(f'{format_iterable(scan)}')

        if isinstance(files, str):
            self._logger.info('files is a string, running in singular mode')
            ret = {files: os.path.basename(files) in scan}
        else:
            ret = {file: os.path.basename(file) in scan for file in files}

        return ret

    def touch(self,
              file: str,
              local: bool = None,
              raise_errors: bool = None) -> CMD:
        """
        perform unix `touch`, creating or updating `file`

        Arguments:
            file (str):
                filename or path to file
            local (bool):
                force local (or remote) execution
            raise_errors (bool):
                raise any stderr encountered

        Returns (CMD):
            CMD instance for the command
        """
        if local is None:
            local = self._parent.is_local
        self._logger.debug(f'utils touch on file {file}')
        fname = os.path.abspath(file)
        return self._parent.cmd(f'touch {fname}',
                                local=local,
                                raise_errors=raise_errors)

    def mkdir(self,
              file: str,
              local: bool = None,
              raise_errors: bool = None) -> CMD:
        """
        perform unix `mkdir -p`, creating a folder structure

        Arguments:
            file (str):
                name or path to folder
            local (bool):
                force local (or remote) execution
            raise_errors (bool):
                raise any stderr encountered

        Returns (CMD):
            CMD instance for the command
        """
        if local is None:
            local = self._parent.is_local
        self._logger.debug(f'utils mkdir on path {file}')
        fname = os.path.abspath(file)
        # print(f'making dir {fname}')
        return self._parent.cmd(f'mkdir -p {fname}',
                                local=local,
                                raise_errors=raise_errors)

    def ls(self,
           file: str,
           as_list: bool = True,
           local: bool = None,
           raise_errors: bool = None) -> [CMD, list]:
        """
        Identify the files present on the directory

        Arguments:
            file (str):
                name or path to folder.
            as_list (bool):
                convert to a list format
            local (bool):
                force local (or remote) execution
            raise_errors (bool):
                raise any stderr encountered

        Returns (CMD, list):
            CMD instance for the command, or the list if as_list is True
        """
        if local is None:
            local = self._parent.is_local
        self._logger.debug(f'utils ls on path {file}')
        fname = os.path.abspath(file) if local else file

        ret = self._parent.cmd(f'ls {fname}',
                               local=local,
                               raise_errors=raise_errors)

        if as_list:
            ret = [f for f in ret.stdout.split('\n') if f != '']
        return ret
