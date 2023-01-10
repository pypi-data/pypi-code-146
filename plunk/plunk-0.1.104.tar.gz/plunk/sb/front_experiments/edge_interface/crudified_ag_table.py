from front.spec_maker_base import APP_KEY, RENDERING_KEY, ELEMENT_KEY
from streamlitfront.elements import FloatSliderInput, TextOutput
from front.elements import OutputBase
from streamlitfront.base import mk_app
import streamlit as st
from st_aggrid import GridOptionsBuilder, AgGrid, DataReturnMode, GridUpdateMode
import pandas as pd
from front.crude import Crudifier
from functools import partial


d = {'A': [1, 2, 3], 'B': [4, 4, 3]}
df = pd.DataFrame(d)


class SimpleDfOutput(OutputBase):
    def render(self):
        st.write(self.output)


class TableOutput(OutputBase):
    def render(self):
        table_show(self.output)
        # st.write(self.output)


def display_df(df):
    return df


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


def table_show(df):
    gb = GridOptionsBuilder.from_dataframe(df)

    gb = configure_grid(gb)
    gb.configure_grid_options(domLayout='normal')
    gridOptions = gb.build()

    return_mode = 'AS_INPUT'
    return_mode_value = DataReturnMode.__members__[return_mode]
    update_mode = 'MODEL_CHANGED'
    update_mode_value = GridUpdateMode.__members__[update_mode]

    grid_response = AgGrid(
        df,
        gridOptions=gridOptions,
        width='100%',
        data_return_mode=return_mode_value,
        update_mode=update_mode_value,
    )

    df_r = grid_response['data']
    st.write(df_r)
    selected = grid_response['selected_rows']
    df_selected = pd.DataFrame(selected).apply(pd.to_numeric, errors='coerce')
    st.write(df_selected)


mall = {'df_store': {'stored_wf': df}}


crudify = Crudifier(param_to_mall_map={'df': 'df_store'}, mall=mall)
f = crudify(display_df)


app = mk_app(
    [f],
    config={
        APP_KEY: {'title': 'My app'},
        RENDERING_KEY: {
            'f': {
                'execution': {
                    'output': {ELEMENT_KEY: TableOutput},
                    # "options": mall["df_store"],
                }
            },
        },
    },
)
app()
