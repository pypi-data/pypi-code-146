import streamlit as st
import pandas as pd

# POSSIBLES VIEWS
_PRODUCTION_LINES_VIEWKEY = 'PRODUCTION_LINES'
_PRODUCTION_LINES_DETAIL_VIEWKEY = 'PRODUCTION_LINES'

st.set_page_config(layout="wide")

if not st.session_state.get('initialized', None):
    st.session_state.current_view = _PRODUCTION_LINES_VIEWKEY
    st.session_state.initialized = True
    st.session_state.production_lines = pd.DataFrame(
        [f'<a target="_self" href="#linea_rapida_cereal">Línea rápida de Cereal</a>',
         f'<a target="_self" href="#linea_de_empaquetado">Linea de empaquetado</a>'],
        columns=['Línea de Producción'],
    )
    st.experimental_rerun()
