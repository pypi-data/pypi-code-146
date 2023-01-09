# """
# An app that loads either a wav file from local folder or records a sound
# and visualizes the resulting numpy array
# """
# from typing import Mapping
# from know.boxes import *
# from functools import partial
# from typing import Callable, Iterable
# from front import APP_KEY, RENDERING_KEY, ELEMENT_KEY, NAME_KEY
# from i2 import Pipe, Sig
# from front.crude import Crudifier, prepare_for_crude_dispatch
# from lined import LineParametrized
# import numpy as np

# from streamlitfront import mk_app, binder as b
# from streamlitfront.elements import (
#     SelectBox,
#     SuccessNotification,
#     PipelineMaker,
# )
# from streamlitfront.elements import (
#     AudioRecorder,
#     FileUploader,
#     MultiSourceInput,
# )
# import streamlit as st

# import soundfile as sf
# from io import BytesIO
# from plunk.sb.front_demo.user_story1.components.components import (
#     AudioArrayDisplay,
#     GraphOutput,
#     ArrayPlotter,
#     ArrayWithIntervalsPlotter,
# )
# from plunk.sb.front_demo.user_story1.utils.tools import (
#     DFLT_FEATURIZER,
#     DFLT_CHK_SIZE,
#     chunker,
#     WaveForm,
#     Stroll,
#     clean_dict,
#     scores_to_intervals,
# )
# from typing import List


# def simple_chunker(wfs, chk_size: int = DFLT_CHK_SIZE):
#     return list(chunker(wfs, chk_size=chk_size))


# def simple_featurizer(chks):
#     fvs = np.array(list(map(DFLT_FEATURIZER, chks)))
#     return fvs


# def tagged_sound_to_array(train_audio: WaveForm, tag: str):
#     sound, tag = train_audio, tag
#     if not isinstance(sound, bytes):
#         sound = sound.getvalue()

#     arr = sf.read(BytesIO(sound), dtype="int16")[0]
#     return arr, tag


# def tagged_sounds_to_single_array(train_audio: List[WaveForm], tag: str):
#     sounds, tag = train_audio, tag
#     result = []
#     for sound in sounds:
#         # if not isinstance(sound, bytes):
#         sound = sound.getvalue()
#         arr = sf.read(BytesIO(sound), dtype="int16")[0]
#         result.append(arr)
#     # print(np.hstack(result))
#     return np.hstack(result).reshape(-1, 1), tag


# def assert_dims(wfs):
#     if wfs.ndim >= 2:
#         wfs = wfs[:, 0]
#     return wfs


# def mk_pipeline_maker_app_with_mall(
#     mall: Mapping,
#     *,
#     step_factories: str = "step_factories",
#     steps: str = "steps",
#     steps_store=None,
#     pipelines: str = "pipelines",
#     pipelines_store=None,
#     data: str = "data",
#     data_store=None,
#     learned_models=None,
#     models_scores=None,
# ):
#     if not b.mall():
#         b.mall = mall
#     mall = b.mall()
#     if not b.selected_step_factory():
#         b.selected_step_factory = "chunker"  # TODO make this dynamic

#     crudifier = partial(Crudifier, mall=mall)

#     steps_store = steps_store or steps
#     data_store = data_store or data
#     pipelines_store = pipelines_store or pipelines

#     @crudifier(
#         param_to_mall_map=dict(step_factory=step_factories), output_store=steps_store
#     )
#     def mk_step(step_factory: Callable, kwargs: dict):
#         kwargs = clean_dict(kwargs)  # TODO improve that logic
#         step = partial(step_factory, **kwargs)()

#         return step

#     #
#     @crudifier(
#         output_store=pipelines_store,
#     )
#     def mk_pipeline(steps: Iterable[Callable]):
#         return LineParametrized(*steps)

#     @crudifier(
#         param_to_mall_map=dict(pipeline=pipelines_store, tagged_data="sound_output"),
#         output_store="exec_outputs",
#     )
#     def exec_pipeline(pipeline: Callable, tagged_data):

#         sound, _ = tagged_sound_to_array(*tagged_data)
#         wfs = np.array(sound)
#         wfs = assert_dims(wfs)

#         result = pipeline(wfs)
#         return result

