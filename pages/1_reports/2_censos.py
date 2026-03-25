import streamlit as st
import altair as alt
import pandas as pd

from models.exposures._exp_censos import exp_censos
from models.exposures._exp_asset_evolution_censos import exp_asset_evolution_censos
from models.exposures.metrics._metric_censo_kpis_by_period import metrics_censo_kpis_by_period

from helpers.ui_components.ui_config import CLASIFICACION_COLORS
from helpers.widgets.explorer_de_datos import explorer_de_datos
from helpers.widgets.display_df_censos import display_df_censos



st.set_page_config(page_title="Censos", layout="wide")

st.title("Censos")
st.caption("Detalle de encuestas de censos")


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

    # Default to the most recent period if available
selected_periodo = st.selectbox(
    "Filtrar por Periodo",
    options=periodos_opciones,
    index=1 if len(unique_periodos) > 0 else 0
)


# 3. Layout: Table & Chart
st.subheader("General")

# Metrics
df_metrics = metrics_censo_kpis_by_period()
st.dataframe(df_metrics, hide_index=True, use_container_width=True)
#metrics

# st.subheader("Cumplimiento")
# # filter out rows with fecha before 2025
# df_filtered_no_2024_s2 = df_censos[pd.to_datetime(df_censos["fecha"], errors='coerce').dt.year >= 2025]
# if "clasificacion" in df_filtered_no_2024_s2.columns and "periodo" in df_filtered_no_2024_s2.columns:
#     chart = alt.Chart(df_filtered_no_2024_s2).mark_bar().encode(
#         x=alt.X('periodo:O', title='Periodo'),
#         y=alt.Y('count():Q', title='Número de Clientes'),
#         color=alt.Color(
#             'clasificacion:N',
#             title='Clasificación',
#             scale=alt.Scale(
#                 domain=list(CLASIFICACION_COLORS.keys()),
#                 range=list(CLASIFICACION_COLORS.values())
#             )
#         ),
#         tooltip=[
#             alt.Tooltip('periodo:O', title='Periodo'),
#             alt.Tooltip('count():Q', title='Número de Clientes'),
#             alt.Tooltip('clasificacion:N', title='Clasificación')
#         ]
#     )
#     st.altair_chart(chart, width='stretch', height=250)
# else:
#     st.info("Las columnas 'clasificacion' o 'periodo' no están disponibles en los datos de censos.")


st.subheader("Detalle por Cliente")

unique_clientes = sorted(df_censos["cliente_id"].dropna().unique())

cliente_seleccionado = st.selectbox(
    "Seleccione un cliente",
    options=unique_clientes,
)

if cliente_seleccionado:
    st.subheader(f"Cliente: {cliente_seleccionado}")
    censo_columns_client = ["periodo", "schoperas_total", "schoperas_ccu", "salidas", "clasificacion"]

    df_filter_by_client = df_censos[df_censos["cliente_id"] == cliente_seleccionado]
    st.dataframe(df_filter_by_client[censo_columns_client], hide_index=True, use_container_width=True)

    st.subheader("Evolucion de Activos")
    asset_evolution_columns_client = ["periodo", "schoperas_total", "schoperas_total_diff", "schoperas_ccu", "schoperas_ccu_diff", "salidas", "salidas_diff"]
    df_asset_evolution_censos_client = df_asset_evolution_censos[df_asset_evolution_censos["cliente_id"] == cliente_seleccionado]
    st.dataframe(df_asset_evolution_censos_client, hide_index=True, use_container_width=True)