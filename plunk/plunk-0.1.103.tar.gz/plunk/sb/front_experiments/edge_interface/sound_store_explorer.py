import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import soundfile as sf
from graze import graze
from dol import FilesOfZip, wrap_kvs, filt_iter
from io import BytesIO
from st_aggrid import GridOptionsBuilder, AgGrid, DataReturnMode, GridUpdateMode


DFLT_URL = 'https://www.dropbox.com/s/gnucwiq8wl7hes8/phone_digits_train.zip?dl=0'

# make some data
def my_obj_of_data(b):
    # return sf.read(BytesIO(b), dtype="float32")[0]
    return sf.read(BytesIO(b), dtype='int16')[0]


@wrap_kvs(obj_of_data=my_obj_of_data)
@filt_iter(filt=lambda x: not x.startswith('__MACOSX') and x.endswith('.wav'))
class WfStore(FilesOfZip):
    """Waveform access. Keys are .wav filenames and values are numpy arrays of int16 waveform."""

    pass


def keys_to_cols(all_keys):
    arr = []
    for key in all_keys:
        train_info, sref = key.split('/')
        arr.append((key, sref[0], train_info))
    df = pd.DataFrame(arr, columns=['key', 'tag', 'train'])
    return df


def mk_store_and_annots(dropbox_url=DFLT_URL):
    wf_store = WfStore(graze(dropbox_url))
    all_keys = list(wf_store.keys())
    df = keys_to_cols(all_keys)

    return wf_store, df


def display_selected_rows(wf_store, selected):
    for row in selected:
        key = row['key']
        tag = row['tag']
        arr = wf_store[key]
        fig, ax = plt.subplots(figsize=(15, 5))
        ax.plot(arr, label=f'Tag={tag}')
        ax.legend()
        st.pyplot(fig)


wf_store, df = mk_store_and_annots()

# The App
st.set_page_config(layout='wide')
st.title('Wav Store explorer')

gb = GridOptionsBuilder.from_dataframe(df)


def configure_grid(gb):
    selection_mode = 'multiple'
    groupSelectsChildren = True
    groupSelectsFiltered = True
    gb.configure_selection(selection_mode)
    gb.configure_selection(
        selection_mode,
        use_checkbox=True,
        groupSelectsChildren=groupSelectsChildren,
        groupSelectsFiltered=groupSelectsFiltered,
    )
    return gb


gb = configure_grid(gb)
gb.configure_grid_options(domLayout='normal')
gridOptions = gb.build()

return_mode = 'AS_INPUT'
return_mode_value = DataReturnMode.__members__[return_mode]
update_mode = 'MODEL_CHANGED'
update_mode_value = GridUpdateMode.__members__[update_mode]


col1, col2 = st.columns(2)

with col1:
    st.header('Display data')

    grid_response = AgGrid(
        df,
        gridOptions=gridOptions,
        width='100%',
        data_return_mode=return_mode_value,
        update_mode=update_mode_value,
    )

    df_r = grid_response['data']
    selected = grid_response['selected_rows']
    selected_df = pd.DataFrame(selected).apply(pd.to_numeric, errors='coerce')

with col2:
    st.header('Display selection')

    if selected:

        display_selected_rows(wf_store, selected)
