import streamlit as st

from models.raw.marts._fct_censos import fct_censos
from models.raw.marts._dim_locales import dim_locales
from models.raw.marts._fct_bases_ccu import fct_bases_ccu
from models.raw.marts._fct_contratos import fct_contratos

from utilities.ui_components import render_model_ui

# Page settings and header
st.title("Finales (Marts)")
st.markdown("Tablas de Hechos (FCT) y Dimensiones (DIM) consolidadas para el negocio.")
st.markdown("estas son las Tabals que iran al gogole sheets y seran el punto de partida")
st.set_page_config(layout="wide")

# Create tabs for organization
tab1, tab2, tab3, tab4 = st.tabs([
    ":material/sports_bar: Locales",
    ":material/checklist_rtl: Censos",
    ":material/assignment: Bases CCU",
    ":material/contract: Contratos"
])

with tab1:
    st.header("Dim Locales")
    st.markdown("Tabla maestra de locales comerciales (clientes) con datos consolidados.")
    
    dim_locales_df = dim_locales()
    
    # Calculate counts for display
    fuente_counts = dim_locales_df["fuente"].value_counts().to_dict()
    fuente_str = ", ".join([f"**{k}**: {v}" for k, v in fuente_counts.items()])
    
    st.markdown(f"- Total locales: **{len(dim_locales_df)}**")
    st.markdown(f"- Distribución por fuente: {fuente_str}")
    
    render_model_ui(dim_locales_df)

with tab2:


    st.header("Fct Censos")
    st.markdown("Unión de los censos 2024-S2 y 2025-S2 con estandarización de columnas.")

    fct_censos_df = fct_censos()
    
    counts_df = fct_censos_df["periodo"].value_counts().reset_index()
    counts_df.columns = ["periodo", "count"]
    counts_df.loc[len(counts_df)] = ["Total", counts_df["count"].sum()]
    st.dataframe(counts_df)

    render_model_ui(fct_censos_df)

with tab3:
    st.header("Fact Bases CCU")
    st.markdown("Comparativa de activos entre los periodos reportados por CCU.")
    st.markdown("este es el input para el gsheets")
    fct_bases_ccu_df = fct_bases_ccu()
    
    # Key Metrics for this section
    st.dataframe(fct_bases_ccu_df["periodo"].value_counts().reset_index())


    
    render_model_ui(fct_bases_ccu_df)

with tab4:
    st.header("Fact Contratos")
    st.markdown("Información consolidada de suscripción de comodatos y términos de contrato.")
    fct_contratos_df = fct_contratos()
    render_model_ui(fct_contratos_df)
