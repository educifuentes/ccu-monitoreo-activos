import streamlit as st

from models.marts.gsheets._dim_clientes_gsheets import dim_clientes_gsheets
from models.marts.gsheets._fct_censos_gsheets import fct_censos_gsheets
from models.marts.gsheets._fct_bases_ccu_gsheets import fct_bases_ccu_gsheets

from helpers.ui_components.ui_icons import ICONS
from helpers.widgets.explorer_de_datos import explorer_de_datos


st.set_page_config(page_title="Explorador de Tablas", layout="wide")

st.title("Explorador de Tablas")
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
    f"{ICONS['bases_ccu']} Bases CCU",
])

with tab1:
    st.header("Clientes")
    try:
        # Use dim_clientes_gsheets instead of dim_clientes
        df_locales = dim_clientes_gsheets()
        df_locales = explorer_de_datos(df_locales, key_prefix="clientes")
            
        st.metric("Total", f"{len(df_locales):,}")
        safe_render(df_locales)
    except Exception as e:
        st.error(f"Error cargando clientes: {e}")

with tab2:
    st.header("Censos")
    try:
        # Use fct_censos_gsheets instead of fct_censos
        df_censos = fct_censos_gsheets()
        df_censos = explorer_de_datos(df_censos, key_prefix="censos")
        
        # Summary by period
        if 'periodo' in df_censos.columns:
            st.caption("Resumen por Periodo:")
            st.dataframe(df_censos.groupby('periodo').size().reset_index(name='Registros'), hide_index=True)
        
        safe_render(df_censos)
    except Exception as e:
        st.error(f"Error cargando censos: {e}")

with tab3:
    st.header("Bases CCU")
    try:
        # Use fct_bases_ccu_gsheets instead of fct_bases_ccu
        df_bases_ccu = fct_bases_ccu_gsheets()
        df_bases_ccu = explorer_de_datos(df_bases_ccu, key_prefix="bases_ccu")
        
        # Summary by period
        if 'periodo' in df_bases_ccu.columns:
            st.caption("Resumen por Periodo:")
            st.dataframe(df_bases_ccu.groupby('periodo').size().reset_index(name='Registros'), hide_index=True)

        safe_render(df_bases_ccu)
    except Exception as e:
        st.error(f"Error cargando bases_ccu: {e}")