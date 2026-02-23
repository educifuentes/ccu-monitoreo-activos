import streamlit as st
from models.gsheets.staging.gsheets_tables import (
    locales, 
    censos, 
    bases_ccu, 
    contratos
)
from utilities.ui_components import render_model_ui

# --- Page Config & Header ---
st.title("Google Sheets Data")
st.markdown("Tablas  en Google Sheets que actúan como **Puntos de Partida**.")
st.markdown("Fuente de datos principal para el desarrollo de los modelos debe ser 1 a 1 con las generadas en Finals Marts")
st.set_page_config(layout="wide")

# --- Tab Layout ---
tab1, tab2, tab3, tab4 = st.tabs([
    ":material/sports_bar: Locales",
    ":material/checklist_rtl: Censos",
    ":material/assignment: Bases CCU",
    ":material/contract: Contratos"
])

# --- Tab Content ---

with tab1:
    st.header("Locales (GSheets)")
    st.markdown("Maestro de locales comerciales.")
    try:
        df_locales = locales()
        render_model_ui(df_locales)
    except Exception as e:
        st.error(f"Error cargando worksheet 'locales': {e}")

with tab2:
    st.header("Censos (GSheets)")
    st.markdown("Registros históricos y actuales de censos.")
    try:
        df_censos = censos()
        render_model_ui(df_censos)
    except Exception as e:
        st.error(f"Error cargando worksheet 'censos': {e}")

with tab3:
    st.header("Bases CCU (GSheets)")
    st.markdown("Información de activos reportada por CCU.")
    try:
        df_bases = bases_ccu()
        render_model_ui(df_bases)
    except Exception as e:
        st.error(f"Error cargando worksheet 'bases_ccu': {e}")

with tab4:
    st.header("Contratos (GSheets)")
    st.markdown("Datos consolidados de contratos y comodatos.")
    try:
        df_contratos = contratos()
        render_model_ui(df_contratos)
    except Exception as e:
        st.error(f"Error cargando worksheet 'contratos': {e}")
