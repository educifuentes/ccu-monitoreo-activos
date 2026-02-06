import streamlit as st

from models.marts.dashboard.bi_censo_locales import bi_censo_locales
from models.marts.dashboard.bi_activos import bi_activos

from utilities.ui_components import render_model_ui

st.header("BI Tables")

# bi_censo_locales_df = bi_censo_locales()
# st.markdown("### BI Censo Locales")
# render_model_ui(bi_censo_locales_df)


st.markdown("### BI Activos")
bi_activos_df = bi_activos()
render_model_ui(bi_activos_df)
