import streamlit as st
import altair as alt
import pandas as pd

from models.exposures._exp_bases_ccu import exp_bases_ccu
from models.exposures._exp_asset_evolution_bases_ccu import exp_asset_evolution_bases_ccu
from models.metrics._metric_bases_ccu_kpis_by_period import metrics_bases_ccu_kpis_by_period

from helpers.ui_components.metrics_display import metrics_display
from helpers.ui_components.ui_config import CLASIFICACION_COLORS
from helpers.widgets.explorer_de_datos import explorer_de_datos



st.set_page_config(page_title="Bases CCU", layout="wide")
st.title("📦 Reporte de Bases CCU")
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

# 2. Global Filter
unique_periodos = sorted(df_bases_ccu["periodo"].dropna().unique(), reverse=True)
col_f1, col_f2 = st.columns([1, 2])
with col_f1:
    selected_periodo = st.selectbox(
        "Periodo",
        options=["Todos"] + unique_periodos,
        index=1 if len(unique_periodos) > 0 else 0
    )

st.divider()

# 3. Content Tabs
tab_gen, tab_det = st.tabs(["📊 Resumen General", "🔍 Detalle por Cliente"])

with tab_gen:
    df_m = df_metrics.copy()
    if selected_periodo != "Todos":
        df_m = df_m[df_m["periodo"] == selected_periodo]
    
    if not df_m.empty:
        kpi_cols = ["periodo", "N Clientes", "N Clientes Local Imagen", "N Clientes Nuevos"]
        st.subheader("Indicadores de Cobertura")
        metrics_display(df_m[kpi_cols])
    else:
        st.info("No hay métricas para el periodo seleccionado.")

with tab_det:
    unique_clientes = sorted(df_bases_ccu["cliente_id"].dropna().unique())
    cliente_seleccionado = st.selectbox(
        "Seleccione un cliente para ver su detalle",
        options=unique_clientes,
    )

    if cliente_seleccionado:
        st.subheader(f"Ficha Cliente: {cliente_seleccionado}")
        
        # Latest info
        client_latest = df_bases_ccu[df_bases_ccu["cliente_id"] == cliente_seleccionado].sort_values("fecha", ascending=False).iloc[0]
        
        c1, c2, c3 = st.columns(3)
        with st.container(border=True):
            st.markdown(f"**Razón Social:** {client_latest['razon_social']}")
            st.markdown(f"**Nombre Fantasía:** {client_latest['nombre_fantasia']}")
            st.markdown(f"**RUT:** {client_latest['rut']}")
        
        st.divider()
        
        st.subheader("Historial de Activos (Base CCU)")
        ccu_cols = ["periodo", "fecha", "schoperas_ccu", "salidas", "coolers", "es_local_imagen"]
        df_c = df_bases_ccu[df_bases_ccu["cliente_id"] == cliente_seleccionado]
        st.dataframe(df_c[ccu_cols], hide_index=True, use_container_width=True)

        st.subheader("Evolución de Activos")
        asset_cols = ["periodo", "schoperas_ccu", "schoperas_ccu_diff", "salidas", "salidas_diff", "coolers", "coolers_diff"]
        df_e = df_asset_evolution_bases[df_asset_evolution_bases["cliente_id"] == cliente_seleccionado]
        st.dataframe(df_e[asset_cols], hide_index=True, use_container_width=True)