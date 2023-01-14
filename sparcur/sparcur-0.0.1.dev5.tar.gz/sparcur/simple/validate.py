#!/usr/bin/env python3
# [[file:../../docs/developer-guide.org::validate.py][validate.py]]
import augpathlib as aug
from sparcur import pipelines as pipes
from sparcur.paths import PathL, CacheL
from sparcur.utils import GetTimeNow


def makeValidator(dataset_path, time_now=None):

    if time_now is None:
        time_now = GetTimeNow()

    class CacheX(CacheL):
        def __new__(cls, *args, **kwargs):
            return super().__new__(cls, *args, **kwargs)

    CacheX._bind_flavours()

    class PathX(PathL):
        """ Workaround absense of cache. """

        _cache_class = CacheX

        def __new__(cls, *args, **kwargs):
            return super().__new__(cls, *args, **kwargs)

        # TODO likely will also need to rebind the cache class as well

        #@property
        #def dataset_relative_path(self, __drp=dataset_path):
            #return self.relative_path_from(self.__class__(__drp))

    CacheX._local_class = PathX
    PathX._bind_flavours()

    # XXX monkey patch TODO sigh FIXME DatasetStructure calls Path directly inside
    #PathL.dataset_relative_path = Path.dataset_relative_path

    # must caste before anything else is done so that anchor and
    # datasets are known
    dataset_path = PathX(dataset_path)

    CacheX._dataset_dirs = [CacheX(dataset_path)]
    # FIXME this is very much not ideal because we don't actually want
    # the parent in this case
    CacheX._asserted_anchor = CacheX(dataset_path.parent)

    class context:
        path = dataset_path.resolve()
        id = path.id
        uri_api = path.as_uri()
        uri_human = path.as_uri()

    class lifters:
        id = context.id
        remote = 'local'
        folder_name = context.path.name
        uri_api = context.uri_api
        uri_human = context.uri_human
        timestamp_export_start = time_now.START_TIMESTAMP

        affiliations = lambda *args, **kwargs: None
        techniques = tuple()
        modality = None
        organ_term = None
        protocol_uris = tuple()

        award_manual = None

    return pipes.PipelineEnd(dataset_path, lifters, context)
    return pipes.SDSPipeline(dataset_path, lifters, context)  # shouldn't need network


def main(path=PathL.cwd(), time_now=None,
         export_local=False, export_parent_path=None,
         _entry_point=False, validate=False, **kwargs):

    # ('../resources/DatasetTemplate')
    pipeline = makeValidator(path, time_now=time_now)
    data = pipeline.data

    if _entry_point:
        from sparcur.simple.export import export_blob
        export_blob_path = export_blob(
            data, 'curation-export.json', time_now=time_now,
            export_parent_path=export_parent_path if export_parent_path is not None else path,
            **kwargs)
        return export_blob_path
    else:
        return data


if __name__ == '__main__':
    from sparcur.simple.utils import pipe_main
    pipe_main(main)
# validate.py ends here
