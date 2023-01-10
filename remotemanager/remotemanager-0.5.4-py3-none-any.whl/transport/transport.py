"""
Baseclass for any file transfer
"""
import os.path

from remotemanager.connection.url import URL
from remotemanager.storage.sendablemixin import SendableMixin
from remotemanager.utils import ensure_list, ensure_dir
from remotemanager.logging import LoggingMixin
from remotemanager.utils.flags import Flags


class Transport(SendableMixin, LoggingMixin):
    """
    Baseclass for file transfer

    Args:
        url (URL):
            url to extract remote address from
    """

    def __init__(self,
                 url: URL = None,
                 *args,
                 **kwargs):

        self._remote_address = None
        self._url = None
        self.set_remote(url)

        self._flags = Flags()
        self._transfers = {}

    def queue_for_push(self,
                       files: list,
                       local: str = None,
                       remote: str = None):
        """
        Queue file(s) for sending (pushing)

        Args:
            files (list[str], str):
                list of files (or file) to add to push queue
            local (str):
                local/origin folder for the file(s)
            remote (str):
                remote/destination folder for the file(s)
        Returns:
            None
        """
        self._logger.info(f'adding to PUSH queue')
        self.add_transfer(files, local, remote, 'push')

    def queue_for_pull(self,
                       files: list,
                       local: str = None,
                       remote: str = None):
        """
        Queue file(s) for retrieving (pulling)

        Args:
            files (list[str], str):
                list of files (or file) to add to pull queue
            local (str):
                local/destination folder for the file(s)
            remote (str):
                remote/origin folder for the file(s)
        Returns:
            None
        """
        self._logger.info(f'adding to PULL queue')
        self.add_transfer(files, remote, local, 'pull')

    def add_transfer(self,
                     files: list,
                     origin: str,
                     target: str,
                     mode: str):
        """
        Create a transfer to be executed. The ordering of the origin/target
        files should be considered as this transport instance being a
        "tunnel" between wherever it is executed (origin), and the destination
        (target)

        Args:
            files (list[str], str):
                list of files (or file) to add to pull queue
            origin (str):
                origin folder for the file(s)
            target (str):
                target folder for the file(s)
            mode (str: "push" or "pull"):
                transfer mode. Chooses where the remote address is placed
        Returns:
            None
        """
        modes = ('push', 'pull')
        if mode.lower() not in modes:
            raise ValueError(f'mode must be one of {modes}')

        if origin is None:
            origin = '.'
        if target is None:
            target = '.'

        # ensure dir-type
        origin = os.path.join(origin, '')
        target = os.path.join(target, '')

        if mode == 'push':
            pair = f'{origin}>{self._add_address(target)}'
        else:
            pair = f'{self._add_address(origin)}>{target}'

        files = [os.path.split(f)[1] for f in ensure_list(files)]

        self._logger.info(f'adding transfer: {split_pair(pair)[0]} '
                          f'-> {split_pair(pair)[1]}')
        self._logger.info(f'for files {files}')

        if pair in self._transfers:
            self._transfers[pair] = self._transfers[pair].union(set(files))
        else:
            self._transfers[pair] = set(files)

    def _add_address(self, dir: str) -> str:
        """
        Adds the remote address to the dir `dir` if it exists

        Args:
            dir (str):
                remote dir to have address appended

        Returns:
            (str) dir
        """
        if self.address is None:
            return dir
        return f'{self.address}:{dir}'

    @staticmethod
    def _format_for_cmd(folder: str, inp: list) -> str:
        """
        Formats a list into a bash expandable command with brace expansion

        Args:
            folder (str):
                the dir to copy to/from
            inp (list):
                list of items to compress

        Returns (str):
            formatted cmd
        """

        if isinstance(inp, str):
            raise ValueError('files is stringtype, '
                             'was a transfer forced into the queue?')

        if len(inp) > 1:
            return os.path.join(folder, '{' + ','.join(inp) + '}')
        return os.path.join(folder, inp[0])

    @property
    def transfers(self) -> dict:
        """
        Return the current transfer dict

        Returns (dict):
            {paths: files} transfer dict
        """
        return {k: sorted(list(v)) for k, v in self._transfers.items()}

    def print_transfers(self):
        """
        Print a formatted version of the current queued transfers

        Returns:
            None
        """
        i = 0
        for pair, files in self.transfers.items():
            i += 1
            print(f'transfer {i}:'
                  f'\norigin: {split_pair(pair)[0]}'
                  f'\ntarget: {split_pair(pair)[1]}')
            j = 0
            for file in files:
                j += 1
                print(f'\t({j}/{len(files)}) {file}')

    @property
    def address(self):
        """
        return the remote address

        Returns (str):
            the remote address
        """
        return self._remote_address

    @address.setter
    def address(self, remote_address):
        """
        set the remote address

        Returns:
            None
        """
        self._remote_address = remote_address

    @property
    def url(self):
        if self._url is not None:
            return self._url
        return URL()

    @url.setter
    def url(self, url):
        self._url = url

    def set_remote(self,
                   url: URL = None):
        """
        set the remote address with a URL object

        Returns:
            None
        """
        if url is None:
            self._remote_address = None
        elif url.is_local:
            self._remote_address = None
        else:
            self._remote_address = url.userhost
            self.url = url

    @property
    def flags(self):
        return self._flags

    @flags.setter
    def flags(self, new):
        self._flags = Flags(str(new))

    @property
    def cmd(self):
        """
        Returns a semi formatted command for issuing transfers. It is left to
        the developer to implement this method when adding more transport
        classes.

        The implementation should ideally be an "intermediate" format between
        the stored `Transport._cmd` string and the final format.

        At its most basic:

        ```
        @property
        def cmd(self):
            base = self._cmd.format(primary='{primary}',
                                    secondary='{secondary}')
            return base
        ```

        where self._cmd is a string of the format

        `command {primary} {secondary}`

        This allows any further injection such as the flags that
        `Transport.rsync` uses.

        Returns (str):
            the semi-formatted command for issuing a transfer
        """
        raise NotImplementedError

    def transfer(self,
                 dry_run: bool = False):
        """
        Perform the actual transfer

        Args:
            dry_run (bool):
                do not perform command, just return the command(s) to be
                executed

        Returns (str, None):
            the dry run string, or None
        """
        def get_remote_dir(path):
            if ':' not in path:
                return ''
            return path.split(':')[1]

        self._logger.info(f'executing a transfer')

        commands = []
        for pair, files in self.transfers.items():

            primary, secondary = split_pair(pair)

            remote_dir = get_remote_dir(secondary)
            if remote_dir == '':
                remote_dir = get_remote_dir(primary)

            primary = self._format_for_cmd(primary, files)

            base_cmd = self.cmd.format(primary=primary,
                                       secondary=secondary,
                                       remote_dir=remote_dir)

            commands.append(base_cmd)

        if dry_run:
            return commands

        for cmd in commands:
            self.url.cmd(cmd, local=True)
            # wipe the transfer queue
            self.wipe_transfers()

    def wipe_transfers(self):
        self._logger.info('wiping transfers')
        self._transfers = {}


def split_pair(pair: str) -> list:
    """
    Convert a "dir>dir" string into list format

    Args:
        pair (tuple):
            (dir, dir) tuple to be split

    Returns (list):
        [dir, dir]

    """
    return [ensure_dir(os.path.split(p)[0]) for p in pair.split('>')]
