import streamlit as st

from utilities.transformations.gsheet_links import add_gsheet_link
from utilities.ui_icons import ICONS

def display_compliance_badge(clasificacion):
    """Displays a formatted st.badge based on the classification."""
    if clasificacion == "En regla":
        st.badge("En regla", icon=ICONS['check'], color="green")
    elif clasificacion == "No en regla":
        st.badge("No en regla", icon=ICONS['warning'], color="red")
    elif clasificacion == "No aplica":
        st.badge("No aplica", icon=ICONS['not_apply'], color="yellow")
    elif clasificacion == "Sin comodato o terminado":
        st.badge("Sin comodato o terminado", icon=ICONS['close'], color="blue")
    else:
        st.badge(clasificacion, icon="🔍")

def render_model_ui(df, source_name=None, table_name=None):
    """
    Renders a standard UI component for a data model summary.
    Includes shape, columns, and the dataframe.
    Optionally fetches and displays description from YAML config.
    """
    # if source_name and table_name:
    #     config = get_table_config(source_name=source_name, table_name=table_name)
    #     if config and config.get("description"):
    #         st.markdown(config.get("description"))

    # st.markdown(f"Source: `{source_name}.{table_name}`")
    st.write(df.shape)
    st.code(df.columns.tolist())
    # Format dtypes as a single line: col1: type1 | col2: type2
    dtypes_str = " | ".join([f"{col}: {dtype}" for col, dtype in df.dtypes.items()])
    st.code(dtypes_str)
    st.dataframe(df)
    st.divider()

def render_troubled_rows(df, gid, row_indices=None):
    """
    Renders a dataframe of troubled rows with a configured Google Sheet link.
    
    Args:
        df (pd.DataFrame): The dataframe containing the rows to display.
        gid (str): The Google Sheet Grid ID.
        row_indices (pd.Series or list, optional): The original row indices for linking. 
                                                   If None, tries to use df['row_index'].
    """
    if row_indices is None:
        if 'row_index' in df.columns:
            row_indices = df['row_index']
    
    # We pass None for row_indices if we can't find them, add_gsheet_link handles it (or we should ensure it does)
    # Looking at add_gsheet_link usage, it expects row_indices. 
    # If df has row_index, we use it. 
    
    df_with_links = add_gsheet_link(df, gid, row_indices)
    
    st.dataframe(
        df_with_links, 
        use_container_width=True,
        column_config={"link": st.column_config.LinkColumn("link", display_text="Ir a Gsheet")}
    )
