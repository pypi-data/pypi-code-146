#!/usr/bin/env python3
# [[file:../../docs/developer-guide.org::fetch_metadata_files.py][fetch_metadata_files.py]]
from itertools import chain
from sparcur import exceptions as exc
from sparcur.utils import log, logd
from sparcur.paths import Path
from sparcur.datasets import DatasetStructure
from sparcur.simple.utils import fetch_paths_parallel, rglob

# fetch metadata files
fetch_prefixes = (
    ('dataset_description', 'glob'),
    ('subjects',            'glob'),
    ('samples',             'glob'),
    ('submission',          'glob'),
    ('manifest',           'rglob'),  # XXX NOTE the rglob here
)


def _from_path_fetch_metadata_files_simple(path, fetch=True):
    """ transitive yield paths to all metadata files, fetch them from
        the remote if fetch == True """
    for glob_prefix, glob_type in fetch_prefixes:
        if glob_type == 'rglob':
            gp0 = glob_prefix[0]
            pattern = f'[{gp0.upper()}{gp0}]{glob_prefix[1:]}*'
            yield from rglob(path, pattern)
            continue
        ds = DatasetStructure(path)
        for path_to_metadata in ds._abstracted_paths(glob_prefix,
                                                     glob_type=glob_type,
                                                     fetch=fetch):  # FIXME fetch here is broken
            yield path_to_metadata


def _from_path_fetch_metadata_files_parallel(path, n_jobs=12):
    """ Fetch all metadata files within the current path in parallel. """
    paths_to_fetch = _from_path_fetch_metadata_files_simple(path, fetch=False)
    try:
        first = next(paths_to_fetch)
        paths_to_fetch = chain((first,), paths_to_fetch)
    except StopIteration:
        log.warning('No paths to fetch, did you pull the file system metadata?')
        return

    # FIXME passing in a generator here fundamentally limits the whole fetching
    # process to a single thread because the generator is stuck feeding from a
    # single process, IF you materialize the paths first then the parallel fetch
    # can actually run in parallel, but bugs/errors encountered late in collecting
    # the paths will force all previous work to be redone
    # XXX as a result of this we use the posix find command to implement rglob
    # in a way that is orders of magnitude faster
    paths_to_fetch = list(paths_to_fetch)
    fetch_paths_parallel(paths_to_fetch, n_jobs=n_jobs)


def from_path_fetch_metadata_files(path, n_jobs=12):
    """ fetch metadata files located within a path """
    #if n_jobs <= 1:
        #gen = _from_path_fetch_metadata_files_simple(path)
        # FIXME broken ??? somehow abstracted paths doesn't fetch when
        # we run in directly, or somehow fetch_paths_parallel does something
        # different
        #paths = list(gen)
    #else:
    _from_path_fetch_metadata_files_parallel(path, n_jobs=n_jobs)


def main(path=Path.cwd(), n_jobs=12, **kwargs):
    if path is None or path.find_cache_root() not in (path, *path.parents):
        from sparcur.simple.pull import main as pull
        path = pull(path=path, n_jobs=n_jobs, **kwargs)

    from_path_fetch_metadata_files(path, n_jobs=n_jobs)
    return path


if __name__ == '__main__':
    from sparcur.simple.utils import pipe_main
    pipe_main(main, after=print)
# fetch_metadata_files.py ends here
