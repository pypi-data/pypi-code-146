#!/usr/bin/env python3
# [[file:../../docs/developer-guide.org::retrieve.py][retrieve.py]]
from sparcur.paths import Path
from sparcur.utils import symlink_latest
from sparcur.simple.clone import main as clone
from sparcur.simple.fetch_remote_metadata_all import main as remote_metadata
from sparcur.simple.pull import main as pull
from sparcur.simple.fetch_metadata_files import main as fetch_metadata_files
from sparcur.simple.fetch_files import main as fetch_files

def main(id=None,
         dataset_id=tuple(),
         parent_path=None,
         parent_parent_path=Path.cwd(),
         path=None,  # keep path out of kwargs
         invariant_local_path='dataset',
         #extensions=('xml',),  # not needed right now
         **kwargs):
    # FIXME parent_path and project_id seem like they probably need to
    # be passed here, it would be nice if project_path could just be
    # the current folder and if the xattrs are missing for the
    # project_id then ... it is somehow inject from somewhere else?
    # this doesn't really work, because that would mean that we would
    # have to carry the project id around in the xattr metadata for
    # all dataset folders, which might not be the worst thing, but
    # definitely redundant
    if id is None:
        raise TypeError('id is a required argument!')

    if parent_path is None:
        uuid = id.uuid  # FIXME hardcoded backend assumption
        parent_path = parent_parent_path / uuid
        parent_path.mkdir(exist_ok=True)
    elif not parent_path.exists():
        parent_path.mkdir()

    invariant_path = parent_path / invariant_local_path

    # XXX for now we do these steps in order here
    # rather than trusting that calling simple.pull.main will do
    # the right thing if there is no path ... it should but probably
    # doesn't right now due to assumptions about paths existing

    # remote metadata from path (could do from id too?)
    remote_metadata(id=id, **kwargs)  # could run parallel to clone, easier in bash
    # clone single without organization parent somehow seems likely broken?
    path = clone(id=id,
                 dataset_id=dataset_id,
                 parent_path=parent_path,
                 parent_parent_path=parent_parent_path,
                 **kwargs)  # XXX symlink_objects_to will just work if you pass it

    symlink_latest(path, invariant_path)

    # pull single
    pull(path=path, **kwargs)
    # fetch metadata files
    fetch_metadata_files(path=path, **kwargs)  # FIXME symlink_to
    # XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX fetch_metadata_files does NOT USE the extensions kwarg!
    # fetch additional files
    fetch_files(path=path)

    return path


if __name__ == '__main__':
    from sparcur.simple.utils import pipe_main
    pipe_main(main, after=print)
# retrieve.py ends here
