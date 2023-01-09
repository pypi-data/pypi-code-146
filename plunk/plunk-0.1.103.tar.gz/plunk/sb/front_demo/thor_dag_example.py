from meshed import dag, code_to_dag
from i2 import Sig
import numpy as np
from omodel.gen_utils.chunker import fixed_step_chunker
from know.boxes import *
import streamlit as st
import matplotlib.pyplot as plt
from functools import partial
from omodel.outliers.pystroll import OutlierModel as Stroll
from streamlitfront import mk_app, binder as b
from front.crude import Crudifier, prepare_for_crude_dispatch
from io import BytesIO
from front import APP_KEY, RENDERING_KEY, ELEMENT_KEY, NAME_KEY
from typing import Mapping, Iterable
from dataclasses import dataclass
from front.elements import OutputBase

from plunk.sb.front_experiments.streamlitfront_dataprep.data_prep2 import (
    # DFLT_WF_PATH,
    # DFLT_ANNOT_PATH,
    data_from_wav_folder,
)

from streamlitfront.elements import (
    SelectBox,
    SuccessNotification,
    KwargsInput,
    PipelineMaker,
)
from streamlitfront.elements import (
    AudioRecorder,
    FileUploader,
    MultiSourceInput,
)
from typing import Mapping

import soundfile as sf

DFLT_CHK_SIZE = 2048
DFLT_CHK_STEP = 2048
DFLT_FEATURIZER = lambda chk: np.abs(np.fft.rfft(chk))


def chunker(it, chk_size: int = DFLT_CHK_SIZE):
    return fixed_step_chunker(it=it, chk_size=chk_size, chk_step=chk_size)


def chunk(wfs):
    chks = list(chunker(wfs, chk_size=DFLT_CHK_SIZE))
    return chks


featurizer = DFLT_FEATURIZER
WaveForm = Iterable[int]


def featurize(chks):
    fvs = np.array(list(map(featurizer, chks)))
    return fvs


def model_run(fvs):
    # chks = list(chunker(wfs, chk_size=DFLT_CHK_SIZE))
    # fvs = np.array(list(map(featurizer, chks)))
    model = Stroll(n_centroids=50)
    model.fit(X=fvs)
    scores = model.score_samples(X=fvs)
    return scores


def prepare(tagged_data):
    sound, tag = tagged_data
    if not isinstance(sound, str):
        sound = sound.getvalue()

    arr = sf.read(BytesIO(sound), dtype='int16')[0]

    wfs = np.array(arr)
    return wfs


# @code_to_dag
# def s():
#     wfs = prepare(audio)
#     chks = chunk(wfs)
#     features = featurize(chks)
#     results = model_run(features)


@dataclass
class GraphOutput(OutputBase):
    use_container_width: bool = False

    def render(self):
        # with st.expander(self.name, True): #cannot nest expanders
        dag = self.output
        st.graphviz_chart(
            figure_or_dot=dag.dot_digraph(),
            use_container_width=self.use_container_width,
        )


@dataclass
class ArrayPlotter(OutputBase):
    def render(self):
        # st.write(f"output = {self.output}")
        X = self.output
        fig, ax = plt.subplots(figsize=(15, 5))
        ax.plot(X)
        # ax.vlines(range(len(X)), ymin=np.min(X), ymax=X)
        ax.legend()
        st.pyplot(fig)


@dataclass
class AudioDisplay(OutputBase):
    def render(self):
        sound, tag = self.output
        if not isinstance(sound, str):
            sound = sound.getvalue()

        arr = sf.read(BytesIO(sound), dtype='int16')[0]
        tab1, tab2 = st.tabs(['Audio Player', 'Waveform'])
        with tab1:
            st.audio(sound)
        with tab2:
            fig, ax = plt.subplots(figsize=(15, 5))
            ax.plot(arr, label=f'Tag={tag}')
            ax.legend()
            st.pyplot(fig)
            # st.write(arr[:10])


