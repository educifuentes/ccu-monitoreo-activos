import streamlit as st
import altair as alt
import pandas as pd

from models.marts._fct_bases_ccu import fct_bases_ccu
from models.exposures._exp_asset_evolution_bases_ccu import exp_asset_evolution_bases_ccu
from models.exposures.metrics._metric_bases_ccu_kpis_by_period import metrics_bases_ccu_kpis_by_period
from helpers.ui_components.metrics_display import metrics_display

from helpers.ui_components.ui_config import CLASIFICACION_COLORS
from helpers.widgets.explorer_de_datos import explorer_de_datos



st.set_page_config(page_title="Bases CCU", layout="wide")

st.title("Bases CCU")
st.caption("Detalle de reportes de bases CCU")


# 1. Data Loading
try:
    df_bases_ccu = fct_bases_ccu()
    df_asset_evolution_bases = exp_asset_evolution_bases_ccu()
except Exception as e:
    st.error(f"Error cargando los datos de Bases CCU: {e}")
    st.stop()

if df_bases_ccu.empty:
    st.warning("No hay datos de Bases CCU disponibles.")
    st.stop()

# 2. Filtering
st.divider()

# Get unique, non-null periods and sort them descending
unique_periodos = sorted(df_bases_ccu["periodo"].dropna().unique(), reverse=True)
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
df_metrics = metrics_bases_ccu_kpis_by_period()
if selected_periodo != "Todos":
    df_metrics = df_metrics[df_metrics["periodo"] == selected_periodo]

kpi_cols = ["periodo", "# Clientes", "# Clientes Local Imagen", "# Clientes Nuevos"]

metrics_display(df_metrics[kpi_cols])


st.subheader("Detalle por Cliente")

unique_clientes = sorted(df_bases_ccu["cliente_id"].dropna().unique())

cliente_seleccionado = st.selectbox(
    "Seleccione un cliente",
    options=unique_clientes,
)

if cliente_seleccionado:
    st.subheader(f"Cliente: {cliente_seleccionado}")
    
    # Basic client info from latest period
    client_info = df_bases_ccu[df_bases_ccu["cliente_id"] == cliente_seleccionado].sort_values("fecha", ascending=False).iloc[0]
    
    col1, col2, col3 = st.columns(3)
    col1.markdown(f"**Razon Social:** {client_info['razon_social']}")
    col2.markdown(f"**Nombre Fantasia:** {client_info['nombre_fantasia']}")
    col3.markdown(f"**RUT:** {client_info['rut']}")
    
    st.divider()
    
    ccu_columns_client = ["periodo", "fecha", "schoperas_ccu", "salidas", "coolers", "es_local_imagen"]

    df_filter_by_client = df_bases_ccu[df_bases_ccu["cliente_id"] == cliente_seleccionado]
    st.dataframe(df_filter_by_client[ccu_columns_client], hide_index=True, use_container_width=True)

    st.subheader("Evolucion de Activos")
    asset_evolution_columns_client = [
        "periodo", 
        "schoperas_ccu", "schoperas_ccu_diff", 
        "salidas", "salidas_diff", 
        "coolers", "coolers_diff"
    ]
    df_asset_evolution_client = df_asset_evolution_bases[df_asset_evolution_bases["cliente_id"] == cliente_seleccionado]
    st.dataframe(df_asset_evolution_client[asset_evolution_columns_client], hide_index=True, use_container_width=True)