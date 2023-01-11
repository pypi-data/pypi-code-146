"""Helpers for maintainers of kofa sites.

XXX: This stuff might go into a separate package, but right
     now it is too less for a complete package.
"""
import sys
from ZODB.FileStorage import FileStorage
from ZODB.scripts.analyze import report, analyze, shorten
from zope.component.hooks import setSite
from zope.component import getUtility
from zope.catalog.interfaces import ICatalog
from zope.intid.interfaces import IIntIds


def db_analyze(args=None):
    """Run the analyze tool from ZODB package.
    """
    if args is None:
        args = sys.argv[1:]

    path = None
    if len(args) > 0:
        path = args[0]
    else:
        print
        print "Analyze a ZODB file and print statistics"
        print "about contained objects, sizes, etc."
        print
        print "Usage: %s <path-to-Data.fs>" % sys.argv[0]
        print
        sys.exit(0)

    report(analyze(path))

def update_catalog(site, cat_name, objects=[], func=None):
    """Update a catalog.

    Put `objects` or objects delivered by `func()` into the catalog
    registered under `cat_name` in `site`.

    Objects to be catalogued must be 'located', i.e. they must have a
    __name__ and __parent__ (because they are adapted to
    IKeyReference).

    You can pass in objects as some iterable or as a function that is
    called to deliver the set of objects to be catalogued.

    A function takes precedence over object lists.
    """
    setSite(site)
    cat = getUtility(ICatalog, name=cat_name)
    intids = getUtility(IIntIds, context=cat)
    if func is not None:
        objects = func()
    for ob in objects:
        doc_id = intids.queryId(ob, None)
        if doc_id is None:
            doc_id = intids.register(ob)
        cat.index_doc(doc_id, ob)
    return cat

def db_diff(args=None):
    """Run the analyze tool from ZODB package to find diffs between
       two ZODBs.
    """
    if args is None:
        args = sys.argv[1:]

    zodb_path1, zodb_path2 = (None, None)
    if len(args) > 1:
        zodb_path1, zodb_path2 = args[0:2]
    else:
        print
        print "Analyze two ZODB files and print statistics"
        print "about contained objects, sizes, etc."
        print "Shows only differences."
        print
        print "Usage: %s <path-to-Data1.fs> <path-to-Data2.fs>" % sys.argv[0]
        print
        sys.exit(0)

    a1 = analyze(zodb_path1)
    a2 = analyze(zodb_path2)

    diff_report(a1, a2)


def diff_report(rep1, rep2):
    print "Processed %d (%d, %d) records in %d (%d, %d) transactions" % (
        rep1.OIDS + rep2.OIDS, rep1.OIDS, rep2.OIDS,
        rep1.TIDS + rep2.TIDS, rep2.TIDS, rep2.TIDS)
    print "Types used:"
    fmt = "  %-44s %7s %9s %6s %7s"
    fmtp = "%-44s %+7d %9d %5.1f%% %7.2f" # per-class format
    fmtpplus = "+ %-44s %+7d %+9d %+5.1f%% %7.2f" # per-class format
    fmtpminus = "- %-44s %+7d %+9d %+5.1f%% %7.2f" # per-class format
    fmts = "  %44s %+7d %+8dk %+5.1f%% %+7.2f" # summary format
    typemap1, typemap2 = rep1.TYPEMAP.keys(), rep2.TYPEMAP.keys()
    typemap1.sort()
    typemap2.sort()
    typemap = list(set(typemap1 + typemap2))
    typemap.sort()
    print fmt % ("Class Name", "Count", "TBytes", "Pct", "AvgSize")
    print fmt % ('-'*44, '-'*7, '-'*9, '-'*5, '-'*7)
    for t in typemap:
        if t in typemap1 and t in typemap2 and (
            rep1.TYPESIZE[t] == rep2.TYPESIZE[t]) and (
            rep1.TYPEMAP[t] == rep2.TYPEMAP[t]):
            continue
        if t not in typemap1:
            cnt = rep2.TYPEMAP[t]
            pct = rep2.TYPESIZE[t] * 100.0 / rep2.DBYTES
            print fmtpplus % (shorten(t, 44), cnt, rep2.TYPESIZE[t],
                      pct, rep2.TYPESIZE[t] * 1.0 / rep2.TYPEMAP[t])

        elif t not in typemap2:
            cnt = -rep1.TYPEMAP[t]
            pct = rep1.TYPESIZE[t] * 100.0 / rep1.DBYTES
            print fmtpminus % (shorten(t, 44), cnt, -rep1.TYPESIZE[t],
                      pct, rep1.TYPESIZE[t] * 1.0 / rep1.TYPEMAP[t])
        else:
            cnt = rep2.TYPEMAP[t] - rep1.TYPEMAP[t]
            pct1 = rep1.TYPESIZE[t] * 100.0 / rep1.DBYTES
            pct2 = rep2.TYPESIZE[t] * 100.0 / rep2.DBYTES
            pct = pct2 - pct1
            size = rep2.TYPESIZE[t] - rep1.TYPESIZE[t]
            if cnt > 0:
                print fmtpplus % (
                    shorten(t, 44), cnt, size,
                    pct, rep2.TYPESIZE[t] * 1.0 / rep2.TYPEMAP[t])
            else:
                print fmtpminus % (
                    shorten(t, 44), cnt, size,
                    pct, rep1.TYPESIZE[t] * 1.0 / rep1.TYPEMAP[t])


    print fmt % ('='*44, '='*7, '='*9, '='*5, '='*7)
    print fmts % ('Current Objects', rep2.COIDS - rep1.COIDS,
                  (rep2.CBYTES / 1024.0) - (rep1.CBYTES / 1024.0),
                  (rep2.CBYTES * 100.0 / rep2.DBYTES) - (
                      rep1.CBYTES * 100.0 / rep1.DBYTES),
                  (rep2.CBYTES * 1.0 / rep2.COIDS) - (
                      rep1.CBYTES * 1.0 / rep1.COIDS))
    #if rep1.FOIDS and rep2.FOIDS:
    fbytes = (rep2.FBYTES / 1024.0) - (rep1.FBYTES / 1024.0)
    rep1_fpct = (rep1.DBYTES and
                 (rep1.FBYTES * 100.0 / (rep1.DBYTES)) or 0.0)
    rep2_fpct = (rep2.DBYTES and
                 (rep2.FBYTES * 100.0 / (rep2.DBYTES)) or 0.0)
    print fmts % ('Old Objects', rep2.FOIDS - rep1.FOIDS,
                  fbytes, rep2_fpct - rep1_fpct,
                  (rep2.FBYTES * 1.0 / (rep2.FOIDS or 1.0)) - (
                      rep1.FBYTES * 1.0 / (rep1.FOIDS or 1.0)))
    return

