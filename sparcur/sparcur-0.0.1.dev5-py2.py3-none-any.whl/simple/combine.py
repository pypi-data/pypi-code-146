#!/usr/bin/env python3
# [[file:../../docs/developer-guide.org::combine.py][combine.py]]
import json
import rdflib
from pathlib import Path
from dateutil import parser as dateparser
from pyontutils.core import OntResPath
from pyontutils.utils import TZLOCAL, timeformat_friendly
from pyontutils.namespaces import TEMP, rdf, sparc
#from sparcur.utils import fromJson, register_all_types  # FIXME this should also go in sparcron
from sparcur.export.triples import TriplesExportSummary
from sparcur.export.published import _merge_graphs
from sparcur.simple.export import add_prov

tu = 'timestamp_updated'
tuc = 'timestamp_updated_contents'
ip = 'inputs'
rmk = 'remote_dataset_metadata'


class TriplesExportSummaryPublished(TriplesExportSummary):

    @property
    def ontid(self):
        return rdflib.URIRef(super().ontid.replace('ontologies/', 'ontologies/published/'))

    @property
    def header_label(self):
        return rdflib.Literal(f'{self.folder_name} curation export published graph')


def max_dataset_or_contents_updated(datasets_list):
    return max(set.union(
        set([a['meta'][tuc] for a in datasets_list
            if tuc in a['meta'] and a['meta'][tuc]]),
        set([a['meta'][tu] for a in datasets_list
            if tu in a['meta'] and a['meta'][tu]])))


def from_dataset_export_path_snapshot(dataset_export_path, snapshots_path, time_now):
    derefs = [l.resolve() for l in [c / 'LATEST' for c in dataset_export_path.children] if l.exists()]
    snapshot_path = snapshots_path / time_now.START_TIMESTAMP_LOCAL_FRIENDLY
    snapshot_path.mkdir(parents=True)
    [(snapshot_path / d.parts[-2]).symlink_to((snapshot_path / 'asdf').relative_path_to(d)) for d in derefs]
    return snapshot_path


def from_snapshot_path_datasets_lists(snapshot_path):
    alld = []
    pubd = []
    for uuid_path in snapshot_path.children:
        with open(uuid_path / 'curation-export.json', 'rt') as f:
            j = json.load(f)
            # TODO validate the load XXX this should probably
            # happen as a final roundtrip check during export
            # TODO filter by organization
            alld.append(j)
            if ip in j and rmk in j[ip] and 'id_published' in j[ip][rmk]:
                pubd.append(j)

    return alld, pubd


def from_snapshot_path_summary_json(snapshot_path, project_id, time_now):
    l_all, l_pub = from_snapshot_path_datasets_lists(snapshot_path)
    sum_all = from_datasets_list_summary_json(l_all, project_id, time_now)
    sum_pub = from_datasets_list_summary_json(l_pub, project_id, time_now)
    return sum_all, sum_pub


def from_snapshot_path_summary_ttl(snapshot_path, project_id, time_now, blob):
    tes = TriplesExportSummary(blob)
    tesp = TriplesExportSummaryPublished(blob)

    orps = [OntResPath(uuid_path / 'curation-export.ttl')
            for uuid_path in sorted(snapshot_path.children, key=lambda p: p.name)]

    graphs_all = [o.graph for o in orps]
    graphs_pub = [
        g for g, doi in [(g, list(g[ds:TEMP.hasDoi]))
                         for g in graphs_all
                         for ds in g[:rdf.type:sparc.Dataset]]
        if doi]
    merged_all = _merge_graphs(graphs_all)
    merged_all.populate_from_triples(tes.triples_header)
    merged_pub = _merge_graphs(graphs_pub)
    merged_pub.populate_from_triples(tesp.triples_header)
    return merged_all, merged_pub, graphs_all, graphs_pub

def from_snapshot_path_summary_ttl_BAD(snapshot_path, project_id, time_now, blob):
    # this variant is too complex, trying to reuse the published graph as the all graph
    # and the implementation of the OntConjunctiveGraph is not far enough along to do it
    tes = TriplesExportSummary(blob)  # FIXME nasty annoying dep
    graph_meta = OntGraph()
    graph_meta.populate_from_triples(tes._triples_header(tes.ontid, time_now._start_time))
    rev_replace_pairs = _fix_for_pub(graph_meta, graph_meta)
    replace_pairs = tuple([(b, a) for a, b in rev_replace_pairs])

    orps = [OntResPath(uuid_path / 'curation_export.ttl')
            for uuid_path in snapshot_path.children]

    graphs = [o.graph for o in orps]
    # FIXME should use id_published here as well, but that isn't being
    # propagated at the moment
    graphs_pub = []
    graphs_nop = []
    for g, doi in [(g, list(g[ds:TEMP.hasDoi]))
                   for g in graphs for ds in g[:rdf.type:sparc.Dataset]]:
        if doi:
            graphs_pub.append(g)
        else:
            graphs_nop.add(g)
    graph_pub = _merge_graphs(published_graphs)
    graph_pub.populate_from(graph_meta)
    # FIXME this is manually aligned with TriplesExport.triples_header
    graph_pub.asdf
    for g in graphs_nop:
        graph_pub.namespace_manager.populate_from(
            {k:v for k, v in dict(g.namespace_manager).items()
            if k not in ('contributor', 'sample', 'subject')})

    ttl_all = None
    ttl_pub = _populate_published(curation_export, graph)


