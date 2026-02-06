import streamlit as st

from utilities.yaml_loader import get_table_config

def display_compliance_badge(clasificacion):
    """Displays a formatted st.badge based on the classification."""
    if clasificacion == "En regla":
        st.badge("En regla", icon="✅")
    elif clasificacion == "No en regla":
        st.badge("No en regla", icon="⚠️")
    elif clasificacion == "No aplica":
        st.badge("No aplica", icon="⚪")
    elif clasificacion == "Sin comodato o terminado":
        st.badge("Sin comodato o terminado", icon="🚫")
    else:
        st.badge(clasificacion, icon="🔍")

def render_model_ui(df, source_name=None, table_name=None):
    """
    Renders a standard UI component for a data model summary.
    Includes shape, columns, and the dataframe.
    Optionally fetches and displays description from YAML config.
    """
    if source_name and table_name:
        config = get_table_config(source_name=source_name, table_name=table_name)
        if config and config.get("description"):
            st.markdown(config.get("description"))

    st.markdown(f"Source: `{source_name}.{table_name}`")
    st.write(df.shape)
    st.code(df.columns.tolist())
    # Format dtypes as a single line: col1: type1 | col2: type2
    dtypes_str = " | ".join([f"{col}: {dtype}" for col, dtype in df.dtypes.items()])
    st.code(dtypes_str)
    st.dataframe(df)
