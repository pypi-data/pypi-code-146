import warnings

from remotemanager.logging import LoggingMixin
from remotemanager.storage.sendablemixin import SendableMixin


class Dependency(SendableMixin, LoggingMixin):

    def __init__(self):
        self._logger.info('new Dependency created')

        self._network = []
        self._parents = []
        self._children = []

    def add_edge(self, primary, secondary):
        pair = (primary, secondary)
        if pair not in self._network:
            self._logger.info(f'adding new edge {pair}')

            self._parents.append(primary.short_uuid)
            self._children.append(secondary.short_uuid)

            self._network.append(pair)

    @property
    def network(self):
        return self._network

    def get_children(self, dataset):
        uuid = dataset.short_uuid

        tmp = []
        for i in range(len(self._parents)):
            if self._parents[i] == uuid:
                tmp.append(self.network[i][1])

        return tmp

    def get_parents(self, dataset):
        uuid = dataset.short_uuid

        tmp = []
        for i in range(len(self._children)):
            if self._children[i] == uuid:
                tmp.append(self.network[i][0])

        return tmp

    @property
    def ds_list(self):

        datasets = []
        for pair in self.network:
            for ds in pair:
                if ds not in datasets:
                    datasets.append(ds)

        return datasets

    def append_run(self, caller, *args, **kwargs):
        """
        Appends runs with the same args to all datasets

        Args:
            caller:
                (Dataset): The dataset which deferrs to the dependency
            *args:
                append_run args
            **kwargs:
                append_run keyword args

        Returns:
            None
        """
        self._logger.info(f'appending run from {caller}')

        datasets = self.ds_list
        self._logger.info(f'There are {len(datasets)} datasets in the chain')

        for ds in datasets:
            ds.append_run(dependency_call=True, *args, **kwargs)

        for ds in datasets:
            parents = self.get_parents(ds)
            if len(parents) > 1:
                warnings.warn('Multiple parents detected. '
                              'Variable passing in this instance is unstable!')
            for parent in parents:
                # TODO this is broken
                lstr = f'repo.loaded = repo.load("' \
                       f'{parent.runners[-1].resultfile}")'
                ds.runners[-1]._dependency_info['parent_import'] = lstr

            tmp = []
            for child in self.get_children(ds):
                tmp.append(f'import time')
                tmp.append(f'time.sleep(1)')
                tmp.append(f'repo.submit_child("'
                           f'{child.runners[-1].jobscript.name}")\n')
            ds.runners[-1]._dependency_info['child_submit'] = tmp

            ds.database.update(ds.pack())

    def run(self,
            *args,
            **kwargs):
        self._logger.info('dependency internal run call')

        ds_store = {}
        for ds in self.ds_list:
            ds_store[ds] = len(ds.runners)

        if not len(set(ds_store.values())) == 1:
            msg = f'Datasets do not have matching numbers of runners!: ' \
                  f'{ds_store}'
            self._logger.critical(msg)
            raise RuntimeError(msg)

        for ds in ds_store:
            ds._run(*args, **kwargs)
