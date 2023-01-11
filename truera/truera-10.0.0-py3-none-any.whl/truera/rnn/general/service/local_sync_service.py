import os

from truera.rnn.general.service.container import Locator
from truera.rnn.general.service.sync_service import SyncService


class LocalSyncService(SyncService):
    '''
    Interface to communicate with the local repo.
    '''

    def __init__(self, config):
        super(LocalSyncService, self).__init__(config)

    def _listdir(self, fp):
        '''
        Lists files in a given directory, ignoring hidden files. 
        '''
        return [f for f in os.listdir(fp) if not f.startswith('.')]

    def push(self, locator: Locator):
        '''
        Pushes the items specified by the locator from the local cache to the backing storage
        Since the backing storage is the same as the cache, this is a no-op
        '''
        return

    def pull(self, locator: Locator):
        '''
        Pulls the items specified by the locator from the backing storage to the local cache
        Since the backing storage is the same as the cache, this is a no-op
        '''
        super(LocalSyncService, self).pull(locator)

    def list_projects(self):
        '''
        returns project folders, ignoring hidden directories
        '''
        return self._listdir(self.local_cache_path)

    def list_artifacts(self, project):
        '''
        returns each artifact as a list of [data_collection, split, model]
        '''
        return [
            name.split('--') for name in self.
            _listdir(os.path.join(self.local_cache_path, project, 'artifacts'))
        ]

    def list_data_collections(self, project):
        return self._listdir(
            os.path.join(self.local_cache_path, project, 'data_collections')
        )

    def list_datasplits(self, project, data_collection):
        return self._listdir(
            os.path.join(
                self.local_cache_path, project, 'data_collections',
                data_collection
            )
        )

    def list_models(self, project, use_artifact=False):
        """
        Args:
            project (string): project name
            use_artifact (bool, optional): set to True if machine only has access
                to output artifacts. Defaults to False.

        Returns:
            string list: model names for given project
        """
        if use_artifact:
            return [
                name.split('--')[2] for name in self._listdir(
                    os.path.join(self.local_cache_path, project, 'artifacts')
                )
            ]

        return self._listdir(
            os.path.join(self.local_cache_path, project, 'models')
        )
