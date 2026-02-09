import streamlit as st

# replace later with gsheets tables
from models.marts.dashboard.bi_censos import bi_censos
from models.marts.dashboard.bi_activos import bi_activos
from models.marts.dashboard.bi_locales import bi_locales
from models.marts.dashboard.bi_contratos import bi_contratos

from utilities.ui_components import render_model_ui

# Page settings and header
st.title("BI Tables")
st.markdown("Tablas procesadas con lógica de negocio específica para visualización en Dashboards.")

# --- Load Data (Top Level) ---
df_activos = bi_activos()
df_censos = bi_censos()
df_locales = bi_locales()
df_contratos = bi_contratos()

# Create tabs for organization using Material Icons
tab1, tab2, tab3, tab4 = st.tabs([
    ":material/sports_bar: Activos",
    ":material/assignment: Censos",
    ":material/store: Locales",
    ":material/description: Contratos"
])

with tab1:
    st.header("BI Activos")
    st.markdown("Cálculo de variaciones y estados de activos entre periodos.")
    render_model_ui(df_activos)

with tab2:
    st.header("BI Censos")
    st.markdown("Lógica de cumplimiento y cuotas basada en censos por periodo.")
    render_model_ui(df_censos)

with tab3:
    st.header("BI Locales")
    st.markdown("Información detallada de locales monitoreados.")
    render_model_ui(df_locales)

with tab4:
    st.header("BI Contratos")
    st.markdown("Información de contratos y activos comprometidos.")
    render_model_ui(df_contratos)
