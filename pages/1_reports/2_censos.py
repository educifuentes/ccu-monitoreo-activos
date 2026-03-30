import streamlit as st
import altair as alt
import pandas as pd

from models.exposures._exp_censos import exp_censos
from models.exposures._exp_asset_evolution_censos import exp_asset_evolution_censos
from models.metrics._metric_censo_kpis_by_period import metrics_censo_kpis_by_period

from helpers.ui_components.ui_config import CLASIFICACION_COLORS
from helpers.widgets.explorer_de_datos import explorer_de_datos
from helpers.widgets.display_df_censos import display_df_censos
from helpers.ui_components.metrics_display import metrics_display
from helpers.ui_components.icons import render_icon


st.set_page_config(page_title="Censos", layout="wide")
st.title(f"{render_icon('censos')} Censos")
st.caption("Seguimiento detallado de las encuestas en terreno.")

# 1. Data Loading
try:
    df_censos = exp_censos()
    df_asset_evolution_censos = exp_asset_evolution_censos()
    df_metrics = metrics_censo_kpis_by_period()
except Exception as e:
    st.error(f"Error cargando los datos de censos: {e}")
    st.stop()

if df_censos.empty:
    st.warning("No hay datos de censos disponibles.")
    st.stop()

# 2. Global Filter & Summary
unique_periodos = sorted(df_metrics["periodo"].dropna().unique().tolist())
col_f1, col_f2 = st.columns([1, 2])
with col_f1:
    selected_periodo = st.selectbox(
        "Periodo",
        options=["Todos"] + unique_periodos,
        index=0,
        key="filter_censos_page"
    )

df_m = df_metrics.copy()
if selected_periodo != "Todos":
    df_m = df_m[df_m["periodo"] == selected_periodo]

with col_f2:
    if not df_m.empty:
        kpi_generales = ["periodo", "N Clientes", "N Permite censos"]
        metrics_display(df_m[kpi_generales], show_header=False, show_divider=False, max_cols=3)

st.divider()

# --- Details Section ---
st.header("Detalle por Cliente")
unique_clientes = sorted(df_censos["cliente_id"].dropna().unique())
cliente_seleccionado = st.selectbox(
    "Seleccione un cliente para ver su historial",
    options=unique_clientes,
)

if cliente_seleccionado:
    st.subheader(f"Cliente ID: {cliente_seleccionado}")
    
    # Latest Info
    latest_info = df_censos[df_censos["cliente_id"] == cliente_seleccionado].sort_values("fecha", ascending=False).iloc[0]
    c1, c2, c3 = st.columns(3)
    
    clasif = latest_info.get("clasificacion")
    c1.metric("Clasificación Actual", str(clasif) if pd.notna(clasif) else "N/A")
    
    stotal = latest_info.get("schoperas_total")
    c2.metric("Total Schoperas", int(stotal) if pd.notna(stotal) else 0)
    
    salccu = latest_info.get("salidas")
    c3.metric("Salidas CCU", int(salccu) if pd.notna(salccu) else 0)
    
    st.divider()
    
    st.subheader("Historial de Censos")
    censo_cols = ["periodo", "fecha", "schoperas_total", "schoperas_ccu", "salidas", "marcas"]
    df_c = df_censos[df_censos["cliente_id"] == cliente_seleccionado]
    st.dataframe(df_c[censo_cols], hide_index=True, use_container_width=True)