#     @crudifier(
#         param_to_mall_map=dict(
#             tagged_data="sound_output", preprocess_pipeline="pipelines"
#         ),
#         output_store="learned_models",
#     )
#     def learn_outlier_model(tagged_data, preprocess_pipeline, n_centroids=5):
#         sound, tag = tagged_sounds_to_single_array(*tagged_data)
#         wfs = np.array(sound)

#         wfs = assert_dims(wfs)

#         fvs = preprocess_pipeline(wfs)
#         model = Stroll(n_centroids=n_centroids)
#         model.fit(X=fvs)

#         return model

#     @crudifier(
#         param_to_mall_map=dict(
#             tagged_data="sound_output",
#             preprocess_pipeline="pipelines",
#             fitted_model="learned_models",
#         ),
#         output_store="models_scores",
#     )
#     def apply_fitted_model(tagged_data, preprocess_pipeline, fitted_model):
#         sound, tag = tagged_sounds_to_single_array(*tagged_data)
#         wfs = np.array(sound)
#         wfs = assert_dims(wfs)

#         fvs = preprocess_pipeline(wfs)
#         scores = fitted_model.score_samples(X=fvs)
#         return scores

#     @crudifier(
#         param_to_mall_map=dict(pipeline=pipelines_store),
#     )
#     def visualize_pipeline(pipeline: LineParametrized):

#         return pipeline

#     @crudifier(
#         param_to_mall_map=dict(scores="models_scores"),
#     )
#     def visualize_scores(scores, threshold=80, num_segs=3):

#         intervals = scores_to_intervals(scores, threshold, num_segs)

#         return scores, intervals

#     @crudifier(output_store="sound_output")
#     def upload_sound(train_audio: List[WaveForm], tag: str):
#         # sound, tag = train_audio, tag
#         # if not isinstance(sound, bytes):
#         #     sound = sound.getvalue()

#         # arr = sf.read(BytesIO(sound), dtype='int16')[0]
#         # return arr, tag
#         return train_audio, tag

#     @crudifier(param_to_mall_map={"result": "sound_output"})
#     def display_tag_sound(result):
#         return result

#     def get_step_name(step):
#         return [k for k, v in mall[steps].items() if v == step][0]

#     def get_selected_pipeline_sig():
#         if not b.selected_pipeline():
#             return Sig()
#         return Sig(mall[pipelines][b.selected_pipeline()])

