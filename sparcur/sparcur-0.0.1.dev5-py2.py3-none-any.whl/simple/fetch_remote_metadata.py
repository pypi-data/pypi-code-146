#!/usr/bin/env python3
# [[file:../../docs/developer-guide.org::fetch_remote_metadata.py][fetch_remote_metadata.py]]
from joblib import Parallel, delayed
from sparcur.paths import Path
from sparcur.backends import PennsieveDatasetData


def _from_project_path_fetch_remote_metadata(project_path, n_jobs=12, cached_ok=False):
    if n_jobs <= 1:
        prepared = [PennsieveDatasetData(dataset_path.cache)
                    for dataset_path in project_path.children]
        [bdd() for bdd in prepared if not (cached_ok and bdd.cache_path.exists())]
    else:
        fetch = lambda bdd: bdd() if not (cached_ok and bdd.cache_path.exists()) else None
        fetch_path = (lambda path: fetch(PennsieveDatasetData(path.cache)))
        Parallel(n_jobs=n_jobs)(delayed(fetch_path)(dataset_path)
                 for dataset_path in project_path.children)


# fetch remote metadata
def from_path_fetch_remote_metadata(path, n_jobs=12, cached_ok=False):
    """ Given a path fetch remote metadata associated with that path. """

    cache = path.cache
    if cache.is_organization():
        _from_project_path_fetch_remote_metadata(path, n_jobs=n_jobs, cached_ok=cached_ok)
    else:  # dataset_path
        # TODO more granular rather than roll up to dataset if inside?
        bdd = PennsieveDatasetData(cache)
        if not (cached_ok and bdd.cache_path.exists()):
            bdd()


def main(path=Path.cwd(), n_jobs=12, rmeta_cached_ok=False, **kwargs):
    if path is None or path.find_cache_root() not in (path, *path.parents):
        from sparcur.simple.clone import main as clone
        path = clone(path=path, n_jobs=n_jobs, **kwargs)
        # NOTE path is passed along here, but kwargs is expected to contain
        # parent_path or parent_parent_path and project_id note that if that
        # happens then the path returned from clone will change accordingly

    from_path_fetch_remote_metadata(path, n_jobs=n_jobs, cached_ok=rmeta_cached_ok)
    return path


if __name__ == '__main__':
    from sparcur.simple.utils import pipe_main
    pipe_main(main)  # we probably don't print here?
# fetch_remote_metadata.py ends here
