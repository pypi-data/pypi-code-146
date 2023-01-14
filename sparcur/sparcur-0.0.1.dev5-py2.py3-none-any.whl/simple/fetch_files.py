#!/usr/bin/env python3
# [[file:../../docs/developer-guide.org::fetch_files.py][fetch_files.py]]
import os
from sparcur.paths import Path
from sparcur.utils import _find_command
from sparcur.simple.utils import fetch_paths_parallel


def _datasets_with_extension(path, extension):
    """ Hack around the absurd slowness of python's rglob """

    # TODO query multiple extensions with -o at the same time
    command = fr"""for d in */; do
    {_find_command} "$d" \( -type l -o -type f \) -name '*.{extension}' \
    -exec getfattr -n user.bf.id --only-values "$d" \; -printf '\n' -quit ;
done"""

    with path:
        with os.popen(command) as p:
            string = p.read()

    has_extension = string.split('\n')
    datasets = [p for p in path.children if p.cache_id in has_extension]
    return datasets


def _from_path_fetch_files_simple(path, filter_function, fetch=True):
    files = filter_function(path)
    if fetch:
        [f.fetch(size_limit_mb=None) for f in files if not f.exists()]
        #Async(rate=5)(deferred(f.fetch)(size_limit_mb=None)
                      #for f in files if not f.exists())

    return files


def _from_path_fetch_files_parallel(path, filter_function, n_jobs=12):
    paths_to_fetch = _from_path_fetch_files_simple(path, filter_function, fetch=False)
    fetch_paths_parallel(paths_to_fetch, n_jobs=n_jobs)


def filter_extensions(extensions):
    """ return a function that selects files in a path by extension """
    def filter_function(path):
        cache = path.cache
        if cache.is_organization():
            paths = set()
            for ext in extensions:
                ds = _datasets_with_extension(path, ext)
                paths.update(ds)

        else:  # dataset_path
            paths = path,

        files = [matching  # FIXME stream ?
                for path in paths
                for ext in extensions
                for matching in path.rglob(f'*.{ext}')]
        return files

    return filter_function


def filter_manifests(dataset_blob):
    """ return a function that selects certain files listed in manifest records """
    # FIXME this needs a way to handle organization level?
    # NOTE this filter is used during the second fetch phase after the inital
    # metadata has been ingested to the point where it can be use to guide further fetches
    # TODO this is going to require the implementation of partial fetching I think
    # TODO preprocessing here?
    def filter_function(path):
        # TODO check that the path and the dataset blob match
        cache = path.cache
        if cache.id != dataset_blob['id']:
            msg = f'Blob is not for this path! {dataset_blob["id"]} != {cache.id}'
            raise ValueError(msg)

        files = []  # TODO get_files_for_secondary_fetch(dataset_blob)
        return files

    return filter_function


def from_path_fetch_files(path, filter_function, n_jobs=12):
    if n_jobs <= 1:
        _from_path_fetch_files_simple(path, filter_function)
    else:
        _from_path_fetch_files_parallel(path, filter_function, n_jobs=n_jobs)


def main(path=Path.cwd(), n_jobs=12, extensions=('xml',), **kwargs):
    #breakpoint()  # XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    if path is None or path.find_cache_root() not in (path, *path.parents):
        from sparcur.simple.pull import main as pull
        path = pull(path=path, n_jobs=n_jobs, **kwargs)

    filter_function = filter_extensions(extensions)

    from_path_fetch_files(path, filter_function, n_jobs=n_jobs)
    return path


if __name__ == '__main__':
    from sparcur.simple.utils import pipe_main
    pipe_main(main)
# fetch_files.py ends here
