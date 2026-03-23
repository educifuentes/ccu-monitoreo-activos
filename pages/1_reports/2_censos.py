import streamlit as st
import altair as alt
import pandas as pd

from models.marts.censos.exposures._exp_censos import exp_censos

from utilities.ui_config import CLASIFICACION_COLORS
from utilities.widgets.explorer_de_datos import explorer_de_datos
from utilities.widgets.display_df_censos import display_df_censos



st.set_page_config(page_title="Censos", layout="wide")

st.title("Censos")


# 1. Data Loading
try:
    df_censos = exp_censos()
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

with col_filt2:
    counts_df = df_censos["periodo"].value_counts().reset_index()
    counts_df.columns = ["periodo", "count"]
    counts_df = counts_df.sort_values(by="periodo", ascending=False).reset_index(drop=True)
    counts_df.loc[len(counts_df)] = ["Total", counts_df["count"].sum()]
    st.dataframe(counts_df, hide_index=True, width=400)

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
    st.subheader(f"por Región - {selected_periodo}")
    if "region" in df_filtered.columns:
        counts_df = df_filtered["region"].value_counts().reset_index()
        counts_df.columns = ["Región", "Cantidad"]
        counts_df = counts_df.sort_values(
            by="Región", 
            ascending=True,
            key=lambda x: pd.to_numeric(x.str.extract(r'^(\d+)', expand=False), errors="coerce")
        )
        st.dataframe(counts_df, hide_index=True, width='stretch', height=500)
    else:
        st.info("La columna 'region' no está disponible en los datos.")

with col_chart:
    st.subheader("Cumplimiento")
    # filter out rows with fecha before 2025
    df_filtered_no_2024_s2 = df_censos[pd.to_datetime(df_censos["fecha"], errors='coerce').dt.year >= 2025]
    if "clasificacion" in df_filtered_no_2024_s2.columns and "periodo" in df_filtered_no_2024_s2.columns:
        chart = alt.Chart(df_filtered_no_2024_s2).mark_bar().encode(
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

st.subheader("Detalles")

censo_columns = ["periodo", "local_id", "razon_social", "marcas",  "instalo", "disponibilizo", "salidas", "clasificacion"]

censo_df_display = df_filtered[censo_columns]

explorer_de_datos(censo_df_display)

display_df_censos(censo_df_display)