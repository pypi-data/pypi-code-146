#!/usr/bin/env python3
# [[file:../../docs/developer-guide.org::pull.py][pull.py]]
from joblib import Parallel, delayed
from sparcur.paths import Path
from sparcur.utils import GetTimeNow


# pull dataset
def from_path_dataset_file_structure(path, time_now=None, exclude_uploaded=False):
    """ pull the file structure and file system metadata for a single dataset
        right now only works from a dataset path """

    if time_now is None:
        time_now = GetTimeNow()

    path._pull_dataset(time_now, exclude_uploaded)


# pull all in parallel
def from_path_dataset_file_structure_all(project_path,
                                         *args,
                                         paths=None,
                                         time_now=None,
                                         n_jobs=12,
                                         exclude_uploaded=False):
    """ pull all of the file structure and file system metadata for a project
        paths is a keyword argument that accepts a list/tuple of the subset of
        paths that should be pulled """

    if time_now is None:
        time_now = GetTimeNow()

    project_path.pull(
        paths=paths,
        time_now=time_now,  # TODO
        debug=False,  # TODO
        n_jobs=n_jobs,
        log_level='DEBUG' if False else 'INFO',  # TODO
        Parallel=Parallel,
        delayed=delayed,
        exclude_uploaded=exclude_uploaded,)


# mark datasets as sparse 
def sparse_materialize(path, sparse_limit:int=None):
    """ given a path mark it as sparse if it is a dataset and
        beyond the sparse limit """

    cache = path.cache
    if cache.is_organization():
        # don't iterate over cache children because that pulls remote data
        for child in path.children:
            sparse_materialize(child, sparse_limit=sparse_limit)
    else:
        cache._sparse_materialize(sparse_limit=sparse_limit)


def main(path=Path.cwd(),
         time_now=None,
         sparse_limit:int=None,
         n_jobs=12,
         exclude_uploaded=False,
         **kwargs):
    if path != path.resolve():
        raise ValueError(f'Path not resolved! {path}')

    project_path = None  # path could be None so can't find_cache_root here
    if path is None or path.find_cache_root() not in (path, *path.parents):
        from sparcur.simple.fetch_remote_metadata import main as remote_metadata
        project_path = remote_metadata(path=path, **kwargs)  # transitively calls clone
    else:
        project_path = path.find_cache_root()
        if path != project_path:
            # dataset_path case
            sparse_materialize(path, sparse_limit=sparse_limit)
            from_path_dataset_file_structure(path, time_now=time_now, exclude_uploaded=exclude_uploaded)
            if path == Path.cwd():
                print('NOTE: you probably need to run `pushd ~/ && popd` '
                      'to get a sane view of the filesystem if you ran this'
                      'from within a dataset folder')
            return path

    if not list(project_path.children):
        raise FileNotFoundError(f'{project_path} has no children.')
        # somehow clone failed
        # WARNING if rmeta failed you may get weirdness  # FIXME
        from sparcur.simple.clone import _from_project_path_top_level
        _from_project_path_top_level(project_path)

    sparse_materialize(project_path,
                       sparse_limit=sparse_limit)
    from_path_dataset_file_structure_all(project_path,
                                         time_now=time_now,
                                         n_jobs=n_jobs,
                                         exclude_uploaded=exclude_uploaded)
    return project_path


if __name__ == '__main__':
    from sparcur.simple.utils import pipe_main
    pipe_main(main, after=print)
# pull.py ends here
