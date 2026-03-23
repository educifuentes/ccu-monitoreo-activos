import streamlit as st

from helpers.ui_components.model_details_ui import render_model_details

# Retrieve query params from URL or session state (since st.switch_page drops query params)
model_name = st.query_params.get("model") or st.session_state.get("selected_model")

render_model_details(model_name)