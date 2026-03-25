import streamlit as st

from tests.test_clientes import validate_locales
from tests.test_censos import validate_censos
from tests.test_bases_ccu import validate_bases_ccu
from tests.test_contratos import validate_contratos

# --- Page Config & Header ---
st.set_page_config(page_title="Validaciones", layout="wide")
st.title(":material/fact_check: Validaciones")
st.markdown("Chequeos automáticos sobre las tablas fuente para asegurar la integridad de los reportes.")

# --- Tab Layout ---
tab1, tab2, tab3, tab4 = st.tabs([
    ":material/sports_bar: Clientes",
    ":material/checklist_rtl: Censos",
    ":material/assignment: Bases CCU",
    ":material/contract: Contratos",
])

with tab1:
    validate_locales()

with tab2:
    validate_censos()

with tab3:
    validate_bases_ccu()

with tab4:
    validate_contratos()
