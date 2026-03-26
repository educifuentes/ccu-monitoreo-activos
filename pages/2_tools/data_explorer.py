import streamlit as st

from models.marts._dim_clientes import dim_clientes
from models.marts._fct_censos import fct_censos
from models.marts._fct_bases_ccu import fct_bases_ccu

from helpers.ui_components.ui_icons import ICONS
from helpers.widgets.explorer_de_datos import explorer_de_datos


st.set_page_config(page_title="Explorador de Datos", layout="wide")

st.title("Explorador de Datos")
st.markdown("Exploración rápida de los tablas en  [Google Sheets](https://docs.google.com/spreadsheets/d/11JgW2Z9cFrHvNFw21-zlvylTHHo5tvizJeA9oxHcDHU/edit?gid=2068995815#gid=2068995815)")

def safe_render(df):
    """
    Renders the data info and dataframe, safely dropping 'row_index' if present.
    """
    if 'row_index' in df.columns:
        df = df.drop(columns=['row_index'])
    
    st.dataframe(df, width='stretch')

# Create tabs for organization
tab1, tab2, tab3 = st.tabs([
    f"{ICONS['clientes']} Clientes",
    f"{ICONS['censos']} Censos",
    f"{ICONS['bases_ccu']} Reportes CCU",
])

with tab1:
    st.header("Clientes")
    try:
        # Use dim_clientes instead of clientes
        df_locales = dim_clientes()
        df_locales = explorer_de_datos(df_locales, key_prefix="clientes")
            
        st.metric("Total Registros", f"{len(df_locales):,}")
        safe_render(df_locales)
    except Exception as e:
        st.error(f"Error cargando clientes: {e}")

with tab2:
    st.header("Censos")
    try:
        # Use fct_censos instead of censos
        df_censos = fct_censos()
        df_censos = explorer_de_datos(df_censos, key_prefix="censos")
        
        safe_render(df_censos)
    except Exception as e:
        st.error(f"Error cargando censos: {e}")

with tab3:
    st.header("Bases CCU")
    try:
        # Use fct_bases_ccu instead of bases_ccu
        df_bases_ccu = fct_bases_ccu()
        df_bases_ccu = explorer_de_datos(df_bases_ccu, key_prefix="bases_ccu")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total", f"{len(df_bases_ccu):,}")
        
        # Check if 'periodo' exists before filtering
        if 'periodo' in df_bases_ccu.columns:
            col2.metric("2024-Q1", f"{len(df_bases_ccu[df_bases_ccu['periodo'] == '2024-Q1']):,}")
            col3.metric("2026-Q1", f"{len(df_bases_ccu[df_bases_ccu['periodo'] == '2026-Q1']):,}")
        
        safe_render(df_bases_ccu)
    except Exception as e:
        st.error(f"Error cargando bases_ccu: {e}")