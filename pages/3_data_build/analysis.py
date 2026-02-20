import streamlit as st

from models.analysis.compare_bases_ccu import compare_locales_df, compare_activos_df
from models.staging.base_normalizada._stg_base_norm_original import stg_base_norm_original

from utilities.ui_components import render_model_ui

# Page settings and header
st.title("Data Analysis")
st.markdown("Herramientas de comparación y perfiado de datos para validación de consistencia.")

# Create tabs for organization
tab1, tab2 = st.tabs([
    "🤝 Comparación CCU",
    "🔎 Análisis Base Normalizada"
])

with tab1:
    st.header("Comparación CCU (2024 vs 2026)")
    st.markdown("Análisis de diferencias entre la base inicial y el reporte actual de CCU.")
    
    st.subheader("Locales (Match)")
    df_locales = compare_locales_df()
    render_model_ui(df_locales)
    
    st.divider()
    
    st.subheader("Activos (Match)")
    df_activos = compare_activos_df()
    render_model_ui(df_activos)

with tab2:
    st.header("Análisis Base Normalizada")
    st.markdown("Inspección de calidad en la base original compartida.")
    
    df_orig = stg_base_norm_original()
    
    # Metrics
    null_count = df_orig['Censo 1'].isnull().sum()
    st.metric("Filas con Censo 1 nulo", null_count)
    
    st.subheader("Detalle de filas con Censo 1 nulo")
    st.dataframe(df_orig[df_orig['Censo 1'].isnull()])
    
    st.divider()
    st.subheader("Data Completa")
    render_model_ui(df_orig)
