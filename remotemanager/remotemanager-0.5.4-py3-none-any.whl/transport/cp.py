"""
Handles file transfer via `cp`
"""

from remotemanager.transport.transport import Transport


class cp(Transport):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self._logger.info('created new cp transport')

        self._cmd = 'mkdir -p {secondary} ; ' \
                    'cp -r --preserve {primary} {secondary}'

    @property
    def cmd(self):
        base = self._cmd.format(primary='{primary}',
                                secondary='{secondary}')
        self._logger.debug(f'returning semi-formatted cmd: "{base}"')
        return base
