import streamlit as st
from models.gsheets.staging.gsheets_tables import (
    clientes, 
    censos, 
    bases_ccu, 
    contratos
)
from utilities.ui_icons import ICONS
from utilities.widgets.explorer_de_datos import explorer_de_datos


st.set_page_config(page_title="Explorador de Datos", layout="wide")

st.title("Explorador de Datos")
st.markdown("Exploración rápida de los tablas en Google Sheets.")

def safe_render(df):
    """
    Renders the data info and dataframe, safely dropping 'row_index' if present.
    """
    if 'row_index' in df.columns:
        df = df.drop(columns=['row_index'])
    
    st.dataframe(df, width='stretch')

# Create tabs for organization
tab1, tab2, tab3, tab4 = st.tabs([
    f"{ICONS['clientes']} Clientes",
    f"{ICONS['censos']} Censos",
    f"{ICONS['bases_ccu']} Bases CCU",
    f"{ICONS['contratos']} Contratos"
])

with tab1:
    st.header("Clientes")
    try:
        df_locales = clientes()
        df_locales = explorer_de_datos(df_locales, key_prefix="clientes")
            
        st.metric("Total Registros", f"{len(df_locales):,}")
        safe_render(df_locales)
    except Exception as e:
        st.error(f"Error cargando clientes: {e}")

with tab2:
    st.header("Censos")
    try:
        df_censos = censos()
        df_censos = explorer_de_datos(df_censos, key_prefix="censos")
        
        safe_render(df_censos)
    except Exception as e:
        st.error(f"Error cargando censos: {e}")

with tab3:
    st.header("Bases CCU")
    try:
        df_bases_ccu = bases_ccu()
        df_bases_ccu = explorer_de_datos(df_bases_ccu, key_prefix="bases_ccu")
        
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
        df_contratos = contratos()
        df_contratos = explorer_de_datos(df_contratos, key_prefix="contratos")
        
        st.metric("Total Registros", f"{len(df_contratos):,}")
        safe_render(df_contratos)
    except Exception as e:
        st.error(f"Error cargando contratos: {e}")
