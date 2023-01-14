#!/usr/bin/env python3
# [[file:../../docs/developer-guide.org::export.py][export.py]]
import json
from socket import gethostname
import augpathlib as aug
from pyontutils.utils import timeformat_friendly
import sparcur
from sparcur.core import JEncode
from sparcur.paths import Path
from sparcur.utils import loge, symlink_latest
from sparcur.config import auth


def prepare_dataset_export(path, export_path=None):  # FIXME do we need export_base?
    if export_path is None:  # FIXME confusing and breaks w/ convention -> Options maybe?
        export_path = Path(auth.get_path('export-path'))  # FIXME allow alt?

    from sparcur.utils import PennsieveId
    identifier = PennsieveId(path.cache.id)
    uuid = identifier.uuid
    # we don't use cache._fs_safe_id here because we know the
    # identifier type from the folder structure
    # FIXME dataset metadata export setup basically needs to do all of this first
    # set latest run and then latest complete at the end, but complete is kind of arbitrary
    # from the atomic point of view
    tupdated = path.updated_cache_transitive()  # FIXME this causes us to traverse all files twice
    # XXX TODO I think that the dataset updated date is now transitive as well? though the dataset
    # updated timestamp seems to happen a bit before the created/updated date on the file itself?
    # FIXME somehow tupdated can be None !??!?! XXX yes, it happens on empty sparse datasets
    export_dataset_folder = export_path / 'datasets' / uuid
    export_parent = export_dataset_folder / timeformat_friendly(tupdated)
    if not export_parent.exists():
        export_parent.mkdir(parents=True)

    export_latest_run = export_dataset_folder / 'LATEST_RUN'
    symlink_latest(export_parent, export_latest_run)
    # FIXME need to symlink to LATEST
    return export_parent


def export_blob(blob, blob_file_name, time_now=None,
                export_path=None, export_parent_path=None, **kwargs):
    if export_parent_path is None:
        # NOTE if export_parent_path is not None then it is up to the user
        # to make sure that the contents of the dataset directory do not change
        # resulting in confusion about mismatched transitive update dates
        export_parent_path = prepare_dataset_export(path, export_path)
    elif not export_parent_path.exists():
        # safe to mkdir here since outside has a record of the path name
        export_parent_path.mkdir(parents=True)

    export_blob_path = export_parent_path / blob_file_name

    add_prov(blob, time_now)

    with open(export_blob_path, 'wt') as f:
        json.dump(blob, f, indent=2, cls=JEncode)

    loge.info(f'path metadata exported to {export_blob_path}')
    return export_blob_path


def add_prov(blob, time_now):
    """ Mutate blob in place to add prov. """
    # FIXME this will klobber cases where prov was embedded by the pipelines
    blob['prov'] = {'timestamp_export_start': time_now.START_TIMESTAMP,
                    'export_system_identifier': Path.sysid,
                    'export_hostname': gethostname(),
                    'sparcur_version': sparcur.__version__,
                    'sparcur_internal_version': sparcur.__internal_version__,
                    }
    rp = aug.RepoPath(sparcur.core.__file__)
    if rp.working_dir is not None:
        blob['prov']['sparcur_commit'] = rp.repo.active_branch.commit.hexsha


def main(path=Path.cwd(), export_path=None, **kwargs):
    return prepare_dataset_export(path, export_path=export_path)


if __name__ == '__main__':
    import pprint
    from sparcur.simple.utils import pipe_main
    pipe_main(main, after=pprint.pprint)
# export.py ends here
