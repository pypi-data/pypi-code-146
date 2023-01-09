"""
An app to take care of the initial 'sourcing' part of the data prep of audio ML
"""
from typing import Mapping
from know.boxes import *
from functools import partial
from typing import Callable, Iterable
from front import APP_KEY, RENDERING_KEY, ELEMENT_KEY, NAME_KEY
from i2 import Pipe, Sig
from front.crude import Crudifier
from slang.chunkers import fixed_step_chunker
import streamlit as st
from streamlitfront import mk_app, binder as b
from streamlitfront.elements import (
    SelectBox,
    SuccessNotification,
    KwargsInput,
    PipelineMaker,
)
from slang import fixed_step_chunker, mk_chk_fft

from plunk.sb.front_experiments.streamlitfront_dataprep.data_prep2 import (
    # DFLT_WF_PATH,
    # DFLT_ANNOT_PATH,
    data_from_wav_folder,
    data_from_csv,
    store_to_key_fvs,
    key_fvs_to_tag_fvs,
    mk_Xy,
)


def chunker(it, chk_size):
    return fixed_step_chunker(it=it, chk_size=chk_size, chk_step=chk_size)


def mk_pipeline_maker_app_with_mall(
    mall: Mapping,
    *,
    step_factories: str = 'step_factories',
    steps: str = 'steps',
    steps_store=None,
    pipelines: str = 'pipelines',
    pipelines_store=None,
):
    # TODO: Like to not have this binder logic involving streamlit state here! Contain it!
    if not b.mall():
        # TODO: Maybe it's here that we need to use know.malls.mk_mall?
        b.mall = mall
    mall = b.mall()
    if not b.selected_step_factory():
        b.selected_step_factory = 'data_loader'

    crudifier = partial(Crudifier, mall=mall)

    steps_store = steps_store or steps
    pipelines_store = pipelines_store or pipelines

    @crudifier(
        param_to_mall_map=dict(step_factory=step_factories), output_store=steps_store
    )
    def mk_step(step_factory: Callable, kwargs: dict):
        return partial(step_factory, **kwargs)

        # def mk_step(func): crudified to be sourced from funcfactory store
        mk_app(choice)

    #
    @crudifier(
        # TODO: Want to be able to do this and this only to have the effect
        # param_to_mall_map=dict(steps=steps),
        output_store=pipelines_store
    )
    def mk_pipeline(steps: Iterable[Callable]):
        print(f'{steps}')
        return Pipe(*steps)

    @crudifier(
        # TODO: Does this work if pipelines_store is a mapping instead of a string?
        param_to_mall_map=dict(pipeline=pipelines_store),
        output_store='exec_outputs',
    )
    def exec_pipeline(pipeline: Callable, kwargs):
        print(type(pipeline), Sig(pipeline))
        return pipeline(**kwargs)

    # NOTE: Just ideas. call_func not used:
    # @crudifier(
    #     param_to_mall_map=dict(pipeline='pipelines'),
    #     # output_store='exec_outputs'
    # )
    def call_func(func: Callable, *args, **kwargs):
        return func(*args, **kwargs)

    def get_step_name(step):
        return [k for k, v in mall[steps].items() if v == step][0]

    def get_selected_pipeline_sig():
        if not b.selected_pipeline():
            return Sig()
        return Sig(mall[pipelines][b.selected_pipeline()])

    config = {
        APP_KEY: {'title': 'Data Preparation'},
        RENDERING_KEY: {
            'mk_step': {
                NAME_KEY: 'Pipeline Step Maker',
                'execution': {
                    'inputs': {
                        'step_factory': {
                            ELEMENT_KEY: SelectBox,
                            'options': mall[step_factories],
                            'value': b.selected_step_factory,
                        },
                        'kwargs': {
                            ELEMENT_KEY: KwargsInput,
                            'func_sig': Sig(
                                mall[step_factories][b.selected_step_factory()]
                            ),
                        },
                    },
                    'output': {
                        ELEMENT_KEY: SuccessNotification,
                        'message': 'The step has been created successfully.',
                    },
                },
            },
            'mk_pipeline': {
                NAME_KEY: 'Pipeline Maker',
                'execution': {
                    'inputs': {
                        steps: {
                            ELEMENT_KEY: PipelineMaker,
                            'items': list(mall[steps].values()),
                            'serializer': get_step_name,
                        },
                    },
                    'output': {
                        ELEMENT_KEY: SuccessNotification,
                        'message': 'The pipeline has been created successfully.',
                    },
                },
            },
            'exec_pipeline': {
                NAME_KEY: 'Pipeline Executor',
                'execution': {
                    'inputs': {
                        'pipeline': {
                            ELEMENT_KEY: SelectBox,
                            'options': mall[pipelines],
                            'value': b.selected_pipeline,
                        },
                        'kwargs': {
                            ELEMENT_KEY: KwargsInput,
                            'func_sig': get_selected_pipeline_sig(),
                        },
                    }
                },
            },
        },
    }

    funcs = [mk_step, mk_pipeline, exec_pipeline]
    app = mk_app(funcs, config=config)

    return app


if __name__ == '__main__':
    # TODO: Try with know.malls.mk_mall:
    mall = dict(
        step_factories=dict(
            # Source Readers
            data_loader=FuncFactory(data_from_wav_folder),
            # data_loader=FuncFactory(foo),
            # Chunkers
            chunker=FuncFactory(chunker),
        ),
        steps=dict(),
        pipelines=dict(),
        exec_outputs=dict(),
    )

    app = mk_pipeline_maker_app_with_mall(
        mall, step_factories='step_factories', steps='steps', pipelines='pipelines'
    )

    app()
