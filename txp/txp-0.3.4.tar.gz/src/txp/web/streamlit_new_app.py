# ============================ imports =========================================
from txp.web.core_components.main_app_component import MainAppComponent
from txp.web.views import *
from txp.web.new_views import *
import streamlit as st
import threading
from streamlit.script_run_context import get_script_run_ctx


st.set_page_config(layout="wide")

# REMOVE RUNNING MAN FROM SCREEN
hide_streamlit_style = """
                <style>
                div[data-testid="stToolbar"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                div[data-testid="stDecoration"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                div[data-testid="stStatusWidget"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                #MainMenu {
                visibility: hidden;
                height: 0%;
                }
                header {
                visibility: hidden;
                height: 0%;
                }
                footer {
                visibility: hidden;
                height: 0%;
                }
                </style>
                """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# ========================= Main App ============================================
def initialize_app():
    if 'initialized' not in st.session_state:
        app_component = MainAppComponent()  # Create the layout component

        st.session_state.initialized = True
        app_component.add_child_component(GeneralDashboard(), make_current=True)
        app_component.add_child_component(EquipmentDetails())
        st.session_state.app_layout = app_component


initialize_app()
st.session_state.app_layout.render()


