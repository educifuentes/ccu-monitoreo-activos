import streamlit as st
from utilities.widgets.explorer_de_datos import explorer_de_datos

from models.intermediate._int_censos_censo_2 import int_censos_censo_2
from models.intermediate._int_censos_censo_1 import int_censos_censo_1
from models.intermediate._int_base_norm_censo_1 import int_base_norm_censo_1
from models.intermediate._int_base_norm_locales import int_base_norm_locales
from models.intermediate._int_reportes_ccu_base_2026_q1 import int_reportes_ccu_base_2026_q1, int_reportes_ccu_base_2026_q1_locales
from models.intermediate._int_reportes_ccu_base_2024_q1 import int_reportes_ccu_base_2024_q1

from utilities.ui_components import render_model_ui

# Page settings and header
st.set_page_config(page_title="Intermediate", layout="wide")

st.title("Intermediate")
st.markdown("Capa intermedia de limpieza, tipado y transformaciones de negocio.")

# Create tabs for organization
tab1, tab2, tab3 = st.tabs([
    ":material/sports_bar: Locales",    
    ":material/checklist_rtl: Censos",
    ":material/assignment: Bases CCU"
])

with tab1:
    st.header("Locales Intermediate")
    
    st.subheader("Base Normalizada")
    df_loc = int_base_norm_locales()
    filtered_df_loc = explorer_de_datos(df_loc)
    st.dataframe(filtered_df_loc, use_container_width=True)
    
    st.divider()
    
    st.subheader("Locales desde Reporte CCU 2026")
    df_ccu_loc = int_reportes_ccu_base_2026_q1_locales()
    filtered_df_ccu_loc = explorer_de_datos(df_ccu_loc)
    st.dataframe(filtered_df_ccu_loc, use_container_width=True)

with tab2:
    st.header("Censos Intermediate")
    
    st.subheader("Censo 2 (2025)")
    st.markdown("**Notas:** Se asume 'CANTIDAD DE SALIDAS' como salidas_ccu.")
    df_c2 = int_censos_censo_2()
    render_model_ui(df_c2)
    
    st.divider()
    
    st.subheader("Censo 1 (2024)")
    st.markdown("**Notas:** Limpieza de IDs nulos y agencias.")
    df_c1 = int_censos_censo_1()
    render_model_ui(df_c1)
    
    st.divider()
    
    st.subheader("Censo 2 + Locales (Match)")
    locales_df = int_base_norm_locales()
    df_merged = df_c2.merge(locales_df, on="local_id", how="left", indicator=True)
    
    missing_locales = df_merged[df_merged["_merge"] == "left_only"]
    if not missing_locales.empty:
        st.warning(f"Hay {len(missing_locales)} filas en Censo 2 que no tienen match en Locales")
    
    render_model_ui(df_merged)

with tab3:
    st.header("Reportes CCU")
    
    st.subheader("Base 2026 Q1")
    df_2026 = int_reportes_ccu_base_2026_q1()
    render_model_ui(df_2026, source_name="reportes_ccu", table_name="base_2026_q1")
    
    st.divider()
    
    st.subheader("Base 2024 Q1")
    df_2024 = int_reportes_ccu_base_2024_q1()
    render_model_ui(df_2024, source_name="reportes_ccu", table_name="base_2024_q1")



