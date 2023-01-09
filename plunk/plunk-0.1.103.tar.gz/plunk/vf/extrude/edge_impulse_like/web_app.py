from io import BytesIO
from typing import Callable
import streamlit as st
import soundfile as sf
import matplotlib.pyplot as plt
from extrude import mk_web_app
from front import APP_KEY, RENDERING_KEY, NAME_KEY, ELEMENT_KEY
from front.elements import OutputBase
from streamlitfront.elements import (
    AudioRecorder,
    FileUploader,
    MultiSourceInput,
    SuccessNotification,
    TextInput,
)

from plunk.vf.extrude.edge_impulse_like import funcs
from plunk.vf.extrude.edge_impulse_like.api import api_url


class FileReader(FileUploader):
    def render(self):
        uploaded_file = super().render()
        if uploaded_file:
            data = uploaded_file.getvalue()
            # print(data)
            # print(type(data))
            return data


class TaggedAudioPlayer(OutputBase):
    def render(self):
        if self.output:
            # wf = self.output['wf'].encode()
            # wf = self.output
            # tag = self.output['tag']
            wf, tag = self.output
            arr = sf.read(BytesIO(wf), dtype='int16')[0]
            tab1, tab2 = st.tabs(['Audio Player', 'Waveform'])
            with tab1:
                st.audio(wf)
            with tab2:
                label = f'Tag={tag}'
                # label = 'Plot'
                fig, ax = plt.subplots(figsize=(15, 5))
                ax.plot(arr, label=f'Tag={label}')
                ax.legend()
                st.pyplot(fig)


get_data_description = '''
Feed the system with wave forms from wav files or directly \
from your microphone, and tag them.
'''


if __name__ == '__main__':
    app = mk_web_app(
        funcs,
        api_url=api_url,
        config={
            APP_KEY: {'title': 'Edge-Impulse-like App'},
            RENDERING_KEY: {
                'tag_wf': {
                    NAME_KEY: 'Get Data',
                    'description': {'content': get_data_description},
                    'execution': {
                        'inputs': {
                            'wf': {
                                ELEMENT_KEY: MultiSourceInput,
                                NAME_KEY: 'Wave Form',
                                'From a file': {
                                    ELEMENT_KEY: FileReader,
                                    'type': 'wav',
                                    'display_label': False,
                                },
                                'From the microphone': {
                                    ELEMENT_KEY: AudioRecorder,
                                    # "save_dir": rootdir,
                                },
                            },
                            'save_name': {NAME_KEY: 'Save as',},
                        },
                        'output': {
                            ELEMENT_KEY: SuccessNotification,
                            'message': 'The wave form has been tagged successfully.',
                        },
                    },
                },
                'get_tagged_wf': {
                    NAME_KEY: 'Data Explorer',
                    'description': {
                        'content': '''Explore the existing tagged wave forms and play them.'''
                    },
                    'execution': {
                        'output': {ELEMENT_KEY: TaggedAudioPlayer,},
                        'auto_submit': True,
                    },
                },
            },
        },
    )
    app()