def mk_pipeline_maker_app_with_mall(
    mall: Mapping,
    *,
    step_factories: str = 'step_factories',
    steps: str = 'steps',
    steps_store=None,
    pipelines: str = 'pipelines',
    pipelines_store=None,
    data: str = 'data',
    data_output=None,
    data_store=None,
):
    # TODO: Like to not have this binder logic involving streamlit state here! Contain it!
    if not b.mall():
        # TODO: Maybe it's here that we need to use know.malls.mk_mall?
        b.mall = mall
    mall = b.mall()
    if not b.selected_step_factory():
        b.selected_step_factory = 'data_loader'  # TODO make this dynamic

    crudifier = partial(Crudifier, mall=mall)

    steps_store = steps_store or steps
    data_store = data_store or data
    pipelines_store = pipelines_store or pipelines

    @crudifier(
        # TODO: Does this work if pipelines_store is a mapping instead of a string?
        param_to_mall_map=dict(pipeline=pipelines_store, tagged_data='sound_output'),
        output_store='exec_outputs',
    )
    def exec_pipeline(pipeline: Callable, tagged_data):
        sound, tag = tagged_data
        if not isinstance(sound, str):
            sound = sound.getvalue()

        arr = sf.read(BytesIO(sound), dtype='int16')[0]
        result = list(
            pipeline(arr)()
        )  # TODO: because we use FuncFactories we need that hack
        return result

    @crudifier(
        # TODO: Does this work if pipelines_store is a mapping instead of a string?
        param_to_mall_map=dict(tagged_data='sound_output'),
        # output_store='exec_outputs'
    )
    def simple_model(tagged_data):
        wfs = prepare(tagged_data)
        chks = chunk(wfs)
        features = featurize(chks)
        results = model_run(features)

        return results

    @crudifier(output_store='sound_output')
    def upload_sound(train_audio: WaveForm, tag: str):
        # mall["tag_store"] = tag
        # sound, tag = train_audio, tag
        # if not isinstance(sound, str):
        #     sound = sound.getvalue()

        # arr = sf.read(BytesIO(sound), dtype="int16")[0]
        # st.write(mall)
        return train_audio, tag

    @crudifier(param_to_mall_map={'result': 'sound_output'})
    def display_tag_sound(result):
        return result

    def get_step_name(step):
        return [k for k, v in mall[steps].items() if v == step][0]

    def get_selected_pipeline_sig():
        if not b.selected_pipeline():
            return Sig()
        return Sig(mall[pipelines][b.selected_pipeline()])

    config = {
        APP_KEY: {'title': 'Data Preparation'},
        RENDERING_KEY: {
            'upload_sound': {
                # NAME_KEY: "Data Loader",
                # "description": {"content": "A very simple learn model example."},
                'execution': {
                    'inputs': {
                        'train_audio': {
                            ELEMENT_KEY: MultiSourceInput,
                            'From a file': {ELEMENT_KEY: FileUploader, 'type': 'wav',},
                            'From the microphone': {ELEMENT_KEY: AudioRecorder},
                        },
                        # "tag": {
                        #     ELEMENT_KEY: TextInput,
                        # },
                    },
                    'output': {
                        ELEMENT_KEY: SuccessNotification,
                        'message': 'Wav loaded successfully.',
                    },
                },
            },
            'display_tag_sound': {
                'execution': {
                    'inputs': {
                        'result': {
                            ELEMENT_KEY: SelectBox,
                            'options': mall['sound_output'],
                        },
                    },
                    'output': {ELEMENT_KEY: AudioDisplay,},
                },
            },
            'mk_step': {
                NAME_KEY: 'Pipeline Step Maker',
                'execution': {
                    'inputs': {
                        'step_factory': {'value': b.selected_step_factory,},
                        'kwargs': {
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
                        'pipeline': {'value': b.selected_pipeline,},
                        'data': {
                            ELEMENT_KEY: SelectBox,
                            'options': mall['sound_output'],
                        },
                    }
                },
            },
            'visualize_pipeline': {
                NAME_KEY: 'Pipeline Visualization',
                'execution': {
                    'inputs': {'pipeline': {'value': b.selected_pipeline,},},
                    'output': {
                        ELEMENT_KEY: GraphOutput,
                        NAME_KEY: 'Flow',
                        'use_container_width': True,
                    },
                },
            },
            'simple_model': {
                NAME_KEY: 'Visualize outputs',
                'execution': {
                    'inputs': {
                        'tagged_data': {
                            ELEMENT_KEY: SelectBox,
                            'options': mall['sound_output'],
                        },
                    },
                    'output': {ELEMENT_KEY: ArrayPlotter,},
                },
            },
        },
    }

    funcs = [
        upload_sound,
        display_tag_sound,
        simple_model,
        # load_data,
        # mk_step,
        # mk_pipeline,
        # exec_pipeline,
        # visualize_pipeline,
    ]
    app = mk_app(funcs, config=config)

    return app


if __name__ == '__main__':

    mall = dict(
        # Factory Input Stores
        sound_output=dict(),
        step_factories=dict(),
        # Output Store
        data=dict(),
        steps=dict(),
        pipelines=dict(),
        exec_outputs=dict(),
    )

    crudifier = partial(prepare_for_crude_dispatch, mall=mall)

    step_factories = dict(
        # Source Readers
        data_loader_factory=FuncFactory(data_from_wav_folder),
        data_loader=data_from_wav_folder,
        # Chunkers
        chunker=FuncFactory(chunker),
    )

    mall['step_factories'] = step_factories

    app = mk_pipeline_maker_app_with_mall(
        mall, step_factories='step_factories', steps='steps', pipelines='pipelines'
    )

    app()
