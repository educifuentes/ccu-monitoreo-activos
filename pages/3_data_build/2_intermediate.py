import streamlit as st

from models.raw.intermediate._int_censos_censo_2025_2 import int_censos_censo_2025_2
from models.raw.intermediate._int_censos_censo_2024_2 import int_censos_censo_2024_2
from models.raw.intermediate._int_base_norm_locales import int_base_norm_locales
from models.raw.marts._dim_locales import _new_locales_censo_2026_1
from models.raw.intermediate._int_censos_censo_2026_1 import int_censos_censo_2026_1_agencia_pk, int_censos_censo_2026_1_agencia_corpa
from models.raw.intermediate._int_reportes_ccu_base_2026_q1 import int_reportes_ccu_base_2026_q1, int_reportes_ccu_base_2026_q1_locales
from models.raw.intermediate._int_reportes_ccu_base_2024_q1 import int_reportes_ccu_base_2024_q1

from utilities.widgets.explorer_de_datos import explorer_de_datos
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

    render_model_ui(_new_locales_censo_2026_1())
    
with tab2:
    st.header("Censos")

    render_model_ui(int_censos_censo_2026_1_agencia_corpa(), table_name="censo_2026_1_agencia_corpa")

    render_model_ui(int_censos_censo_2026_1_agencia_pk(), table_name="censo_2026_1_agencia_pk") 

    render_model_ui(int_censos_censo_2025_2(), table_name="censo_2025_2")

    render_model_ui(int_censos_censo_2024_2(), table_name="censo_2024_2")


with tab3:
    st.header("Reportes CCU")

    st.subheader("Base 2024 Q1")
    df_2024 = int_reportes_ccu_base_2024_q1()
    render_model_ui(df_2024, table_name="base_2024_q1")

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
    render_model_ui(df_2026, table_name="base_2026_q1")