def from_dataset_export_path_datasets_lists(dataset_export_path):
    dep = dataset_export_path
    alld = []
    pubd = []
    derefs = [l.resolve() for l in [c / 'LATEST' for c in dep.children] if l.exists()]
    # TODO consider creating a folder that is just symlinks before this
    for lp in sorted(derefs, key=lambda p: p.name):
        with open(lp / 'curation-export.json', 'rt') as f:
            j = json.load(f)
            # TODO validate the load XXX this should probably
            # happen as a final roundtrip check during export
            # TODO filter by organization
            alld.append(j)
            if ip in j and rmk in j[ip] and 'id_published' in j[ip][rmk]:
                pubd.append(j)

    return alld, pubd


def from_datasets_list_summary_json(datasets_list, project_id, time_now):
    # XXX FIXME issue with datasets from multiple projects
    fn = Path(datasets_list[0]['prov']['export_project_path']).name
    out = {
        'id': project_id.id,
        'meta': {
            'count': len(datasets_list),
            'folder_name': fn,  # WHAT A RELIEF we don't need network
            'uri_api': project_id.uri_api,
            'uri_human': project_id.uri_human(),
        },
        'datasets': datasets_list,
    }
    add_prov(out, time_now)
    # some potential prov summaries, but lets not do that here
    # most prov stats should be on the single dataset level
    #'export_timestamp_start_min': min(tes),
    #'export_timestamp_start_max': max(tes),
    return out


def from_dataset_export_path_summary_json(dataset_export_path, project_id, time_now):
    l_all, l_pub = from_dataset_export_path_datasets_lists(dataset_export_path)
    #[a['meta']['timestamp_updated'] < a['meta']['timestamp_updated_contents']
    #for a in l_all if a['meta']['timestamp_updated_contents']]
    sum_all = from_datasets_list_summary_json(l_all, project_id, time_now)
    sum_pub = from_datasets_list_summary_json(l_pub, project_id, time_now)
    return sum_all, sum_pub


def main(project_id=None, export_path=None, time_now=None,
         project_id_auth_var='remote-organization',  # FIXME move to clifun
         disco=False, **kwargs):
    from sparcur.paths import Path
    from sparcur.config import auth

    if project_id is None:
        from sparcur.config import auth
        from sparcur.utils import PennsieveId
        project_id = auth.get(project_id_auth_var)
        project_id = PennsieveId(project_id)  # FIXME abstract the hardcoded backend

    if export_path is None:  # XXX see issues mentioned above
        export_path = Path(auth.get_path('export-path'))

    dataset_export_path = export_path / 'datasets'
    snapshots_path = export_path / 'snapshots'
    snapshot_path = from_dataset_export_path_snapshot(
        dataset_export_path, snapshots_path, time_now)
    sum_all, sum_pub = from_snapshot_path_summary_json(
        snapshot_path, project_id, time_now)
    # write symlink LATEST_PARTIAL
    ttl_all, ttl_pub, graphs_all, graphs_pub = from_snapshot_path_summary_ttl(
        snapshot_path, project_id, time_now, sum_all)
    # write symlink LATEST
    maxdt = max_dataset_or_contents_updated(sum_all['datasets'])
    dt_maxdt = dateparser.parse(maxdt)
    dt_maxdt_local = dt_maxdt.astimezone(TZLOCAL())
    friendly_maxdt_local = timeformat_friendly(dt_maxdt_local)
    # FIXME there are some bad assumptions in here that should be refactored out
    # at some point, but for now we implicitly assume that all datasets come from
    # the same organization, which can easily be violated because we don't check 
    # however the existing internal schema requires an id for the summary which is
    # currenty the organization id
    # FIXME summary is a hardcoded path
    # XXX WARNING it is possible to overwrite since maxdt might not change between runs
    # this is desirable behavior for development, but could cause issues in other cases
    pexpath = export_path / 'summary' / project_id.uuid
    latest = pexpath / 'LATEST'
    npath = pexpath / friendly_maxdt_local
    snapshot_link = npath / 'snapshot'
    if not npath.exists():
        npath.mkdir(parents=True)
    else:
        # FIXME not sure if this makes sense?
        if snapshot_link.is_symlink():
            snapshot_link.unlink()

    snapshot_link.symlink_to(snapshot_link.relative_path_to(snapshot_path))

    npath_ce = npath / 'curation-export.json'
    npath_cep = npath / 'curation-export-published.json'
    for path, blob in ((npath_ce, sum_all),
                       (npath_cep, sum_pub)):
        with open(path, 'wt') as f:
            json.dump(blob, f, indent=2)

    npath_ttl = npath / 'curation-export.ttl'
    npath_ttlp = npath / 'curation-export-published.ttl'
    ttl_all.write(npath_ttl)
    ttl_pub.write(npath_ttlp)

    if disco:
        # export xml and tsv for disco
        from sparcur.simple.disco import from_curation_export_json_path_datasets_json_xml_and_disco
        from_curation_export_json_path_datasets_json_xml_and_disco(
            npath_ce, sum_all['datasets'], graphs_all)

    if latest.is_symlink():
        latest.unlink()

    latest.symlink_to(friendly_maxdt_local)

    return npath_ce, sum_all, sum_pub, graphs_all, graphs_pub


if __name__ == '__main__':
    #import pprint
    from sparcur.simple.utils import pipe_main
    # these are really big, don't print them
    # pipe_main(main, after=pprint.pprint)
    pipe_main(main)
# combine.py ends here