#     config = {
#         APP_KEY: {"title": "Data Preparation"},
#         RENDERING_KEY: {
#             "upload_sound": {
#                 # NAME_KEY: "Data Loader",
#                 "execution": {
#                     "inputs": {
#                         "train_audio": {
#                             ELEMENT_KEY: FileUploader,
#                             "type": "wav",
#                             "accept_multiple_files": True,
#                         },
#                     },
#                     "output": {
#                         ELEMENT_KEY: SuccessNotification,
#                         "message": "Wav files loaded successfully.",
#                     },
#                 },
#             },
#             "display_tag_sound": {
#                 "execution": {
#                     "inputs": {
#                         "result": {
#                             ELEMENT_KEY: SelectBox,
#                             "options": mall["sound_output"],
#                         },
#                     },
#                     "output": {
#                         ELEMENT_KEY: AudioArrayDisplay,
#                     },
#                 },
#             },
#             "mk_step": {
#                 NAME_KEY: "Pipeline Step Maker",
#                 "execution": {
#                     "inputs": {
#                         "step_factory": {
#                             "value": b.selected_step_factory,
#                         },
#                         "kwargs": {
#                             "func_sig": Sig(
#                                 mall[step_factories][b.selected_step_factory()]
#                             ),
#                         },
#                     },
#                     "output": {
#                         ELEMENT_KEY: SuccessNotification,
#                         "message": "The step has been created successfully.",
#                     },
#                 },
#             },
#             "mk_pipeline": {
#                 NAME_KEY: "Pipeline Maker",
#                 "execution": {
#                     "inputs": {
#                         steps: {
#                             ELEMENT_KEY: PipelineMaker,
#                             "items": list(mall[steps].values()),
#                             "serializer": get_step_name,
#                         },
#                     },
#                     "output": {
#                         ELEMENT_KEY: SuccessNotification,
#                         "message": "The pipeline has been created successfully.",
#                     },
#                 },
#             },
#             "exec_pipeline": {
#                 NAME_KEY: "Pipeline Executor",
#                 "execution": {
#                     "inputs": {
#                         "pipeline": {
#                             "value": b.selected_pipeline,
#                         },
#                         "data": {
#                             ELEMENT_KEY: SelectBox,
#                             "options": mall["sound_output"],
#                         },
#                     }
#                 },
#             },
#             "visualize_pipeline": {
#                 NAME_KEY: "Pipeline Visualization",
#                 "execution": {
#                     "inputs": {
#                         "pipeline": {
#                             "value": b.selected_pipeline,
#                         },
#                     },
#                     "output": {
#                         ELEMENT_KEY: GraphOutput,
#                         NAME_KEY: "Flow",
#                         "use_container_width": True,
#                     },
#                 },
#             },
#             "visualize_scores": {
#                 NAME_KEY: "Scores Visualization",
#                 "execution": {
#                     "inputs": {
#                         "scores": {
#                             ELEMENT_KEY: SelectBox,
#                             "options": mall["models_scores"],
#                         },
#                     },
#                     "output": {
#                         ELEMENT_KEY: ArrayWithIntervalsPlotter,
#                     },
#                 },
#             },
#             "simple_model": {
#                 NAME_KEY: "Learn model",
#                 "execution": {
#                     "inputs": {
#                         "tagged_data": {
#                             ELEMENT_KEY: SelectBox,
#                             "options": mall["sound_output"],
#                         },
#                         "preprocess_pipeline": {
#                             ELEMENT_KEY: SelectBox,
#                             "options": mall["pipelines"],
#                         },
#                     },
#                     "output": {
#                         ELEMENT_KEY: ArrayPlotter,
#                     },
#                 },
#             },
#             "apply_fitted_model": {
#                 NAME_KEY: "Apply model",
#                 "execution": {
#                     "inputs": {
#                         "tagged_data": {
#                             ELEMENT_KEY: SelectBox,
#                             "options": mall["sound_output"],
#                         },
#                         "preprocess_pipeline": {
#                             ELEMENT_KEY: SelectBox,
#                             "options": mall["pipelines"],
#                         },
#                         "learned_model": {
#                             ELEMENT_KEY: SelectBox,
#                             "options": mall["learned_models"],
#                         },
#                     },
#                     "output": {
#                         ELEMENT_KEY: ArrayPlotter,
#                     },
#                 },
#             },
#         },
#     }

#     funcs = [
#         upload_sound,
#         # display_tag_sound,
#         mk_step,
#         mk_pipeline,
#         learn_outlier_model,
#         apply_fitted_model,
#         # exec_pipeline,
#         visualize_pipeline,
#         visualize_scores,
#     ]
#     app = mk_app(funcs, config=config)

#     return app


# if __name__ == "__main__":

#     mall = dict(
#         # Factory Input Stores
#         sound_output=dict(),
#         step_factories=dict(),
#         # Output Store
#         data=dict(),
#         steps=dict(),
#         pipelines=dict(),
#         exec_outputs=dict(),
#         learned_models=dict(),
#         models_scores=dict(),
#     )

#     crudifier = partial(prepare_for_crude_dispatch, mall=mall)

#     step_factories = dict(
#         # ML
#         chunker=FuncFactory(simple_chunker),
#         featurizer=FuncFactory(simple_featurizer),
#     )

#     mall["step_factories"] = step_factories

#     app = mk_pipeline_maker_app_with_mall(
#         mall, step_factories="step_factories", steps="steps", pipelines="pipelines"
#     )

#     app()


import streamlit as st
from s3dol import get_s3_client, S3BucketBaseReader


# bucket_name ='s3://drillnoise/DrillDataset/'
bucket_name = 'drillnoise'

# r = S3BucketBaseReader(S3BucketBaseReader.mk_client(**resources_kwargs), bucket='bucket_name', prefix='my_stuff/')
client = get_s3_client(**st.secrets.s3_credentials)
r = S3BucketBaseReader(client, bucket=bucket_name)
st.write(list(r.keys()))

# save locally the store and do it as fileupload
