#!/usr/bin/env python3
# [[file:../../docs/developer-guide.org::fetch_remote_metadata_all.py][fetch_remote_metadata_all.py]]
from joblib import Parallel, delayed
from sparcur.backends import PennsieveDatasetData
from sparcur.simple.utils import backend_pennsieve


def from_id_fetch_remote_metadata(id, project_id=None, n_jobs=12):
    """ given an dataset id fetch its associated dataset metadata """
    if id.type == 'organization':
        RemotePath = backend_pennsieve()
        project = RemotePath(id)
        prepared = [PennsieveDatasetData(r) for r in project.children]
        if n_jobs <= 1:
            [p() for p in prepared]
        else:
            # FIXME Paralle isn't really parallel here ...
            # can't use multiprocessing due to broken aug.RemotePath implementation
            # LOL PYTHON everything is an object, except when you want to pickle it
            # then some objects are more equal than others
            Parallel(n_jobs=n_jobs)(delayed(p._no_return)() for p in prepared)

    elif id.type == 'dataset':
        RemotePath = backend_pennsieve(project_id)
        dataset = RemotePath(id)
        bdd = PennsieveDatasetData(dataset)
        bdd()
    else:
        raise NotImplementedError(id)


def main(id=None,
         project_id=None,
         project_id_auth_var='remote-organization',  # FIXME move to clifun
         n_jobs=12,
         **kwargs):

    if project_id is None:
        from sparcur.utils import PennsieveId
        from sparcur.config import auth
        project_id = auth.get(project_id_auth_var)
        project_id = PennsieveId(project_id)  # FIXME abstract the hardcoded backend

    if id is None:
        id = project_id

    from_id_fetch_remote_metadata(id,
                                  project_id=project_id,
                                  n_jobs=n_jobs,)


if __name__ == '__main__':
    from sparcur.simple.utils import pipe_main
    pipe_main(main)  # nothing to print or do after
# fetch_remote_metadata_all.py ends here
