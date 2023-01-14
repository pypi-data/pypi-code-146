#!/usr/bin/env python3
# [[file:../../docs/developer-guide.org::fetch_secondary.py][fetch_secondary.py]]
from sparcur.paths import Path
from sparcur.simple.fetch_files import from_path_fetch_files, filter_manifests


def from_blob_fetch_files(dataset_blob, path=None):
    # should the blob contain a reference to the path
    # it was derived from?
    filter_function = filter_manifests(dataset_blob)
    from_path_fetch_files(path, filter_function, n_jobs=n_jobs)


def main(path=Path.cwd(), n_jobs=12, **kwargs):
    #breakpoint()  # XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    # if not dataset_blob: get_blob vs path blob pairs?
    # starting from a partial blob means that this probably
    # should not kick off from the file system, but we know
    # that we will want to be able to kick it off from the
    # file system ... maybe the intermediate blobs can encode
    # the prov of where the file system reference they were
    # derived from lives ?
    dataset_blob = get_blob(path.cache_id)  # FIXME TODO
    from_blob_fetch_files(dataset_blob, path)


if __name__ == '__main__':
    from sparcur.simple.utils import pipe_main
    pipe_main(main)
# fetch_secondary.py ends here
