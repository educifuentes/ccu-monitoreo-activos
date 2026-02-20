import streamlit as st

from models.staging.censos._stg_censos_censo_2 import stg_censos_censo_2
from models.staging.censos._stg_censos_censo_1 import stg_censos_censo_1
from models.staging.base_normalizada._stg_base_norm_censo_1 import stg_base_norm_censo_1
from models.staging.base_normalizada._stg_base_norm_locales import stg_base_norm_locales
from models.staging.base_normalizada._stg_base_norm_original import stg_base_norm_original
from models.staging.bases_ccu._stg_reportes_ccu_base_2026_q1 import stg_reportes_ccu_base_2026_q1

from utilities.ui_components import render_model_ui

# Page settings and header
st.title("Staging")
st.markdown("Tablas staging 1:1 con fuentes - Bases CCU, Contratos, Locales y Censos.")

# Create tabs for organization
tab1, tab2, tab3, tab4 = st.tabs([
    ":material/sports_bar: Locales",
    ":material/checklist_rtl: Censos",
    ":material/assignment: Bases CCU",
    ":material/book: Original"
])

with tab3:
    st.header("Base CCU 2026 Q1")
    st.markdown("Carga directa desde el reporte de CCU.")
    df = stg_reportes_ccu_base_2026_q1()
    render_model_ui(df)

with tab2:
    st.header("Censos")
    
    st.subheader("Censo 2 (2025)")
    df2 = stg_censos_censo_2()
    render_model_ui(df2)
    
    st.divider()
    
    st.subheader("Censo 1 (2024)")
    st.warning("Data histórica - Usar con precaución.")
    df1 = stg_censos_censo_1()
    render_model_ui(df1)

with tab1:
    st.header("Bases Normalizadas")
    
    st.subheader("Locales")
    df_loc = stg_base_norm_locales()
    render_model_ui(df_loc)
    
    st.divider()
    
    st.subheader("Censo 1 (Normalizado)")
    df_c1 = stg_base_norm_censo_1()
    render_model_ui(df_c1)

with tab4:
    st.header("Data Original")
    st.markdown("Primera versión de la data compartida.")
    df_orig = stg_base_norm_original()
    render_model_ui(df_orig)





