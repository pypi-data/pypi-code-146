#!/usr/bin/env python3
# [[file:../../docs/developer-guide.org::utils.py][utils.py]]
from sparcur.config import auth
__doc__ = f"""Common command line options for all sparcur.simple modules
Usage:
    sparcur-simple manifest  [options]  [<path>...]
    sparcur-simple get-uuid  <remote-id>...
    sparcur-simple datasets
    sparcur-simple for-racket
    sparcur-simple check-names
    sparcur-simple git-repos [update] [options]
    sparcur-simple [options] [<path>...]
    sparcur-simple [options] [--dataset-id=<ID>...]
    sparcur-simple [options] [--extension=<EXT>...] [<path>...]

Commands:
    manifest                        generate manifest files for path
    for-racket                      print data for reading into Racket

Options:
    -h --help                       show this

    --hypothesis-group-name=NAME    the hypotheis group name

    --project-id=ID                 the project id
    --dataset-id=<ID>...            one or more datset ids
    --project-id-auth-var=VAR       name of the auth variable holding the project-id

    --project-path=PATH             the project path, will be path if <path>... is empty
    --parent-path=PATH              the parent path where the project will be cloned to
    --parent-parent-path=PATH       parent in which a random tempdir is generated
                                    or the dataset uuid is used as the parent path, don't use this ...
    --invariant-local-path=PATH     path relative to parent path for dataset [default: dataset]
    --export-local                  set export-parent-path to {{:parent-path}}/exports/
    --export-path=PATH              base export path containing the standard path structure [default: {auth.get_path('export-path')}]
    --cleaned-parent-path=PATH      direct parent path into which cleaned paths will be placed
    --cleaned-path=PATH             base cleaned path containing the standard path structure [default: {auth.get_path('cleaned-path')}]
    --export-parent-path=PATH       direct parent path into which exports will be placed
    --extension=<EXT>...            one or more file extensions to fetch

    -j --jobs=N                     number joblib jobs [default: 12]
    --exclude-uploaded              do not pull files from remote marked as uploaded
    --sparse-limit=N                package count that forces a sparse pull [default: {auth.get('sparse-limit')}]
    --symlink-objects-to=PATH       path to an existing objects directory
    --log-level=LEVEL               log level info [default: INFO]
    --open=PROGRAM                  show file with PROGRAM
    --show                          show file with xopen
    --pretend                       show what would be done for update
"""

import os
import sys
from types import GeneratorType
from pyontutils import clifun as clif
from sparcur import exceptions as exc
from sparcur.utils import _find_command
from sparcur.utils import log, logd, loge, GetTimeNow, PennsieveId
from sparcur.paths import Path, PennsieveCache
from sparcur.backends import PennsieveRemote


def backend_pennsieve(project_id=None, Local=Path, Cache=PennsieveCache):  # (ref:def_babf)
    """return a configured pennsieve backend
        calling this is sufficient to get everything set up correclty

        You must call RemotePath.init(project_id) before using
        RemotePath.  Passing the project_id argument to this function
        will do that for you. It is not required because there are
        cases where the project_id may not be known at the time that
        this function is called. """

    RemotePath = PennsieveRemote._new(Local, Cache)

    if project_id is not None:
        RemotePath.init(project_id)

    return RemotePath


