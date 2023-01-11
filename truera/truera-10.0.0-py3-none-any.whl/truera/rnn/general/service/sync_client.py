import os
import pathlib

import yaml


class SyncClient(object):

    def __init__(
        self,
        backend='local',
        config_path=str(pathlib.Path(__file__).parent.absolute()) +
        '/config.yaml',
        **kwargs
    ):
        '''
        Client to setup backend sync service. Current supported backends are local and s3
        '''
        with open(config_path, 'r') as stream:
            config = yaml.safe_load(stream)
        self.config = config
        self.backend = backend
        ss = SyncClient.of_str(backend, config.get("use_external_services"))
        self.sync_service = ss(config, **kwargs)

    @classmethod
    def of_str(cls, s: str, use_metarepo=False):
        '''
        use_metarepo (bool) : set to True only if using metarepo-backed locators
        '''

        if use_metarepo:
            from truera.rnn.general.service.metarepo_sync_service import \
                MetarepoSyncService
            return MetarepoSyncService

        elif s == 'local':
            from truera.rnn.general.service.local_sync_service import \
                LocalSyncService
            return LocalSyncService

        elif s == 's3':
            from truera.rnn.general.service.s3_sync_service import \
                S3SyncService
            return S3SyncService

        elif s == 'az':
            from truera.rnn.general.service.az_sync_service import \
                AZSyncService
            return AZSyncService

        else:
            raise Exception(
                f'Backend {s} not recognized. Please use local, s3, or az.'
            )
