import pandas as pd
import streamlit as st

from models.exposures._exp_clientes import exp_clientes
from models.exposures._exp_censos import exp_censos

from models.exposures._exp_censos import exp_censos
from models.exposures._exp_asset_evolution_censos import exp_asset_evolution_censos
from models.metrics._metric_censo_kpis_by_period import metrics_censo_kpis_by_period
from models.metrics._metric_bases_ccu_kpis_by_period import metrics_bases_ccu_kpis_by_period
from helpers.ui_components.metrics_display import metrics_display

from helpers.ui_components.ui_config import CLASIFICACION_COLORS
from helpers.widgets.explorer_de_datos import explorer_de_datos
from helpers.widgets.display_df_censos import display_df_censos


# marts
from models.metrics.general_metrics import calculate_general_metrics, get_latest_classification

# helpers
from helpers.ui_components.ui_components import display_compliance_badge
from helpers.ui_components.ui_config import CLASIFICACION_COLORS, MARCAS_COLORS
from helpers.transformations.date_formatting import format_date_spanish


from helpers.ui_components.icons import render_icon


st.set_page_config(page_title="Monitoreo de Activos CCU", layout="wide")
st.title(f"{render_icon('dashboard')} Monitoreo de Activos CCU")
st.markdown("Dashboard de información de activos de CCU para el Cumplimiento de Ley de Competencia de la FNE")
st.markdown("""
    Fuente de Datos: [Google Sheets](https://docs.google.com/spreadsheets/d/11JgW2Z9cFrHvNFw21-zlvylTHHo5tvizJeA9oxHcDHU/edit?gid=2068995815#gid=2068995815)
""")    
st.markdown(" ")

# 1. Data Loading
try:
    df_censos = exp_censos()
    df_metrics_censos = metrics_censo_kpis_by_period()
    df_metrics_bases = metrics_bases_ccu_kpis_by_period()
except Exception as e:
    st.error(f"Error cargando los datos: {e}")
    st.stop()

# 2. Censos Section
unique_periodos_censos = sorted(df_metrics_censos["periodo"].dropna().unique(), reverse=True)

# Header Row
col_f1, col_f2 = st.columns([1, 2])
with col_f1:
    selected_periodo_censos = st.selectbox(
        "Periodo",
        options=["Todos"] + unique_periodos_censos,
        index=1 if len(unique_periodos_censos) > 0 else 0,
        key="filter_censos"
    )

df_m = df_metrics_censos.copy()
if selected_periodo_censos != "Todos":
    df_m = df_m[df_m["periodo"] == selected_periodo_censos]

with col_f2:
    if not df_m.empty:
        kpi_generales = ["periodo", "N Clientes", "N Permite censos"]
        metrics_display(df_m[kpi_generales], show_header=False, show_divider=False, max_cols=2)

if not df_m.empty:
    kpi_generales = ["periodo", "N Clientes", "N Permite censos"]
    kpi_marcas = ["periodo",
            "N con AbInbev", "% con AbInbev",
            "N con Kross", "% con Kross",
            "N con CCU", "% con CCU",
            "N con Otras Marcas", "% con Otras Marcas"]

    kpi_acciones = ["periodo", 
            "N que Instalaron", "% que Instalaron",
            "N que Disponibilizaron", "% que Disponibilizaron", 
            "N con Comp. en Salida", "% con Comp. en Salida"]

    # --- Presencia de Marcas ---
    st.markdown("#### Presencia de Marcas")
    
    for period in df_m["periodo"].unique():
        st.markdown(f"###### Periodo: {period}")
        df_p = df_m[df_m["periodo"] == period]
        
        col1, col2, col3 = st.columns(3)
        with col1:
            with st.container(border=True):
                st.markdown("**AbInbev**")
                metrics_display(df_p[["periodo", "N con AbInbev", "% con AbInbev"]], show_header=False, show_divider=False)
        with col2:
            with st.container(border=True):
                st.markdown("**Kross**")
                metrics_display(df_p[["periodo", "N con Kross", "% con Kross"]], show_header=False, show_divider=False)
        with col3:
            with st.container(border=True):
                st.markdown("**Otras Marcas**")
                metrics_display(df_p[["periodo", "N con Otras Marcas", "% con Otras Marcas"]], show_header=False, show_divider=False)
        st.divider()
    
    st.markdown("#### Acciones en el Punto de Venta")
    for period in df_m["periodo"].unique():
        st.markdown(f"###### Periodo: {period}")
        df_p = df_m[df_m["periodo"] == period]
        
        col1, col2, col3 = st.columns(3)
        with col1:
            with st.container(border=True):
                st.markdown("**Instalaron**")
                metrics_display(df_p[["periodo", "N que Instalaron", "% que Instalaron"]], show_header=False, show_divider=False)
        with col2:
            with st.container(border=True):
                st.markdown("**Disponibilizaron**")
                metrics_display(df_p[["periodo", "N que Disponibilizaron", "% que Disponibilizaron"]], show_header=False, show_divider=False)
        with col3:
            with st.container(border=True):
                st.markdown("**Competencia en Salida**")
                metrics_display(df_p[["periodo", "N con Comp. en Salida", "% con Comp. en Salida"]], show_header=False, show_divider=False)
        st.divider()
else:
    st.info("No hay métricas de censos para el periodo seleccionado.")


# 3. Bases CCU Section
unique_periodos_bases = sorted(df_metrics_bases["periodo"].dropna().unique(), reverse=True)

st.markdown("### Contratos")

col_fb1, col_fb2 = st.columns([1, 2])
with col_fb1:
    selected_periodo_bases = st.selectbox(
        "Filtrar por Periodo (Bases CCU)",
        options=["Todos"] + unique_periodos_bases,
        index=1 if len(unique_periodos_bases) > 0 else 0,
        key="filter_bases"
    )

df_b = df_metrics_bases.copy()
if selected_periodo_bases != "Todos":
    df_b = df_b[df_b["periodo"] == selected_periodo_bases]

if not df_b.empty:
    kpi_bases = ["periodo", "N Clientes", "N Clientes Local Imagen", "N Clientes Nuevos"]
    metrics_display(df_b[kpi_bases], max_cols=6)
else:
    st.info("No hay métricas de bases CCU para el periodo seleccionado.")