class Options(clif.Options):

    @property
    def id(self):
        # dataset_id has priority since project_id can occure without a
        # dataset_id, but dataset_id may sometimes come with a project_id
        # in which case the dataset_id needs priority for functions that
        # branch on the most granular identifier type provided
        return (self.dataset_id[0]
                if self.dataset_id else
                (self.project_id
                 if self.project_id else
                 None))

    @property
    def project_id(self):
        if not hasattr(self, '_cache_project_id'):
            id = self._args['--project-id']
            if id is not None:
                identifier = PennsieveId(id, type='organization')
                self._cache_project_id = identifier
            else:
                return

        return self._cache_project_id

    @property
    def dataset_id(self):
        if not hasattr(self, '_cache_dataset_id'):
            ids = self._args['--dataset-id']
            if ids:
                identifiers = [PennsieveId(id, type='dataset') for id in ids]
                self._cache_dataset_id = identifiers
            else:
                return ids

        return self._cache_dataset_id

    @property
    def remote_id(self):
        if not hasattr(self, '_cache_remote_id'):
            ids = self._args['<remote-id>']
            if ids:
                identifiers = [PennsieveId(id) for id in ids]
                self._cache_remote_id = identifiers
            else:
                return ids

        return self._cache_remote_id

    @property
    def jobs(self):
        return int(self._args['--jobs'])

    n_jobs = jobs  # match internal kwargs conventions

    @property
    def paths(self):
        return [Path(p).expanduser().resolve() for p in self._args['<path>']]

    @property
    def path(self):
        paths = self.paths
        if paths:
            return paths[0]
        elif self.project_path:
            return self.project_path
        else:
            # if no paths were listed default to cwd
            # consistent with how the default kwargs
            # are set on a number of mains
            # this is preferable to allow path=None
            # to be overwritten by the conventions of
            # individual pipeline mains
            return Path.cwd()

    @property
    def project_path(self):
        pp = self._args['--project-path']
        if pp:
            return Path(pp).expanduser().resolve()

    @property
    def parent_parent_path(self):
        ppp = self._args['--parent-parent-path']
        if ppp:
            return Path(ppp).expanduser().resolve()
        else:
            return Path.cwd()

    @property
    def parent_path(self):
        pap = self._args['--parent-path']
        did = self.dataset_id
        if pap:
            return Path(pap).expanduser().resolve()
        elif did:
            id = self.id  # dataset_id is a list so use id which handles that
            uuid = id.uuid
            return (self.parent_parent_path / uuid).expanduser().resolve()

    @property
    def export_path(self):
        ep = self._args['--export-path']
        epp = self.export_parent_path
        if ep and epp:
            raise TypeError('Only one of --export-path and --export-parent-path may be set.')
        elif ep:
            return Path(ep).expanduser().resolve()
        else:
            raise Exception('should not happen')

    @property
    def export_parent_path(self):
        epp = self._args['--export-parent-path']
        el = self.export_local
        pap = self.parent_path
        if epp and el:
            raise TypeError('Only one of --export-local and --export-parent-path may be set.')
        elif epp:
            return Path(epp).expanduser().resolve()
        elif el and pap:
            # it is ok to do this here becuase the TypeError above prevents
            # the case where both epp and el are set, so even though epp
            # is no longer always what was set on the command line, it is
            # it is the case that there won't be conflicting sources
            return pap / 'exports'

    @property
    def cleaned_path(self):
        cp = self._args['--cleaned-path']
        cpp = self.export_parent_path
        if cp and cpp:
            raise TypeError('Only one of --cleaned-path and --cleaned-parent-path may be set.')
        elif cp:
            return Path(cp).expanduser().resolve()
        else:
            raise Exception('should not happen')

    @property
    def cleaned_parent_path(self):
        cpp = self._args['--cleaned-parent-path']
        if cpp:
            return Path(cpp).expanduser().resolve()

    @property
    def extensions(self):
        return self.extension

    @property
    def symlink_objects_to(self):
        slot = self._args['--symlink-objects-to']
        if slot:
            return Path(slot).expanduser()

    @property
    def sparse_limit(self):  # FIXME not being pulled in by asKwargs ??
        return int(self._args['--sparse-limit'])

    @property
    def time_now(self):  # FIXME make it possible to pass this in?
        if not hasattr(self, '_time_now'):
            self._time_now = GetTimeNow()

        return self._time_now

    @property
    def log_level(self):  # FIXME not being pulled in by asKwargs ??
        ll = self._args['--log-level']
        if ll.isdigit() or ll[0] == '-' and ll[1:].isdigit():
            return int(ll)
        else:
            return ll


def pipe_main(main, after=None, argv=None):
    options, args, defaults = Options.setup(__doc__, argv=argv)
    # _entry_point is used as a way to switch behavior when a
    # pipeline main is run directly or actually in a pipeline
    try:
        log.setLevel(options.log_level)
        logd.setLevel(options.log_level)
        loge.setLevel(options.log_level)
        out = main(_entry_point=True, **options.asKwargs())
    except Exception as e:
        log.exception(e)
        log.error(options.path)
        raise e

    if after:
        after(out)

    return out


def rglob(path, pattern):
    """ Hack around the absurd slowness of python's rglob """

    if sys.platform == 'win32':
        log.warning('no findutils on windows, watch out for unexpected files')
        return list(path.rglob(pattern))

    doig = (hasattr(path, 'cache') and
            path.cache and
            path.cache.cache_ignore)
    exclude = ' '.join([f"-not -path './{p}*'" for p in path.cache.cache_ignore]) if doig else ''
    command = f"""{_find_command} {exclude} -name {pattern!r}"""

    with path:
        with os.popen(command) as p:
            string = p.read()

    path_strings = string.split('\n')  # XXX posix path names can contain newlines
    paths = [path / s for s in path_strings if s]
    return paths


def _fetch(cache):  # sigh joblib multiprocessing pickling
    # lambda functions are great right up until you have to handle an
    # error function inside of them ... thanks python for yet another
    # failure to be homogenous >_<
    meta = cache.meta
    try:
        size_mb = meta.size.mb
    except AttributeError as e:
        if meta.errors:
            logd.debug(f'remote errors {meta.errors} for {cache!r}')
            return
        else:
            raise exc.StopTheWorld(cache) from e

    return cache.fetch(size_limit_mb=size_mb + 1)  # FIXME somehow this is not working !?


