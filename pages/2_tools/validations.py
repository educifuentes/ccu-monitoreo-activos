import streamlit as st
import pandas as pd

from models.marts.gsheets.gsheets_tables import (
    locales, 
    censos, 
    bases_ccu, 
    contratos
)

from tests.test_locales import validate_locales
from tests.test_censos import validate_censos
from tests.test_bases_ccu import validate_bases_ccu
from tests.test_contratos import validate_contratos

# --- Page Config & Header ---
st.set_page_config(page_title="Validaciones", layout="wide")
st.title(":material/fact_check: Validaciones")
st.markdown("Chequeos automáticos sobre las tablas maestras (Marts) para asegurar la integridad de los reportes.")


# --- Tab Layout ---
tab1, tab2, tab3, tab4 = st.tabs([
    ":material/sports_bar: Locales",
    ":material/checklist_rtl: Censos",
    ":material/assignment: Bases CCU",
    ":material/contract: Contratos"
])

# --- Tab 1: Locales ---
with tab1:
    # test com
    df_loc = locales()
    validate_locales(df_loc)

# --- Tab 2: Censos ---
with tab2:
    df_censos = censos()
    # We reuse df_loc from tab1, but ensuring it's loaded if tab1 wasn't run is safer, 
    # though streamlit runs top-down. 
    # Better to load it if not present, but here we can assume it's available or reload.
    if 'df_loc' not in locals():
        df_loc = locales()
    validate_censos(df_censos, df_loc)

# --- Tab 3: Bases CCU ---
with tab3:
    df_bases = bases_ccu()
    if 'df_loc' not in locals():
        df_loc = locales()
    validate_bases_ccu(df_bases, df_loc)

# --- Tab 4: Contratos ---
with tab4:
    df_contratos = contratos()
    validate_contratos(df_contratos)

