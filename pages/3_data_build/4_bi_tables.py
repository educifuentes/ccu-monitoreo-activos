import streamlit as st

# replace later with gsheets tables
from models.marts.dashboard.bi_censo_locales import bi_censo_locales
from models.marts.dashboard.bi_activos import bi_activos

from utilities.ui_components import render_model_ui

# Page settings and header
st.title("BI Tables")
st.markdown("Tablas procesadas con lógica de negocio específica para visualización en Dashboards.")

# Create tabs for organization
tab1, tab2 = st.tabs([
    "📊 BI Activos",
    "📍 BI Censo Locales"
])

with tab1:
    st.header("BI Activos")
    st.markdown("Cálculo de variaciones y estados de activos entre periodos.")
    df_activos = bi_activos()
    render_model_ui(df_activos)

with tab2:
    st.header("BI Censo Locales")
    st.markdown("Lógica de cumplimiento y cuotas basada en el último censo.")
    df_censo = bi_censo_locales()
    render_model_ui(df_censo)
