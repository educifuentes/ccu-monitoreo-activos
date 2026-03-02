import streamlit as st
from utilities.widgets.explorer_de_datos import explorer_de_datos

from models.raw.intermediate._int_censos_censo_2 import int_censos_censo_2
from models.raw.intermediate._int_censos_censo_1 import int_censos_censo_1
from models.raw.intermediate._int_base_norm_censo_1 import int_base_norm_censo_1, clean_df_summary_censo_2024
from models.raw.intermediate._int_base_norm_locales import int_base_norm_locales

from models.raw.intermediate._int_censos_censo_2026_1 import int_censos_censo_2026_1

from models.raw.intermediate._int_reportes_ccu_base_2026_q1 import int_reportes_ccu_base_2026_q1, int_reportes_ccu_base_2026_q1_locales
from models.raw.intermediate._int_reportes_ccu_base_2024_q1 import int_reportes_ccu_base_2024_q1

from models.raw.intermediate._int_base_norm_censo_1 import int_base_norm_original_censo_2024

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
], default= ":material/checklist_rtl: Censos")

with tab1:
    st.header("Locales Intermediate")
    
    st.subheader("Base Normalizada")
    df_loc = int_base_norm_locales()
    filtered_df_loc = explorer_de_datos(df_loc)
    st.dataframe(filtered_df_loc, width='stretch')
    
    st.divider()
    
    st.subheader("Locales desde Reporte CCU 2026")
    df_ccu_loc = int_reportes_ccu_base_2026_q1_locales()
    filtered_df_ccu_loc = explorer_de_datos(df_ccu_loc)
    st.dataframe(filtered_df_ccu_loc, width='stretch')

with tab2:

    st.subheader("Censo 2026_1")
    df_c2026_1 = int_censos_censo_2026_1()
    render_model_ui(df_c2026_1) 

    st.subheader("Censo 2025_2")
    df_c2025_2 = int_censos_censo_2()
    render_model_ui(df_c2025_2) 

with tab3:
    st.header("Reportes CCU")

    st.subheader("Base 2024 Q1")
    df_2024 = int_reportes_ccu_base_2024_q1()
    render_model_ui(df_2024, source_name="reportes_ccu", table_name="base_2024_q1")

    # inspect
    empty_activos = df_2024[
        df_2024["schoperas"].isna() & 
        df_2024["coolers"].isna() & 
        df_2024["salidas"].isna()
    ]
    st.write(f"Rows with None in schoperas, coolers, and salidas: {len(empty_activos)}")
    st.dataframe(empty_activos)


    st.divider()
    
    st.subheader("Base 2026 Q1")
    df_2026 = int_reportes_ccu_base_2026_q1()
    render_model_ui(df_2026, source_name="reportes_ccu", table_name="base_2026_q1")


