#!/usr/bin/env python3
# [[file:../../docs/developer-guide.org::dataset-path-metadata-validate][dataset-path-metadata-validate]]
# FIXME this is not really doing what we want yet
from sparcur.paths import Path
from sparcur.simple import path_metadata


def from_path_validated_json_metadata(path):
    tm = path_metadata.from_path_transitive_metadata(path)
    from_blob_validated_json_metadata(tm)
    return tm


def from_blob_validated_json_metadata(blob):
    """ Mutates in place. """
    Path.validate_path_json_metadata(blob)
    # perferred
    # accepted
    # banned
    # known
    # unknown


def main(_entry_point=False, **kwargs):
    # FIXME we want to be able to accept
    # --dataset-id, <json-file-to-validate>, and some other things probably?
    return path_metadata.main(validate=True, _entry_point=_entry_point, **kwargs)
    if export_path:
        from_blob_validate_path_json_metadata
    else:
        from_path_validate_path_json_metadata(path)


if __name__ == '__main__':
    #import pprint
    from sparcur.simple.utils import pipe_main
    pipe_main(main)#, after=pprint.pprint)
# dataset-path-metadata-validate ends here
