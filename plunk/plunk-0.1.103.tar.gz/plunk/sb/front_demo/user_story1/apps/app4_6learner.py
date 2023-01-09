"""
An app that loads either a wav file from local folder or records a sound
and visualizes the resulting numpy array 
"""
from typing import Mapping
from know.boxes import *
from functools import partial
from front import APP_KEY, RENDERING_KEY, ELEMENT_KEY, NAME_KEY
from front.crude import Crudifier

from streamlitfront import mk_app, binder as b
from streamlitfront.elements import SuccessNotification
from streamlitfront.elements import FileUploader

from plunk.sb.front_demo.user_story1.components.components import ArrayPlotter
from plunk.sb.front_demo.user_story1.utils.tools import DFLT_PIPELINE
from plunk.sb.front_demo.user_story1.utils.simple_config import Component


def mk_pipeline_maker_app_with_mall(
    mall: Mapping,
    *,
    pipelines: str = None,
    sound_output: str = None,
    models_scores: str = None
):

    from plunk.sb.front_demo.user_story1.utils.funcs import (
        learn_apply_model,
        upload_sound,
    )

    if not b.mall():
        b.mall = mall
    mall = b.mall()

    crudifier = partial(Crudifier, mall=mall)

    learn_component = Component(func=learn_apply_model)
    learn_config = learn_component.mk_configs(
        {'execution.output': {ELEMENT_KEY: ArrayPlotter,},}
    )
    learn_apply_model = crudifier(
        param_to_mall_map=dict(tagged_data='sound_output', pipeline='pipelines',),
        output_store='models_scores',
    )(learn_apply_model)

    upload_component = Component(func=upload_sound)
    upload_config = upload_component.mk_configs(
        {
            'execution.inputs.train_audio': {
                ELEMENT_KEY: FileUploader,
                'type': 'wav',
                'accept_multiple_files': True,
            },
        }
    )

    upload_sound = crudifier(output_store='sound_output')(upload_sound)

    # do the whole config to view and compare with old-style one
    # config = {
    #     APP_KEY: {"title": "Data Preparation"},
    #     RENDERING_KEY: {
    #         "upload_sound": upload_config,
    #         "learn_apply_model": {
    #             "execution": {
    #                 "output": {
    #                     ELEMENT_KEY: ArrayPlotter,
    #                 },
    #             }
    #         },
    #     },
    # }

    config = {
        APP_KEY: {'title': 'Data Preparation'},
        RENDERING_KEY: {
            'upload_sound': {
                'execution': {
                    'inputs': {
                        'train_audio': {
                            ELEMENT_KEY: FileUploader,
                            'type': 'wav',
                            'accept_multiple_files': True,
                        },
                    },
                },
            },
            'learn_apply_model': {
                NAME_KEY: 'Apply model',
                'execution': {'output': {ELEMENT_KEY: ArrayPlotter,},},
            },
        },
    }

    funcs = [
        upload_sound,
        learn_apply_model,
    ]
    app = mk_app(funcs, config=config)

    return app


if __name__ == '__main__':

    mall = dict(sound_output=dict(), pipelines=dict(), models_scores=dict(),)

    mall['sound_output'] = dict()
    mall['pipelines'] = dict(
        # ML
        default_pipeline=DFLT_PIPELINE
    )

    app = mk_pipeline_maker_app_with_mall(
        mall, pipelines='pipelines', sound_output='sound_output'
    )

    app()
