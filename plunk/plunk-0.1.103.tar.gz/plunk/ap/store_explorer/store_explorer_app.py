"""An app that loads wav file from local folder"""
from functools import partial, reduce
from typing import Iterable

from front import APP_KEY, RENDERING_KEY, ELEMENT_KEY

from front.crude import Crudifier

from streamlitfront import mk_app
from streamlitfront.elements import SuccessNotification
from streamlitfront.elements import FileUploader

from plunk.ap.store_explorer.store_explorer_element import (
    get_mall,
    StoreExplorerOutput,
    StoreExplorerInput,
)


def mk_pipeline_maker_app_with_mall(mall: dict):
    mall = get_mall(mall)

    crudifier = partial(Crudifier, mall=mall)

    @crudifier(output_store='sound_output')
    def upload_sound(train_audio: list, tag: str):
        return train_audio, tag

    def explore_mall(depth_keys: Iterable = ()):
        return depth_keys, reduce(lambda o, k: o[k], depth_keys, mall)

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
            'explore_mall': {
                'execution': {
                    'inputs': {
                        'depth_keys': {ELEMENT_KEY: StoreExplorerInput, 'mall': mall}
                    },
                    'output': {
                        ELEMENT_KEY: StoreExplorerOutput,
                        'write_depth_keys': True,
                    },
                    'auto_submit': True,
                },
            },
        },
    }

    funcs = [
        explore_mall,
        upload_sound,
    ]
    app = mk_app(funcs, config=config)

    return app


_mall = dict(
    # Factory Input Stores
    sound_output=dict(),
    # Output Store
    data=dict(
        a=1,
        b='2',
        c=[3],
        d={'4': 4, '5': [{'e': 6}, {'f': 7}, ['g', 'h', 'i']]},
        j=[{'k': 8, 'l': 9}, 'm', 10],
    ),
)


if __name__ == '__main__':

    app = mk_pipeline_maker_app_with_mall(_mall)

    app()
