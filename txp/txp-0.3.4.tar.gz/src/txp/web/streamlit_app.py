"""
The streamlit entrypoint for the streamlit cloud application.
Currently this is a "Hello World" used to test the txp classes in the
streamlit cloud deployment.
"""
# ============================ imports =========================================
from txp.web.core_components.main_app_component import MainAppComponent
from txp.web.views import *

import streamlit as st

st.set_page_config(layout="wide")


# ========================= Main App ============================================
def initialize_app():
    if 'initialized' not in st.session_state:
        app_component = MainAppComponent()  # Create the layout component
        app_component.add_child_component(AssetConditionsView(), make_current=True)
        app_component.add_child_component(ReportView())
        app_component.add_child_component(DeviceHealthView())
        app_component.add_child_component(TelemetryHealthView())
        app_component.add_child_component(AnalyticsView())

        st.session_state.initialized = True
        st.session_state.app_layout = app_component


initialize_app()
st.session_state.app_layout.render()