def _fetch_path(path):  # sigh joblib multiprocessing pickling
    path = Path(path)
    cache = path.cache
    if cache is None:
        raise exc.NoCachedMetadataError(path)

    # do not return to avoid cost of serialization back to the control process
    _fetch(cache)


def fetch_paths_parallel(paths, n_jobs=12, use_async=True):
    if n_jobs <= 1:
        [_fetch_path(path) for path in paths]
    elif use_async:
        from pyontutils.utils import Async, deferred
        Async()(deferred(_fetch_path)(path) for path in paths)
    else:
        import pathlib
        from joblib import Parallel, delayed
        backend = 'multiprocessing' if hasattr(sys, 'pypy_version_info') else None
        # FIXME FIXME FIXME somehow this can result in samples.xlsx being fetched to subjects.xlsx !?!??!!
        # XXX either a race condition on our end or something insane from the remote
        Parallel(n_jobs=n_jobs, backend=backend)(delayed(_fetch_path)(pathlib.Path(path)) for path in paths)
        #Parallel(n_jobs=n_jobs)(delayed(fetch_path)(path) for path in paths)


def combinate(*functions):
    def combinator(*args, **kwargs):
        for f in functions:
            # NOTE no error handling is needed here
            # in no cases should the construction of
            # the python object version of a path fail
            # all failures should happen _after_ construction
            # the way we have implemented this they fail when
            # the data attribute is accessed
            obj = f(*args, **kwargs)
            if isinstance(obj, GeneratorType):
                yield from obj
                # FIXME last one wins, vs yield tuple vs ...?
                # FIXME manifests are completely broken for this
            else:
                yield obj

    return combinator


def multiple(func, merge=None):
    """ combine multiple results """
    def express(*args, **kwargs):
        vs = tuple(func(*args, **kwargs))
        if merge is not None:
            yield merge(vs)
        else:
            yield vs

    return express


def early_failure(path, error, dataset_blob=None):
    # these are the 9999 5555 and 4444 errors
    # TODO match the minimal schema reqs as
    # we did in pipelines
    if dataset_blob is None:
        cache = path.cache
        return {'id': cache.id,
                'meta': {'uri_api': cache.uri_api,
                         'uri_human': cache.uri_human,},
                #'status': 'early_failure',  # XXX note that status is not requried
                # if we cannot compute it, but if there are inputs there should be
                # a status
                'errors': [error],  # FIXME format errro
                }

    else:
        if 'errors' not in datset_blob:
            dataset_blob['errors'] = []

        datset_blob['errors'].append(error)
        return dataset_blob


class DataWrapper:
    # sigh patterns are stupid, move this to elsewhere so it doesn't taint everything
    def __init__(self, data):
        self.data = data


