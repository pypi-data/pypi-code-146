#!/usr/bin/env python3
# [[file:../../docs/developer-guide.org::*Fetch][Fetch:1]]
from sparcur.simple.fetch_metadata_files import main as files
from sparcur.simple.fetch_remote_metadata import main as rmeta


def main(path=Path.cwd(), **kwargs):
    if path is None or not path.find_cache_root() in (path, *path.parents):
        from sparcur.simple.pull import main as pull
        path = pull(path=path, n_jobs=n_jobs, **kwargs)

    # FIXME these can be run in parallel
    # python is not its own best glue code ...
    rmeta(path=path)
    files(path=path)
    return path


if __name__ == '__main__':
    from sparcur.simple.utils import pipe_main
    pipe_main(main, after=print)
# Fetch:1 ends here
