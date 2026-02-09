import streamlit as st
from models.marts.gsheets.gsheets_tables import (
    locales, 
    censos, 
    bases_ccu, 
    contratos
)
from utilities.ui_icons import ICONS

st.title("Explorador de Datos")
st.markdown("Exploración rápida de los tablas en Google Sheets.")

def safe_render(df):
    """
    Renders the data info and dataframe, safely dropping 'row_index' if present.
    """
    if 'row_index' in df.columns:
        df = df.drop(columns=['row_index'])
    
    st.dataframe(df, use_container_width=True)


# Create tabs for organization
tab1, tab2, tab3, tab4 = st.tabs([
    f"{ICONS['locales']} Locales",
    f"{ICONS['censos']} Censos",
    f"{ICONS['bases_ccu']} Bases CCU",
    f"{ICONS['contratos']} Contratos"
])

with tab1:
    st.header("Locales")
    try:
        st.metric("Total Registros", f"{len(locales()):,}")
        safe_render(locales())
    except Exception as e:
        st.error(f"Error cargando locales: {e}")

with tab2:
    st.header("Censos")
    try:
        df_censos = censos()
        col1, col2, col3 = st.columns(3)
        col1.metric("Total", f"{len(df_censos):,}")
        col2.metric("2024-S2", f"{len(df_censos[df_censos['periodo'] == '2024-S2']):,}")
        col3.metric("2025-S2", f"{len(df_censos[df_censos['periodo'] == '2025-S2']):,}")

        safe_render(df_censos)
    except Exception as e:
        st.error(f"Error cargando censos: {e}")

with tab3:
    st.header("Bases CCU")
    try:
        df_bases_ccu = bases_ccu()
        col1, col2, col3 = st.columns(3)
        col1.metric("Total", f"{len(df_bases_ccu):,}")
        col2.metric("2024-Q1", f"{len(df_bases_ccu[df_bases_ccu['periodo'] == '2024-Q1']):,}")
        col3.metric("2026-Q1", f"{len(df_bases_ccu[df_bases_ccu['periodo'] == '2026-Q1']):,}")
        safe_render(df_bases_ccu)
    except Exception as e:
        st.error(f"Error cargando bases_ccu: {e}")

with tab4:
    st.header("Contratos")
    try:
        st.metric("Total Registros", f"{len(contratos()):,}")
        safe_render(contratos())
    except Exception as e:
        st.error(f"Error cargando contratos: {e}")
