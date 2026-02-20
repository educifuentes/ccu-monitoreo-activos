import streamlit as st

from scripts.reprocess_gsheet_snapshot import reprocessed_sheets
from utilities.ui_components import render_model_ui

# Page settings and header
st.set_page_config(page_title="Reprocess Sheets", layout="wide")

st.title("Reprocess sheets")
st.markdown("Tablas staging 1:1 con fuentes - Bases CCU, Contratos, Locales y Censos.")

# Get dataframes
df_bases_ccu, df_contratos = reprocessed_sheets()

# Create tabs for organization
tab1, tab2 = st.tabs([
    ":material/assignment: Bases CCU",
    ":material/book: Contratos"
])


with tab1:
    st.header("Bases CCU")
    st.markdown("Data de Bases CCU re-procesada.")
    render_model_ui(df_bases_ccu)

with tab2:
    st.header("Contratos")
    st.markdown("Data de Contratos re-procesada.")
    render_model_ui(df_contratos)




