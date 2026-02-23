import streamlit as st

from models.raw.staging.censos._stg_censos_censo_2 import stg_censos_censo_2
from models.raw.staging.censos._stg_censos_censo_1 import stg_censos_censo_1
from models.raw.staging.base_normalizada._stg_base_norm_censo_1 import stg_base_norm_censo_1
from models.raw.staging.base_normalizada._stg_base_norm_locales import stg_base_norm_locales

from models.raw.staging.base_normalizada._stg_base_norm_original import stg_base_norm_original, stg_base_norm_original_base_ccu_2024

from models.raw.staging.bases_ccu._stg_reportes_ccu_base_2026_q1 import stg_reportes_ccu_base_2026_q1

from utilities.widgets.explorer_de_datos import explorer_de_datos
from utilities.ui_components import render_model_ui

# Page settings and header
st.title("Staging")
st.markdown("Tablas staging 1:1 con fuentes - Bases CCU, Contratos, Locales y Censos.")

st.set_page_config(layout="wide")

# Create tabs for organization
tab1, tab2, tab3, tab4 = st.tabs([
    ":material/sports_bar: Locales",
    ":material/checklist_rtl: Censos",
    ":material/assignment: Bases CCU",
    ":material/book: Base Norm Original"
], default=":material/book: Base Norm Original")

with tab3:
    st.header("Base CCU 2026 Q1")
    st.markdown("Carga directa desde el reporte de CCU.")
    df = stg_reportes_ccu_base_2026_q1()
    filtered_df = explorer_de_datos(df)
    render_model_ui(filtered_df)

    st.divider()
    

    


with tab2:
    st.header("Censos")
    
    st.subheader("Censo 2 (2025)")
    df2 = stg_censos_censo_2()
    filtered_df2 = explorer_de_datos(df2)
    render_model_ui(filtered_df2)
    
    st.divider()
    
    st.subheader("Censo 1 (2024)")
    st.warning("Data histórica - Usar con precaución.")
    df1 = stg_censos_censo_1()
    filtered_df1 = explorer_de_datos(df1)
    render_model_ui(filtered_df1)

with tab1:
    st.header("Bases Normalizadas")
    
    st.subheader("Locales")
    df_loc = stg_base_norm_locales()
    filtered_df_loc = explorer_de_datos(df_loc)
    render_model_ui(filtered_df_loc)
    
    st.divider()
    
    st.subheader("Censo 1 (Normalizado)")
    df_c1 = stg_base_norm_censo_1()
    filtered_df_c1 = explorer_de_datos(df_c1)
    render_model_ui(filtered_df_c1)

with tab4:
    st.header("Data Original")
    st.markdown("Primera versión de la data compartida.")
    df_orig = stg_base_norm_original()
    filtered_df_orig = explorer_de_datos(df_orig)
    render_model_ui(filtered_df_orig)

    st.subheader("Base CCU 2024 Q1")
    df_base_ccu_2024 = stg_base_norm_original_base_ccu_2024()
    render_model_ui(df_base_ccu_2024)

    # st.subheader("Censo 2024 Q1")
    # df_censo_2024 = stg_base_norm_original_censo_2024()
    # render_model_ui(df_censo_2024)





