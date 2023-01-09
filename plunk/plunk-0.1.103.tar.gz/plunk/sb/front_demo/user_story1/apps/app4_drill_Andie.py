"""
An app that loads either a wav file from local folder or records a sound
and visualizes the resulting numpy array 
"""
from typing import Mapping
from know.boxes import *
from functools import partial
from front import APP_KEY, RENDERING_KEY, ELEMENT_KEY

from front.crude import Crudifier
import numpy as np

from streamlitfront import mk_app, binder as b
from streamlitfront.elements import SuccessNotification
from streamlitfront.elements import FileUploader

import soundfile as sf
from io import BytesIO

from plunk.sb.front_demo.user_story1.utils.tools import WaveForm
from typing import List


def mk_pipeline_maker_app_with_mall(
    mall: Mapping,
    *,
    step_factories: str = 'step_factories',
    steps: str = 'steps',
    steps_store=None,
    pipelines: str = 'pipelines',
    pipelines_store=None,
    data: str = 'data',
    data_store=None,
    learned_models=None,
    models_scores=None,
):
    if not b.mall():
        b.mall = mall
    mall = b.mall()

    crudifier = partial(Crudifier, mall=mall)

    @crudifier(output_store='sound_output')
    def upload_sound(train_audio: List[WaveForm], tag: str):

        return train_audio, tag

    config = {
        APP_KEY: {'title': 'Data Preparation'},
        RENDERING_KEY: {
            'upload_sound': {
                # NAME_KEY: "Data Loader",
                'execution': {
                    'inputs': {
                        'train_audio': {
                            ELEMENT_KEY: FileUploader,
                            'type': 'wav',
                            'accept_multiple_files': True,
                        },
                    },
                    'output': {
                        ELEMENT_KEY: SuccessNotification,
                        'message': 'Wav files loaded successfully.',
                    },
                },
            },
        },
    }

    funcs = [
        upload_sound,
    ]
    app = mk_app(funcs, config=config)

    return app


mall = dict(
    # Factory Input Stores
    sound_output=dict(),
    # Output Store
    data=dict(),
)


if __name__ == '__main__':

    app = mk_pipeline_maker_app_with_mall(mall,)

    app()
