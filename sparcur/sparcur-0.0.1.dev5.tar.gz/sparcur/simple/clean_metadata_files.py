#!/usr/bin/env python3
# [[file:../../docs/developer-guide.org::clean_metadata_files.py][clean_metadata_files.py]]
from sparcur.paths import Path
from sparcur import datasets as dat
from sparcur.utils import symlink_latest
from sparcur.config import auth
from sparcur.simple.utils import rglob


def prepare_dataset_cleaned(dataset_path, cleaned_path=None, time_now=None):
    if cleaned_path is None:  # FIXME confusing and breaks w/ convention -> Options maybe?
        cleaned_path = Path(auth.get_path('cleaned-path'))

    from sparcur.utils import PennsieveId
    identifier = PennsieveId(dataset_path.cache.id)
    uuid = identifier.uuid
    cleaned_dataset_folder = cleaned_path / uuid
    cleaned_parent = cleaned_dataset_folder / time_now.START_TIMESTAMP_LOCAL_FRIENDLY
    if not cleaned_parent.exists():
        cleaned_parent.mkdir(parents=True)

    cleaned_latest = cleaned_dataset_folder / 'LATEST'
    # FIXME do we symlink before we know things have succeeded ???
    symlink_latest(cleaned_parent, cleaned_latest)
    return cleaned_parent


def from_dataset_path_metadata_file_paths(dataset_path):
    matches = []
    for candidate in rglob(dataset_path, '*.xlsx'):
        rp = candidate.relative_path_from(dataset_path)
        if not rp.parent.name or 'anifest' in rp.name:
            matches.append(candidate)

    return matches


def from_path_cleaned_object(path):
    t = dat.Tabular(path)
    sheet, wb, sparse_empty_rows = t._openpyxl_fixes()
    return wb


def from_file_paths_objects(paths):
    for path in paths:
        if path.suffix == '.xlsx':
            cleaned = from_path_cleaned_object(path)
            yield cleaned
        else:
            yield None


def from_dataset_path_cleaned_files(dataset_path, cleaned_parent):
    "NOTE this actually does the cleaning"

    paths = from_dataset_path_metadata_file_paths(dataset_path)
    for path, obj in zip(paths, from_file_paths_objects(paths)):
        if obj is not None:
            drp = path.dataset_relative_path
            target = cleaned_parent / drp
            if not target.parent.exists():
                target.parent.mkdir(parents=True)

            obj.save(target)


def main(path=Path.cwd(), id=None, time_now=None,
         parent_path=None, invariant_local_path='dataset',
         parent_parent_path=Path.cwd(),
         cleaned_path=None, cleaned_parent_path=None, **kwargs):
    # setup taken from path_metadata.py::main so check the notes there
    if path == Path.cwd() and (id is not None or parent_path is not None):
        if parent_path is None:
            uuid = id.uuid
            parent_path = parent_parent_path / uuid

        invariant_path = parent_path / invariant_local_path
        path = invariant_path.expanduser().resolve()
    else:
        parent_parent_path = None

    path = Path(path)
    cache = path.cache
    if not cache.is_dataset():
        raise TypeError('can only run on a single dataset')

    cleaned_parent = prepare_dataset_cleaned(path, cleaned_path, time_now)
    from_dataset_path_cleaned_files(path, cleaned_parent)


if __name__ == '__main__':
    import pprint
    from sparcur.simple.utils import pipe_main
    pipe_main(main, after=pprint.pprint)
# clean_metadata_files.py ends here
