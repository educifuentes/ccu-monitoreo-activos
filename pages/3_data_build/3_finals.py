import streamlit as st

from models.marts._fct_censos import fct_censos
from models.marts._dim_locales import dim_locales
from models.marts._fct_bases_ccu import fct_bases_ccu
from models.marts._fct_contratos import fct_contratos_ccu

from utilities.ui_components import render_model_ui

# Page settings and header
st.title("Finales (Marts)")
st.markdown("Tablas de Hechos (FCT) y Dimensiones (DIM) consolidadas para el negocio.")
st.markdown("estas son las Tabals que iran al gogole sheets y seran el punto de partida")

# Create tabs for organization
tab1, tab2, tab3, tab4 = st.tabs([
    ":material/sports_bar: Locales",
    ":material/checklist_rtl: Censos",
    ":material/assignment: Bases CCU",
    ":material/contract: Contratos"
])

with tab4:
    st.header("Fact Contratos CCU")
    st.markdown("Información consolidada de suscripción de comodatos y términos de contrato.")
    fct_contratos_ccu_df = fct_contratos_ccu()
    
    # multi_fecha_count = fct_contratos_ccu_df[
    #     (fct_contratos_ccu_df["fecha_suscripcion_comodato_es_rango"] == True)
    # ].shape[0]

    # st.markdown(f"- Hay **{multi_fecha_count}** locales con multi fecha en inicio o término de contratos.")
    render_model_ui(fct_contratos_ccu_df)



with tab2:
    st.header("Fact Censos")
    st.markdown("Unión de los censos 2024-S2 y 2025-S2 con estandarización de columnas.")
    fct_censos_df = fct_censos()
    render_model_ui(fct_censos_df)

with tab3:
    st.header("Fact Bases CCU")
    st.markdown("Comparativa de activos entre los periodos reportados por CCU.")
    fct_bases_ccu_df = fct_bases_ccu()
    
    # Key Metrics for this section
    count_ambos = fct_bases_ccu_df[fct_bases_ccu_df["en_ambos_periodos"] == True]["local_id"].nunique()
    total_locales = fct_bases_ccu_df["local_id"].nunique()
    
    col1, col2 = st.columns(2)
    col1.metric("Locales en ambos periodos", count_ambos)
    col2.metric("Total Locales Únicos", total_locales)
    
    render_model_ui(fct_bases_ccu_df)

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




