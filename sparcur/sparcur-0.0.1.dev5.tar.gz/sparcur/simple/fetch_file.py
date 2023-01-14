#!/usr/bin/env python3
# [[file:../../docs/developer-guide.org::fetch_file.py][fetch_file.py]]
def main(path=None, **kwargs):
    if path is not None:
        # FIXME this will fail if the remote for the file is not in
        # the current project, or if the cachedir is not a child of
        # the top level project directory e.g. in .operations/objects
        cache = path.cache
        cache.fetch(size_limit_mb=None)


if __name__ == '__main__':
    from sparcur.simple.utils import pipe_main
    pipe_main(main)
# fetch_file.py ends here
