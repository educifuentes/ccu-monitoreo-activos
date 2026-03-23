import streamlit as st

# replace later with gsheets tables
from models.gsheets.exposures._exp_censos import exp_censos
from models.gsheets.exposures._exp_activos import exp_activos
from models.gsheets.exposures._exp_locales import exp_locales
from models.gsheets.exposures._exp_contratos import exp_contratos

from utilities.ui_components import render_model_ui

# Page settings and header
st.title("BI Tables")
st.markdown("Tablas procesadas con lógica de negocio específica para visualización en Dashboards.")

# --- Load Data (Top Level) ---
df_activos = exp_activos()
df_censos = exp_censos()
df_locales = exp_locales()
df_contratos = exp_contratos()

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

    # Find local_ids that have at least 3 rows
    st.markdown("Locales con al menos 3 filas")
    local_ids_with_min_rows = (
        df_activos.groupby('local_id')
        .size()
        .loc[lambda x: x >= 3]
        .index.tolist()
    )
    
    filtered_df = df_activos[df_activos['local_id'].isin(local_ids_with_min_rows)].sort_values('local_id')
    st.dataframe(filtered_df, width='stretch')

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
