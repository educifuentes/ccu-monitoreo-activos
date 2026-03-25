import streamlit as st
import altair as alt
import pandas as pd

from models.exposures._exp_censos import exp_censos
from models.exposures._exp_asset_evolution_censos import exp_asset_evolution_censos

from helpers.ui_components.ui_config import CLASIFICACION_COLORS
from helpers.widgets.explorer_de_datos import explorer_de_datos
from helpers.widgets.display_df_censos import display_df_censos



st.set_page_config(page_title="Evolucion de Activos", layout="wide")

st.title("Evolucion de Activos")
st.caption("data de censos y reportes comodatos trimestrales de CCU")


# 1. Data Loading
try:
    df_censos = exp_censos()
    df_asset_evolution_censos = exp_asset_evolution_censos()
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
st.subheader("Resumen")

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
            y=alt.Y('count():Q', title='Número de Clientes'),
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
                alt.Tooltip('count():Q', title='Número de Clientes'),
                alt.Tooltip('clasificacion:N', title='Clasificación')
            ]
        )
        st.altair_chart(chart, width='stretch', height=250)
    else:
        st.info("Las columnas 'clasificacion' o 'periodo' no están disponibles en los datos de censos.")


st.subheader("Detalle por Cliente")

unique_clientes = (
    df_censos[["cliente_id", "razon_social"]]
    .drop_duplicates()
    .sort_values("cliente_id")
)
clientes_options = {
    row["cliente_id"]: f"{row['cliente_id']} - {row['razon_social']}"
    for _, row in unique_clientes.iterrows()
}

cliente_seleccionado = st.selectbox(
    "Seleccione un cliente",
    options=list(clientes_options.keys()),
    format_func=lambda x: clientes_options[x],
)

if cliente_seleccionado:
    st.subheader(clientes_options[cliente_seleccionado])
    censo_columns_client = ["periodo", "schoperas_total", "schoperas_ccu", "salidas", "clasificacion"]

    df_filter_by_client = df_censos[df_censos["cliente_id"] == cliente_seleccionado]
    st.dataframe(df_filter_by_client[censo_columns_client], hide_index=True, use_container_width=True)

    st.subheader("Evolucion de Activos")
    asset_evolution_columns_client = ["periodo", "schoperas_total", "schoperas_total_diff", "schoperas_ccu", "schoperas_ccu_diff", "salidas", "salidas_diff"]
    df_asset_evolution_censos_client = df_asset_evolution_censos[df_asset_evolution_censos["cliente_id"] == cliente_seleccionado]
    st.dataframe(df_asset_evolution_censos_client, hide_index=True, use_container_width=True)