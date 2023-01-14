#!/usr/bin/env python3
# [[file:../../docs/developer-guide.org::dataset-transform][dataset-transform]]
from pathlib import Path
from sparcur import schemas as sc
from sparcur import pipelines as pipes
from sparcur.core import DictTransformer as DT


def __apply_step(step, spec, data, **kwargs):
    return step(data, spec, **kwargs)


def popl(data, pops, source_key_optional=False):
    popped = list(DT.pop(data, pops, source_key_optional))
    return data


def simple_add(data, adds):
    pass


def execute_pipeline(pipeline, data):
    for func, *args, kwargs in pipeline:
        # man variable arity is a pain to deal with here
        # where are lambda lists when you need them :/
        # FIXME maybe we can make steps functional instead of mutating?
        if not kwargs:
            kwargs = {}

        func(data, *args, **kwargs)

    return data


def __wd(transformer):  # not needed atm since transformers do in place modification
    def inner(data, *args, **kwargs):
        transformer(data, *args, **kwargs)
        return data


def schema_validate(data, schema, fail=False, pipeline_stage_name=None):
    if isinstance(schema, type):
        # we were passed a class so init it
        # doing it this way makes it easier to
        # use remote schemas that hit the network
        # since the network call doesn't have to
        # happen at the top level but can mutate
        # the class later before we init here
        schema = schema()

    ok, norm_or_error, data = schema.validate(data)
    if not ok:
        if fail:
            logd.error('schema validation has failed and fail=True')
            raise norm_or_error

        if 'errors' not in data:
            data['errors'] = []

        if pipeline_stage_name is None:
            pipeline_stage_name = f'Unknown.checked_by.{schema.__class__.__name__}'

        data['errors'] += norm_or_error.json(pipeline_stage_name)
        # TODO make sure the step is noted even if the schema is the same


simple_moves = (
    [['structure', 'dirs',], ['meta', 'dirs']],  # FIXME not quite right ...
    [['structure', 'files',], ['meta', 'files']],
    [['structure', 'size',], ['meta', 'size']],
    [['remote_dataset_metadata'], ['inputs', 'remote_dataset_metadata']],
    *pipes.SDSPipeline.moves[3:]
)

# function, *args, **kwargs
# functions should accept data as the first argument
core_pipeline = (
    # FIXME validation of dataset_raw is not being done right now
    (DT.copy, pipes.SDSPipeline.copies, dict(source_key_optional=True)),
    (DT.move, simple_moves, dict(source_key_optional=True)),
    # TODO clean has custom behavior
    (popl, pipes.SDSPipeline.cleans, dict(source_key_optional=True)),
    (DT.derive, pipes.SDSPipeline.derives, dict(source_key_optional=True)),
    #(DT.add, pipes.SDSPipeline.adds),  # FIXME lifter issues
    (schema_validate, sc.DatasetOutSchema, None),
    # extras (missing)
    # xml files
    # contributors
    # submission
    (DT.copy, pipes.PipelineExtras.copies, dict(source_key_optional=True)),
    # TODO clean has custom behavior
    (DT.update, pipes.PipelineExtras.updates, dict(source_key_optional=True)),
    (DT.derive, pipes.PipelineExtras.derives, dict(source_key_optional=True)),
    #(DT.add, pipes.PipelineExtras.adds),  # TODO and lots of evil custom behavior here
    # TODO filter_failures
    (schema_validate, sc.DatasetOutSchema, None),
    (pipes.PipelineEnd._indexes, None),  # FIXME this is conditional and in adds
    # TODO pipeline end has a bunch of stuff in here
    (schema_validate, sc.PostSchema, dict(fail=True)),
)


def main(path=Path.cwd(), path_dataset_raw=None, dataset_raw=None, **kwargs):
    # FIXME TODO need to follow the behavior of main in extract
    if dataset_raw is None:
        if path_dataset_raw is None:
            cache = path.cache
            if not cache.is_dataset():
                raise TypeError('can only run on a single dataset')
            from sparcur.simple.extract import main as extract
            dataset_raw = extract(path)
        else:
            from sparcur.utils import path_ir
            dataset_raw = path_ir(path_dataset_raw)

    data = execute_pipeline(core_pipeline, dataset_raw)
    breakpoint()


if __name__ == '__main__':
    from sparcur.simple.utils import pipe_main
    pipe_main(main, after=print)
# dataset-transform ends here
