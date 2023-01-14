#!/usr/bin/env python3
# [[file:../../docs/developer-guide.org::dataset-extract][dataset-extract]]
from sparcur import datasets as dat
from sparcur import pipelines as pipes
from sparcur import exceptions as exc
from sparcur.utils import log, logd
from sparcur.paths import Path
from sparcur.backends import PennsieveDatasetData
from sparcur.simple.utils import combinate, multiple, early_failure, DataWrapper
from sparcur.simple.fetch_metadata_files import fetch_prefixes


class ManifestFiles(DataWrapper):
    """ wrapper for manifest files. """


def merge_manifests(vs):
    """ Merge individual manifest records into the same list """
    # FIXME massive hack :/
    k = 'manifest_file'
    # FIXME errors key ... ? is it allowed up there? it shouldn't be ...
    # FIXME {'content': m}
    return ManifestFiles([m for v in vs for m in v.data[k]])


def object_from_find_path(glob_prefix, object_from_path_function, glob_type='glob', onfail=None):
    """ Return a function that will find files that start with glob_prefix"""
    # FIXME should be in utils but depends on fetch_prefixes
    if glob_prefix not in dict(fetch_prefixes):
        raise ValueError('glob_prefix not in fetch_prefixes! '
                         f'{glob_prefix!r} not in {fetch_prefixes}')
    def func(path, *args, **kwargs):
        ds = dat.DatasetStructure(path)
        rpath = None
        for rpath in ds._abstracted_paths(glob_prefix, sandbox=True):
            yield object_from_path_function(rpath, *args, **kwargs)

        if rpath is None and onfail is not None:
            raise onfail(f'No match for {glob_prefix} in {path.name}')

    return func

# file type -> dataset blob key indirection

_TOP = object()  # SIGH SIGH SIGH always need a escape hatch

otkm = {ThingFilePath.obj:prefix + '_file' for prefix, ThingFilePath
        in dat.DatasetStructure.sections.items()}
otkm[ManifestFiles] = 'manifest_file'
otkm[PennsieveDatasetData] = 'remote_dataset_metadata'
otkm[type(dat.DatasetStructure())] = 'structure'  # hack around Pathlib type mangling
otkm[type(dat.DatasetMetadata())] = _TOP

# stream of objects -> place in dataset blob

def dataset_raw(*objects, object_type_key_map=otkm):
    data = {}
    log.debug(objects)
    #path_structure, description, subjects, samples, submission, manifests, *rest = objects
    for obj in objects:
        log.debug(obj)
        key = object_type_key_map[type(obj)]
        try:
            if key is not _TOP:
                data.update({key: obj.data})
            else:
                data.update(obj.data)
        except Exception as e:
            # FIXME current things that leak through
            # MalformedHeaderError
            # something in the objects list is a dict
            breakpoint()
            pass

    return data


# path + version -> python object

# TODO how to attach and validate schemas orthogonally in this setting?
# e.g. so that we can write dataset_1_0_0 dataset_1_2_3 etc.

# we capture version as early as possible in the process, yes we
# could also gather all the files and folders and then pass the version
# in as an argument when we validate their structure, but there are
# elements of the locations or names of those files that might depend
# on the template version, therefore we get maximum flexibility by only
# need to look for the dataset description file
def description(path):          return dat.DatasetDescriptionFilePath(path).object
def submission(path, version):  return dat.SubmissionFilePath(path).object_new(version)
def subjects(path, version):    return dat.SubjectsFilePath(path).object_new(version)
def samples(path, version):     return dat.SamplesFilePath(path).object_new(version)
def manifest(path, version):    return dat.ManifestFilePath(path).object_new(version)

# dataset path -> python object

def from_path_remote_metadata(path): return PennsieveDatasetData(path.cache)
def from_path_local_metadata(path): return dat.DatasetMetadata(path)
from_path_dataset_description = object_from_find_path('dataset_description', description,
                                                      onfail=exc.MissingFileError)

