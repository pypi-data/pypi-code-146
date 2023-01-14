#!/usr/bin/env python3
# [[file:../../docs/developer-guide.org::dataset-path-metadata-extract][dataset-path-metadata-extract]]
from pathlib import Path


def from_path_transitive_metadata(path):
    tml = path._transitive_metadata()
    # FIXME TODO handle sparse cases
    return {'type': 'path-metadata',
            'data': tml,}


def main(path=Path.cwd(), id=None, time_now=None,
         parent_path=None, invariant_local_path='dataset',
         parent_parent_path=Path.cwd(),
         export_local=False, export_path=None, export_parent_path=None,
         _entry_point=False, validate=False, **kwargs):
    from sparcur.paths import Path
    from sparcur.simple.export import prepare_dataset_export, export_blob

    if path == Path.cwd() and (id is not None or parent_path is not None):
        if parent_path is None:
            uuid = id.uuid
            parent_path = parent_parent_path / uuid

        invariant_path = parent_path / invariant_local_path
        path = invariant_path.expanduser().resolve()
    else:
        parent_parent_path = None

    # TODO path from dataset_id and retrieve conventions? or just pass path from retrieve final output?
    # TODO parallelize if multiple paths
    # This assumes that all retrieve operations have
    # finished successfully for the current dataset
    # FIXME Options calls resolve on all paths but not if Path.cwd slips through ...
    path = Path(path)  # FIXME even here some paths don't have caches ?!
    cache = path.cache  # XXX this should have errored when Path was applied below !?!?!??! pipe_main wat ???
    if not cache.is_dataset():
        raise TypeError('can only run on a single dataset')

    if _entry_point:
        if export_parent_path is None:
            export_parent_path = prepare_dataset_export(path, export_path)

        kwargs.update({'export_path': export_path,
                       'export_parent_path': export_parent_path,
                       'time_now': time_now,})

    tm = from_path_transitive_metadata(path)
    # FIXME TODO validate file formats, which means this also needs to support the remoteless case
    # FIXME TODO process metadata for each timepoint when things enter should go in prov I think
    #    or we need to be collecting prov along the way, we don't have an overseer or conductor
    #    so we can't keep everything embedded
    # FIXME TODO embed the transitive cache updated value that is used in prepare_dataset_export
    if validate:  # FIXME raw vs validated and FIXME pipeline
        from sparcur import schemas as sc
        from sparcur.simple.transform import schema_validate
        Path.validate_path_json_metadata(tm)
        schema_validate(tm, sc.PathTransitiveMetadataSchema)

    if _entry_point:
        export_blob_path = export_blob(tm, 'path-metadata.json', **kwargs)  # FIXME naming for raw vs validated
        return export_blob_path
    else:
        return tm


if __name__ == '__main__':
    #import pprint
    from sparcur.simple.utils import pipe_main
    pipe_main(main)#, after=pprint.pprint)
# dataset-path-metadata-extract ends here
