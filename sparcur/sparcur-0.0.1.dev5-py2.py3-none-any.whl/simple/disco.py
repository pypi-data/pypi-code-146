#!/usr/bin/env python3
# [[file:../../docs/developer-guide.org::disco.py][disco.py]]
import json
from pyontutils.core import OntGraph
from sparcur import export as ex
from sparcur.utils import PennsieveId
from sparcur.utils import fromJson, register_all_types  # FIXME this should also go in sparcron


def from_curation_export_json_path_xml_and_disco(curation_export_json_path):
    with open(curation_export_json_path, 'rt') as f:
        summary = json.load(f)

    datasets_json = summary['datasets']
    from_curation_export_json_path_datasets_json_xml_and_disco(
        curation_export_json_path, datasets_json)


def from_curation_export_json_path_datasets_json_xml_and_disco(
        curation_export_json_path, datasets_json, graphs=None):
    # FIXME need the snapshot linked somehow, export time started if we are using summary
    # or summary prov timestamp_export_start will give us the snapshot path as well if we
    # parse it back to a date
    if not graphs:
        snapshot_path = curation_export_json_path.parent / 'snapshot'
        paths = [(snapshot_path /
                  PennsieveId(d['id']).uuid /
                  'curation-export.ttl')
                 for d in datasets_json]
        graphs = [OntGraph().parse(path) for path in paths]

    datasets_ir = fromJson(datasets_json)
    ex.export_xml(curation_export_json_path, datasets_ir)
    ex.export_disco(curation_export_json_path, datasets_ir, graphs)
    # XXX not doing jsonld here, it will be combined
    # from single dataset jsonld or similar


def main(path=None, **kwargs):
    register_all_types()
    # FIXME the problem with this approach is that can cannot run
    # multiple downstream steps from the same upstream step, we would
    # need a compositional way to tell each downstream which upstreams
    # we wanted to run in any given situation, all to save additional
    # reads from disk
    if path is None:  # assume the user wants to run combine first
        from sparcur.simple.combine import main as combine
        curation_export_json_path, summary_all, _, graphs_all, _ = combine(**kwargs)
        datasets_json = summary_all['datasets']
        from_curation_export_json_path_datasets_json_xml_and_disco(
            curation_export_json_path, datasets_json, graphs)
    else:
        curation_export_json_path = path
        from_curation_export_json_path_xml_and_disco(curation_export_json_path)


if __name__ == '__main__':
    #import pprint
    from sparcur.simple.utils import pipe_main
    # these are really big, don't print them
    # pipe_main(main, after=pprint.pprint)
    pipe_main(main)
# disco.py ends here