comb_metadata = combinate(
    # dataset description is not included here because it is special
    # see from_path_dataset_raw for details
    from_path_remote_metadata,
    from_path_local_metadata,
)

# dataset path + version -> python object

def from_path_dataset_path_structure(path, version): return dat.DatasetStructure(path)
from_path_subjects   = object_from_find_path('subjects',            subjects)
from_path_samples    = object_from_find_path('samples',             samples)
from_path_submission = object_from_find_path('submission',          submission)
from_path_manifests  = multiple(object_from_find_path('manifest',   manifest,
                                                      'rglob'),
                                merge_manifests)

# combinate all the individual dataset path + version -> data functions

comb_dataset = combinate(
    #from_path_dataset_description,  # must be run prior to combination to get version
    from_path_dataset_path_structure,
    from_path_subjects,
    from_path_samples,
    from_path_submission,
    from_path_manifests,
    #from_path_file_metadata,  # this must wait until 2nd fetch phase
    )

# dataset path -> raw data

def from_path_dataset_raw(dataset_path):
    """ Main entry point for getting dataset metadata from a path. """
    gen  = from_path_dataset_description(dataset_path)
    try:
        ddo = dataset_description_object = next(gen)
    except exc.MissingFileError as e:
        # TODO return a stub with embedded error
        logd.critical(e)
        dataset_blob = dataset_raw(*comb_metadata(dataset_path))
        return early_failure(dataset_path, e, dataset_blob)

    try:
       next(gen)
       # TODO return a stub with embedded error
    except StopIteration:
        pass

    data = ddo.data
    ddod = type('ddod', tuple(), {'data': data})
    dtsv = data['template_schema_version']
    return dataset_raw(ddo, *comb_metadata(dataset_path), *comb_dataset(dataset_path, dtsv))


# unused

def from_path_file_metadata(path, _version):  # FIXME doesn't go in this file probably
    # FIXME this is going to depend on the manifests
    # and a second fetch step where we kind of cheat
    # and prefetch file files we know we will need
    pass


def from_export_path_protocols_io_data(curation_export_json_path): pass
def protocols_io_ids(datasets): pass
def protocols_io_data(protocols_io_ids): pass

def from_group_name_protcur(group_name): pass
def protcur_output(): pass

def summary(datasets, protocols_io_data, protcur_output): pass

def from_path_summary(project_path):
    dataset_path_structure
    summary((
        dataset(
            dataset_path_structure,
            dataset_description,
            subjects,
            samples,
            submission,
            manifests,
            *rest
)))


def main(path=Path.cwd(), id=None, dataset_id=tuple(), time_now=None,
         export_path=None, export_parent_path=None, _entry_point=False, **kwargs):
    # TODO path from dataset_id and retrieve conventions? or just pass path from retrieve final output?
    # TODO parallelize if multiple paths
    # This assumes that all retrieve operations have
    # finished successfully for the current dataset
    from sparcur.simple.export import prepare_dataset_export, export_blob
    if id is not None:  # XXX note that id should be dataset_id # TODO parent_path ??
        uuid = id.uuid  # FIXME hardcoded backend assumption
        path = path / uuid / 'dataset'  # FIXME hardcoded see invariant_path
        path = path.resolve()  # make sure that invariant_path is expanded as we expect.

    cache = path.cache
    if not cache.is_dataset():
        raise TypeError('can only run on a single dataset')

    if _entry_point:
        if export_parent_path is None:
            export_parent_path = prepare_dataset_export(path, export_path)

        kwargs.update({'export_path': export_path,
                       'export_parent_path': export_parent_path,
                       'time_now': time_now,})

    dataset_raw = from_path_dataset_raw(path)

    if _entry_point:
        export_blob_path = export_blob(dataset_raw, 'ir.json', **kwargs)
        return export_blob_path
    else:
        return dataset_raw


if __name__ == '__main__':
    import pprint
    from sparcur.simple.utils import pipe_main
    pipe_main(main, after=pprint.pprint)
# dataset-extract ends here
