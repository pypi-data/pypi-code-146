#!/usr/bin/env python3
# [[file:../../docs/developer-guide.org::compact.py][compact.py]]
"""
Examples:
    # look at the second one and then run the first one since it is easier and safer to stop and resume
    # python -m sparcur.simple.compact | xargs -P4 -r -I{} sh -c 'tar -cvJf "{}.tar.xz" "{}" && rm -r "{}"'
    python -m sparcur.simple.compact | xargs -P12 -r -I{} echo tar -cvJf '{}.tar.xz' '{}'
    # python -m sparcur.simple.compact | xargs -P6 -r -I{} echo rm -r '{}'
"""
from sparcur.paths import Path
from sparcur.config import auth


__dep_cache = {}
def latest_snapped(dataset_export_path, snapped):
    if dataset_export_path not in __dep_cache:
        cs = set(c for c in dataset_export_path.children if c.is_dir() and not c.is_symlink())
        csnap = cs.intersection(snapped)
        if not csnap:  # no snap, pretend that latest is snapped
            # this can happen if there is no LATEST because we
            # were e.g. just exporting path metadata and nothing else
            maxsnap = sorted(cs, key=lambda p: p.name)[-1]
        else:
            maxsnap = sorted(csnap, key=lambda p: p.name)[-1]

        __dep_cache[dataset_export_path] = maxsnap.name

    return __dep_cache[dataset_export_path]


def main():
    export_path = Path(auth.get_path('export-path'))
    summary_path = export_path / 'summary'
    snapshots_path = export_path / 'snapshots'
    datasets_path = export_path / 'datasets'

    snap_shotted = [
        dss.resolve()
        for d in summary_path.rchildren_dirs
        for l in d.rchildren if l.is_symlink() and l.name == 'snapshot'
        for dss in l.resolve().children]

    snapped = set(snap_shotted)

    latest_sums = [
        d.resolve()
        for c in summary_path.children
        for d in (c / 'LATEST',) if d.exists()]

    all_builds = [
        build
        for date in datasets_path.children if date.is_dir() and not date.is_symlink()
        for build in date.children if build.is_dir() and not build.is_symlink()]

    older_not_snap = [
        a for a in all_builds
        if a not in snapped and a.name < latest_snapped(a.parent, snapped)]

    assert not snapped.intersection(older_not_snap)

    # newer = set(all_builds) - snapped - set(older_not_snap)

    _ = [print(p) for p in older_not_snap]


if __name__ == '__main__':
    main()
# compact.py ends here
