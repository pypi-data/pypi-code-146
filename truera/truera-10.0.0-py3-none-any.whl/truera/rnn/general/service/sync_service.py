import os
from pathlib import Path

from sumtypes import match

from truera.rnn.general.service.container import Locator
from truera.rnn.general.utils import log
from truera.rnn.general.utils.paths import find_in_parents
from truera.rnn.general.utils.strings import Stringable


class SyncService(Stringable, object):
    '''
    Interface to communicate with the repo. Current supported backends are local and s3
    '''

    def __init__(
        self, config, needs_local_proxy_cache=True, local_workspace_mode=False
    ):
        if needs_local_proxy_cache:
            if 'ARTIFACT_PROXY_HOME' in os.environ:
                log.info(
                    f"artifact proxy in env: {os.environ['ARTIFACT_PROXY_HOME']}"
                )
            else:
                home = find_in_parents(Path.cwd(), "artifact_proxy")
                if home is None:
                    raise Exception(
                        "cannot find artifact proxy; ARTIFACT_PROXY_HOME env variable needed"
                    )
                else:
                    log.info(f"found artifact_proxy in {home}")
                    os.environ['ARTIFACT_PROXY_HOME'] = str(home)
            self.local_cache_path = os.path.expandvars(
                config['local']['repo_path']
            )
            self.config = config
        elif local_workspace_mode:
            self.local_cache_path = config
            # TODO: self.config is currently unused for local_workspace_mode but is needed to export stuff (see export.export_pkl())
            # which is not yet supported in local_workspace_mode
            self.config = {}
        else:
            self.local_cache_path = os.path.expandvars(
                config['local']['repo_path']
            )
            self.config = config
        self.local_workspace_mode = local_workspace_mode

    def push(self, locator: Locator):
        '''
        Pushes the items specified by the locator from the local cache to the backing storage
        '''
        raise NotImplementedError

    def sync(self, locator: Locator):
        '''
        Syncs the items specified by the locator to/from the local cache to the backing storage
        '''
        raise NotImplementedError

    def pull(self, locator: Locator):
        '''
        Pulls the items specified by the locator from the backing storage to the local cache
        current supported locators: artifacts, split
        '''
        if type(locator) == Locator.Model:
            model_path = self.get_cache_path(
                Locator.Model(locator.project, locator.model)
            )
            if not os.path.exists(model_path + 'Empty_File'):
                self._make_empty_file(model_path)
        elif type(locator) == Locator.Split:
            split_path = self.get_cache_path(
                Locator.Split(
                    locator.project, locator.data_collection, locator.split
                )
            )
            if not os.path.exists(split_path + 'Empty_File'):
                self._make_empty_file(split_path)

    def list_projects(self):
        raise NotImplementedError

    def list_artifacts(self, project):
        raise NotImplementedError

    def list_data_collections(self, project):
        raise NotImplementedError

    def list_datasplits(self, project, data_collection):
        raise NotImplementedError

    def list_models(self, project):
        raise NotImplementedError

    def get_repo_path(self, locator: Locator, prefix: str) -> str:

        @match(Locator)
        class imp(object):

            def Artifact(project, model, data_collection, split):
                if data_collection is None or split is None or model is None:
                    raise Exception(
                        'Data collection, Split, and Model parameters must not be none'
                    )
                if self.local_workspace_mode:
                    return os.path.join(prefix, split)
                return os.path.join(
                    prefix, project, 'artifacts',
                    data_collection + '--' + split + '--' + model + '/'
                )

            def Split(project, data_collection, split):
                if data_collection is None or split is None:
                    raise Exception(
                        'Data collection and Split parameters must not be none'
                    )
                if self.local_workspace_mode:
                    raise NotImplementedError(
                        "Locating Split is not implemented in local_workspace_mode"
                    )
                return os.path.join(
                    prefix, project, 'data_collections', data_collection,
                    split + '/'
                )

            def DataCollection(project, data_collection):
                if data_collection is None:
                    raise Exception(
                        'Data collection parameter must not be none'
                    )
                if self.local_workspace_mode:
                    raise NotImplementedError(
                        "Locating DataCollection is not implemented in local_workspace_mode"
                    )
                return os.path.join(
                    prefix, project, 'data_collections', data_collection + '/'
                )

            def Model(project, model):
                if model is None:
                    raise Exception('Model parameter must not be none')
                if self.local_workspace_mode:
                    raise NotImplementedError(
                        "Locating Model is not implemented in local_workspace_mode"
                    )
                return os.path.join(prefix, project, 'models', model + '/')

            def Export(project, model, data_collection, split, filename):
                if data_collection is None or split is None or model is None:
                    raise Exception(
                        'Data collection, Split, and Model parameters must not be none'
                    )
                if self.local_workspace_mode:
                    raise NotImplementedError(
                        "Locating Export is not implemented in local_workspace_mode"
                    )
                return os.path.join(
                    prefix, project, 'exports', data_collection,
                    data_collection + '--' + split + '--' + model + '/'
                )

        return imp(locator)

    def get_cache_path(self, locator: Locator):
        '''
        Designates the local file storage for files categorized by type.
        Most folders are sibling folders to avoid accidental uploads/downloads of children folders
        '''
        return self.get_repo_path(locator, self.local_cache_path)

    def _make_empty_file(self, path):
        os.makedirs(path, exist_ok=True)
        with open(os.path.join(path, "Empty_File"), 'w') as fp:
            pass
