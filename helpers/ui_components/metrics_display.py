import streamlit as st

def metrics_display(df):
    """
    Renders metrics from a DataFrame using st.metric in a columnar layout.
    
    Args:
        df (pd.DataFrame): DataFrame containing columns for metrics and 'periodo'.
    """
    if df.empty:
        st.info("No hay métricas para mostrar.")
        return

    # Ensure 'periodo' is present
    if 'periodo' not in df.columns:
        st.warning("El DataFrame de métricas debe contener una columna 'periodo'.")
        return

    # Filter out columns that shouldn't be metrics (like 'periodo')
    metric_cols = [col for col in df.columns if col != 'periodo']
    MAX_COLS = 6

    for _, row in df.iterrows():
        # Period Header
        st.markdown(f"#### Periodo: {row['periodo']}")
        
        # Chunk metrics into groups of MAX_COLS
        for i in range(0, len(metric_cols), MAX_COLS):
            chunk = metric_cols[i : i + MAX_COLS]
            cols = st.columns(len(chunk))
            for j, col_name in enumerate(chunk):
                val = row[col_name]
                cols[j].metric(label=col_name, value=val)
        
        st.divider()
