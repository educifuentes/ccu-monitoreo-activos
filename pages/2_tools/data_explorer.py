import streamlit as st
from models.marts.gsheets.gsheets_tables import (
    locales, 
    censos, 
    bases_ccu, 
    contratos
)

st.title("Explorador de Datos")
st.markdown("Exploración rápida de los DataFrames maestros alojados en Google Sheets.")

def render_data_info(df):
    """Renders a human-readable info panel for the dataframe."""
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Registros", f"{len(df):,}")
    with col2:
        st.metric("Columnas", len(df.columns))


# Create tabs for organization
tab1, tab2, tab3, tab4 = st.tabs([
    ":material/sports_bar: Locales",
    ":material/checklist_rtl: Censos",
    ":material/assignment: Bases CCU",
    ":material/contract: Contratos"
])

with tab1:
    st.header("Locales")
    try:
        df_locales = locales()
        render_data_info(df_locales)
        st.dataframe(df_locales, use_container_width=True)
    except Exception as e:
        st.error(f"Error cargando locales: {e}")

with tab2:
    st.header("Censos")
    try:
        df_censos = censos()
        render_data_info(df_censos)
        st.dataframe(df_censos, use_container_width=True)
    except Exception as e:
        st.error(f"Error cargando censos: {e}")

with tab3:
    st.header("Bases CCU")
    try:
        df_bases = bases_ccu()
        render_data_info(df_bases)
        st.dataframe(df_bases, use_container_width=True)
    except Exception as e:
        st.error(f"Error cargando bases_ccu: {e}")

with tab4:
    st.header("Contratos")
    try:
        df_contratos = contratos()
        render_data_info(df_contratos)
        st.dataframe(df_contratos, use_container_width=True)
    except Exception as e:
        st.error(f"Error cargando contratos: {e}")
