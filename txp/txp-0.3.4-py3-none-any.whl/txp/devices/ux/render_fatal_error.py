"""
This module defines the helper function to draw considered fatal
errors in the web view. A fatal error will not allow to render
anything else.

An example of fatal error: Production not completed because it was interrupted.
"""
# =====================imports=====================================
import streamlit as st


def render_fatal_error():
    gateway_state = st.session_state.gateway_state
    st.markdown("-------------")
    st.subheader("Error")

    st.error(gateway_state.details.message)
