from dataclasses import dataclass
import streamlit as st
import numpy as np
import pandas as pd
from front.crude import Crudifier
import matplotlib.pyplot as plt
from typing import Any

# from plunk.sb.front_experiments.data_visualizer.dags.wfstore_and_annots_to_dataset import (
#     load_dataset,
# )
# from plunk.sb.front_experiments.data_visualizer.components.elements import (
#     # DataLoader,
#     # DataLoader2,
#     ZipWavDataLoader,
# )
# from functools import partial
from plunk.sb.front_experiments.data_visualizer.utils.tools import (
    store_to_key_fvs,
    key_fvs_to_tag_fvs,
    mk_Xy,
)
from streamlitfront import mk_app, binder as b
from front import APP_KEY, RENDERING_KEY, ELEMENT_KEY
from streamlitfront.elements import SelectBox
from front.elements import OutputBase
import umap
import umap.plot
from hear import WavLocalFileStore


root_dir = '/Users/sylvain/Dropbox/_odata/sound/vacuum'
annots_path = '../data/annots_vacuum.csv'


# ============ BACKEND ============


def load_dataset(folder_path: str, annot_path: str):
    wf_store = WavLocalFileStore(folder_path)
    df = pd.read_csv(annot_path)
    key_fvs = store_to_key_fvs(wf_store)
    tag_fv_iterator = key_fvs_to_tag_fvs(key_fvs, annots_df=df)
    X, y = mk_Xy(tag_fv_iterator)  # Cmd+]

    return X, y


def plot_umap(Xy: Any):
    return Xy
    # X, y = Xy
    # mapper = umap.UMAP().fit(X)
    # umap.plot.points(mapper, labels=np.array(y), show_legend=show_legend)


# ============ END BACKEND ============


# ============ FRONT END   ============


if not b.mall():
    b.mall = dict(Xy={})
mall = b.mall()

load_dataset = Crudifier(output_store='Xy', mall=mall)(load_dataset)


# plot_umap = Crudifier(param_to_mall_map=dict(Xy="Xy"), mall=mall)(plot_umap)

plot_umap = Crudifier(param_to_mall_map=['Xy'], mall=mall)(plot_umap)


@dataclass
class UmapPlotter(OutputBase):
    def render(self):
        # st.write(f"output = {self.output}")
        X, y = self.output
        mapper = umap.UMAP().fit(X)
        fig, ax = plt.subplots()
        show_legend = st.checkbox(label='Show legend')
        umap.plot.points(mapper, labels=np.array(y), show_legend=show_legend, ax=ax)
        st.pyplot(fig)


config_ = {
    APP_KEY: {'title': 'Data Visualizer'},
    RENDERING_KEY: {
        'load_dataset': {
            # NAME_KEY: "Get Data",
            # "description": {"content": get_data_description},
            # "execution": {
            #     "inputs": {
            #         "folder_path": {
            #             ELEMENT_KEY: ZipWavDataLoader,
            #         }
            #     }
            # },
        },
        'plot_umap': {
            # NAME_KEY: "Get Data",
            # "description": {"content": get_data_description},
            'execution': {
                'inputs': {'Xy': {ELEMENT_KEY: SelectBox, 'options': mall['Xy']},},
                'output': {ELEMENT_KEY: UmapPlotter},
                # "auto_submit": True,
            },
        },
    },
}
# ============ END FRONTEND ============

if __name__ == '__main__':
    app = mk_app([load_dataset, plot_umap], config=config_)
    app()
st.write(mall)