def main(id=None, **kwargs):
    def ik(key):
        return key in kwargs and kwargs[key]

    if id is not None:
        print(id.uuid)

    if ik('get_uuid'):
        for id in kwargs['remote_id']:
            print(id.uuid)

        return

    if (ik('datasets') or ik('for_racket') or ik('check_names')):
        log.setLevel(60)  # logging.CRITICAL = 50
        from sparcur.config import auth
        from sparcur.simple.utils import backend_pennsieve
        if ik('project_id'):
            pass  # project_id from command line
        else:
            project_id = auth.get('remote-organization')

        PennsieveRemote = backend_pennsieve(project_id)
        root = PennsieveRemote(project_id)
        datasets = list(root.children)

    if ik('datasets'):
        print('\n'.join([d.id for d in datasets]))

    if ik('for_racket'):
        import json
        _dsmeta = '\n'.join([f"({json.dumps(d.id)} {json.dumps(d.name)})"
                             for d in datasets])
        dsmeta = f"({_dsmeta})"
        # lab pi last name should be cached in some other way
        print(dsmeta)

    if ik('check_names'):
        # you will want to run sparcur.simple.fetch_remote_metadata_all
        from pathlib import PurePosixPath
        def report(pid, exp, pub):
            pname = pub['name']
            name_mismatch = (
                False if exp['basename'] == pname
                else (exp['basename'], pname))
            # [6:] to strip files/
            ppname = PurePosixPath(pub['path']).name
            pathname_mismatch = (
                False if exp['basename'] == ppname
                else (exp['basename'], ppname))

            eppp = PurePosixPath(exp['dataset_relative_path']).parent.as_posix()
            pppp = PurePosixPath(pub['path'][6:]).parent.as_posix()
            parent_path_mismatch = (
                False if eppp == pppp
                else (eppp, pppp))

            # once we fix things on our end names should match
            # parent paths should match
            # name and pathname might match but do not have to match
            pid = f'  {pid}'
            nsp = '\n        '
            if name_mismatch:
                if pathname_mismatch and pname != ppname:
                    return (f'{pid}    name mismatch and pathname mismatch                '
                            f'{nsp}{nsp.join(name_mismatch)}{nsp}{nsp.join(pathname_mismatch)}')
                else:
                    return (f'{pid}    name mismatch                                      '
                            f'{nsp}{nsp.join(name_mismatch)}')

            if parent_path_mismatch:
                if True:
                    return (f'{pid}                                        parent mismatch'
                            f'{nsp}{nsp.join(parent_path_mismatch)}')

            if True:
                if True:
                    return ''
                    #return (f'{pid} ok                                                    ')

        import json
        from sparcur.backends import PennsieveDatasetData
        export_path = kwargs['export_path']
        epd = export_path / 'datasets'
        for dataset in datasets:
            latest = epd / dataset.identifier.uuid / 'LATEST'
            export_path_metadata =  latest / 'path-metadata.json'
            exported = export_path_metadata.exists()

            # pass the remote not just the id so that bfobject is
            # accessible to the RemoteDatasetData class
            pdd = PennsieveDatasetData(dataset)
            rmeta = pdd.fromCache()
            published = 'id_published' in rmeta
            if exported and published:
                with open(export_path_metadata, 'rt') as f:
                    j = json.load(f)
                epni = {'N:' + o['remote_id']:o for o in j['data']
                        if o['remote_id'].startswith('package:')}
                ppni = pdd._published_package_name_index()
                se, sp = set(epni), set(ppni)
                e_missing = sp - se
                p_missing = se - sp
                s_common = sp & se
                rep = [report(c, epni[c], ppni[c]) for c in s_common]
                repstr = '\n'.join([r for r in rep if r])
                if repstr:
                    print(dataset.id, 'bad')
                    print(repstr)
                else:
                    print(dataset.id, 'ok')
            elif exported:
                print(dataset.id, 'unpublished')
            elif published:
                print(dataset.id, 'unexported')
            else:
                print(dataset.id, 'unpublished and unexported')

    if ik('git_repos'):
        import augpathlib as aug
        import sparcur
        from sparcur.config import auth
        from importlib import metadata
        d = metadata.distribution(sparcur.__package__)
        rps = [p for p in [aug.RepoPath(d._path) for d in d.discover()] if p.working_dir]
        setups = [p for p in [p.parent / 'setup.py' for p in rps] if p.exists()]
        wds = sorted(set([p.working_dir for p in rps]))
        never_update = auth.get('never-update')
        pretend=ik('pretend') or never_update
        if pretend:
            if never_update:
                print(f'never-update: true is set in {auth.user_config._path}')
            print('These are the commands that would be run.')
        def doupdate(rp):
            if pretend:
                print(f'git -C {rp.as_posix()} stash')
                print(f'git -C {rp.as_posix()} pull')
                return
            print(f'Pulling {rp.as_posix()}')
            print(rp.repo.git.stash())
            # TODO checkout to a safety branch and tag for rollback
            print(rp.repo.git.pull())
        if ik('update'):
            for wd in wds:
                doupdate(wd)
            # indescriminately run setup.py with --release set to tangle
            from importlib import util as imu
            oldargv = sys.argv
            try:
                for s in setups:
                    if pretend:
                        print(f'pushd {s.parent.as_posix()}; python setup.py --release; popd')
                        continue
                    sys.argv = ['setup.py', '--release']  # reset every time since most will mutate
                    print(f'Maybe tangling via {s.as_posix()}')
                    spec = imu.spec_from_file_location(f'setup_{s.parent.name}', s)
                    mod = imu.module_from_spec(spec)
                    try:
                        with s.parent:  # ah relative paths
                            spec.loader.exec_module(mod)
                    except SystemExit:
                        pass
                    except Exception as e:
                        log.exception(e)
            finally:
                sys.argv = oldargv

    if ik('manifest'):
        from sparcur.utils import write_manifests
        paths = kwargs['paths']
        if not paths:
            paths = [Path.cwd()]

        manifests_rendered = write_manifests(parents=paths)
        manifests, rendered = zip(*manifests_rendered)
        nl = '\n'
        print(f'generated manifests at:\n{nl.join([m.as_posix() for m in manifests])}')
        if ik('open'):
            cmd = kwargs['open']
            [m.xopen(cmd) for m in manifests]
        elif ik('show'):
            [m.xopen() for m in manifests]


if __name__ == '__main__':
    pipe_main(main)
# utils.py ends here
