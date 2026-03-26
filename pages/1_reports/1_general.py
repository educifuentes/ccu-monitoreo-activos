import pandas as pd
import streamlit as st

from models.exposures._exp_clientes import exp_clientes
from models.exposures._exp_censos import exp_censos

from models.exposures._exp_censos import exp_censos
from models.exposures._exp_asset_evolution_censos import exp_asset_evolution_censos
from models.exposures.metrics._metric_censo_kpis_by_period import metrics_censo_kpis_by_period
from models.exposures.metrics._metric_bases_ccu_kpis_by_period import metrics_bases_ccu_kpis_by_period
from helpers.ui_components.metrics_display import metrics_display

from helpers.ui_components.ui_config import CLASIFICACION_COLORS
from helpers.widgets.explorer_de_datos import explorer_de_datos
from helpers.widgets.display_df_censos import display_df_censos


# marts
from models.marts.metrics.general_metrics import calculate_general_metrics, get_latest_classification

# helpers
from helpers.ui_components.ui_components import display_compliance_badge
from helpers.ui_components.ui_config import CLASIFICACION_COLORS, MARCAS_COLORS
from helpers.transformations.date_formatting import format_date_spanish


st.set_page_config(page_title="Reportes General y Clientes", layout="wide")
st.title("General")
st.markdown("Lectura de datos desde csv. Luego ira a [Google Sheets](https://docs.google.com/spreadsheets/d/11JgW2Z9cFrHvNFw21-zlvylTHHo5tvizJeA9oxHcDHU/edit?gid=2068995815#gid=2068995815)")



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
st.subheader("Metricas - Censos")

# Metrics
df_metrics = metrics_censo_kpis_by_period()
if selected_periodo != "Todos":
    df_metrics = df_metrics[df_metrics["periodo"] == selected_periodo]

kpi_marcas = ["periodo", "# Clientes",
        "# con AbInbev",
        "% con AbInbev",
        "# con Kross",
        "% con Kross",
        "# con CCU",
        "% con CCU",
        "# con Otras Marcas",
        "% con Otras Marcas"]

kpi_acciones = ["periodo", "# con Comp. en Salida",
        "% con Comp. en Salida",
        "# que Instalaron",
        "% que Instalaron",
        "# que Disponibilizaron",
        "% que Disponibilizaron"]

# metrics_display(df_metrics[kpi_marcas])
# metrics_display(df_metrics[kpi_acciones])

st.dataframe(df_metrics[kpi_marcas], hide_index=True)
st.dataframe(df_metrics[kpi_acciones], hide_index=True)

# Metricas - Bases CCU
st.subheader("Metricas - Bases CCU")

df_metrics_bases = metrics_bases_ccu_kpis_by_period()

unique_periodos_bases = sorted(df_metrics_bases["periodo"].dropna().unique(), reverse=True)
periodos_opciones_bases = ["Todos"] + list(unique_periodos_bases)
selected_periodo_bases = st.selectbox(
    "Filtrar por Periodo (Bases CCU)",
    options=periodos_opciones_bases,
    index=1 if len(unique_periodos_bases) > 0 else 0
)

if selected_periodo_bases != "Todos":
    df_metrics_bases = df_metrics_bases[df_metrics_bases["periodo"] == selected_periodo_bases]

kpi_bases = ["periodo", "# Clientes", "# Clientes Local Imagen", "# Clientes Nuevos"]

metrics_display(df_metrics_bases[kpi_bases])

