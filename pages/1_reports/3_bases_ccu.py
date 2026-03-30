import streamlit as st
import altair as alt
import pandas as pd

from models.exposures._exp_bases_ccu import exp_bases_ccu
from models.exposures._exp_asset_evolution_bases_ccu import exp_asset_evolution_bases_ccu
from models.metrics._metric_bases_ccu_kpis_by_period import metrics_bases_ccu_kpis_by_period

from helpers.ui_components.metrics_display import metrics_display
from helpers.ui_components.ui_config import CLASIFICACION_COLORS
from helpers.widgets.explorer_de_datos import explorer_de_datos
from helpers.ui_components.icons import render_icon


st.set_page_config(page_title="Bases CCU", layout="wide")
st.title(f"{render_icon('bases_ccu')} Reporte de Bases CCU")
st.caption("Detalle de activos y cumplimiento según la base oficial.")

# 1. Data Loading
try:
    df_bases_ccu = exp_bases_ccu()
    df_asset_evolution_bases = exp_asset_evolution_bases_ccu()
    df_metrics = metrics_bases_ccu_kpis_by_period()
except Exception as e:
    st.error(f"Error cargando los datos de Bases CCU: {e}")
    st.stop()

if df_bases_ccu.empty:
    st.warning("No hay datos de Bases CCU disponibles.")
    st.stop()

# 2. Global Filter & Summary
unique_periodos = sorted(df_metrics["periodo"].dropna().unique().tolist())
col_f1, col_f2 = st.columns([1, 2])
with col_f1:
    selected_periodo = st.selectbox(
        "Periodo",
        options=["Todos"] + unique_periodos,
        index=0,
        key="filter_bases_page"
    )

df_m = df_metrics.copy()
if selected_periodo != "Todos":
    df_m = df_m[df_m["periodo"] == selected_periodo]

with col_f2:
    if not df_m.empty:
        kpi_cols = ["periodo", "N Clientes", "N Clientes Local Imagen"]
        metrics_display(df_m[kpi_cols], show_header=False, show_divider=False, max_cols=3)

st.divider()

# 3. Details Section
st.header("Detalle por Cliente")
unique_clientes = sorted(df_bases_ccu["cliente_id"].dropna().unique())
cliente_seleccionado = st.selectbox(
    "Seleccione un cliente para ver su detalle",
    options=unique_clientes,
)

if cliente_seleccionado:    
    # Latest info
    client_latest = df_bases_ccu[df_bases_ccu["cliente_id"] == cliente_seleccionado].sort_values("fecha", ascending=False).iloc[0]
    
    c1, c2, c3 = st.columns(3)
    
    st.subheader("Historial de Activos (Base CCU)")
    ccu_cols = ["periodo", "fecha", "schoperas_ccu", "salidas", "coolers", "es_local_imagen"]
    df_c = df_bases_ccu[df_bases_ccu["cliente_id"] == cliente_seleccionado]
    st.dataframe(df_c[ccu_cols], hide_index=True, use_container_width=True)