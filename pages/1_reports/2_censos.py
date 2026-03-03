import streamlit as st
import altair as alt
import pandas as pd

from models.gsheets.marts.bi_censos import bi_censos
from utilities.ui_config import CLASIFICACION_COLORS


st.set_page_config(page_title="Censos", layout="wide")

st.title("Reporte de Censos")
st.markdown("Tabla de resumen por región y gráfico de cumplimiento según los datos de censos.")

# 1. Data Loading
try:
    df_censos = bi_censos()
except Exception as e:
    st.error(f"Error cargando los datos de censos: {e}")
    st.stop()

if df_censos.empty:
    st.warning("No hay datos de censos disponibles.")
    st.stop()

# 2. Filtering
st.divider()

# Get unique, non-null periods and sort them descending
unique_periodos = sorted(df_censos["periodo"].dropna().unique(), reverse=True)
periodos_opciones = ["Todos"] + unique_periodos

col_filt1, col_filt2 = st.columns(2)

with col_filt1:
    # Default to the most recent period if available
    selected_periodo = st.selectbox(
        "Filtrar por Periodo",
        options=periodos_opciones,
        index=1 if len(unique_periodos) > 0 else 0
    )

if selected_periodo != "Todos":
    df_filtered = df_censos[df_censos["periodo"] == selected_periodo]
else:
    df_filtered = df_censos.copy()

if df_filtered.empty:
    st.warning("No hay datos para el o los periodos seleccionados.")
    st.stop()

# 3. Layout: Table & Chart
st.divider()
col_table, col_chart = st.columns([1, 1.5])

with col_table:
    st.subheader(f"Resumen por Región - {selected_periodo}")
    if "region" in df_filtered.columns:
        counts_df = df_filtered["region"].value_counts().reset_index()
        counts_df.columns = ["Región", "Cantidad"]
        counts_df = counts_df.sort_values(by="Cantidad", ascending=False).reset_index(drop=True)
        counts_df.loc[len(counts_df)] = ["Total", counts_df["Cantidad"].sum()]
        st.dataframe(counts_df, hide_index=True, use_container_width=True)
    else:
        st.info("La columna 'region' no está disponible en los datos.")

with col_chart:
    st.subheader("Cumplimiento - Censos")
    if "clasificacion" in df_filtered.columns and "periodo" in df_filtered.columns:
        chart = alt.Chart(df_filtered).mark_bar().encode(
            x=alt.X('periodo:O', title='Periodo'),
            y=alt.Y('count():Q', title='Número de Locales'),
            color=alt.Color(
                'clasificacion:N',
                title='Clasificación',
                scale=alt.Scale(
                    domain=list(CLASIFICACION_COLORS.keys()),
                    range=list(CLASIFICACION_COLORS.values())
                )
            ),
            tooltip=[
                alt.Tooltip('periodo:O', title='Periodo'),
                alt.Tooltip('count():Q', title='Número de Locales'),
                alt.Tooltip('clasificacion:N', title='Clasificación')
            ]
        )
        st.altair_chart(chart, width='stretch', height=250)
    else:
        st.info("Las columnas 'clasificacion' o 'periodo' no están disponibles en los datos de censos.")
