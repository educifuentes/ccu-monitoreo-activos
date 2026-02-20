import streamlit as st

from models.analysis.compare_bases_ccu import compare_locales_df, compare_activos_df
from models.analysis.locales_base_2024 import analyze_empty_2024_locales

from models.raw.staging.base_normalizada._stg_base_norm_original import stg_base_norm_original

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

    # --- New Analysis: Locales 2024 ---
    st.divider()
    st.header("Análisis de Locales Vacíos en Base CCU 2024-Q1")
    st.markdown("Revisa los `local_id` de la Base CCU 2024 que no reportan ningún activo (schoperas, coolers, salidas) y verifica si existen en la Base Normalizada Original.")

    results = analyze_empty_2024_locales()

    col1, col2, col3 = st.columns(3)
    col1.metric("Totales (Vacíos 2024)", results["total_empty_2024"])
    col2.metric("Encontrados en Base Norm.", results["total_matched_in_base"])
    col3.metric("Faltantes en Base Norm.", results["total_missing_in_base"])

    st.subheader("Locales Encontrados en Base Original")
    if not results["df_matched"].empty:
        st.dataframe(results["df_matched"])
    else:
        st.info("Ninguno de los locales vacíos de 2024 se encontró en la base normalizada original.")

    st.subheader("Locales Faltantes en Base Original")
    if not results["df_missing"].empty:
        st.dataframe(results["df_missing"])
    else:
        st.info("Todos los locales vacíos de 2024 se encontraron en la base normalizada original.")
