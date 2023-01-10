"""
Handles file transfer via the `scp` protocol
"""
import os

from remotemanager.transport.transport import Transport
from remotemanager.utils import ensure_list


class scp(Transport):
    """
    Class to handle file transfers using the scp protocol

    Args:
        url (URL):
            url to extract remote address from
    """

    def __init__(self,
                 *args,
                 **kwargs):

        super().__init__(*args, **kwargs)

        # flags can be exposed, to utilise their flexibility
        flags = kwargs.pop('flags', 'r')
        self.flags = flags

        self._transfers = {}

        self._cmd = '{password}scp {flags} {primary} {secondary}'

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
        def scp_join(files):
            return f' '.join([os.path.join(folder, f) for f in files])

        if isinstance(inp, str):
            raise ValueError('files is stringtype, '
                             'was a transfer forced into the queue?')

        inp = ensure_list(inp)

        if ':' not in folder:
            return scp_join(inp)
        remote, folder = folder.split(':')
        return f'{remote}:"{scp_join(inp)}"'

    @property
    def cmd(self):
        password = ''

        if self.url.passfile is not None:
            password = f'sshpass -f {self.url.passfile} '

        base = self._cmd.format(password=password,
                                flags=self.flags,
                                primary='{primary}',
                                secondary='{secondary}')
        self._logger.debug(f'returning semi-formatted cmd: "{base}"')
        return base
