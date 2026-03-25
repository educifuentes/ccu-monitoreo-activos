import pandas as pd
import streamlit as st

from models.exposures._exp_clientes import exp_clientes
from models.exposures._exp_censos import exp_censos


# marts
from models.marts.metrics.general_metrics import calculate_general_metrics, get_latest_classification

# helpers
from helpers.ui_components.ui_components import display_compliance_badge
from helpers.ui_components.ui_config import CLASIFICACION_COLORS, MARCAS_COLORS
from helpers.transformations.date_formatting import format_date_spanish


st.set_page_config(page_title="Reportes General y Clientes", layout="wide")
st.title("General")
st.markdown("Lectura de datos desde csv. Luego ira a [Google Sheets](https://docs.google.com/spreadsheets/d/11JgW2Z9cFrHvNFw21-zlvylTHHo5tvizJeA9oxHcDHU/edit?gid=2068995815#gid=2068995815)")


# -----------------------------------------------------------------------------
# PANEL METRICAS 
# -----------------------------------------------------------------------------
# censos_2025_df = censos_df[censos_df['periodo'] == "2025-S2"]
# metrics = calculate_general_metrics(activos_df, censos_2025_df, clientes_df)

# m1.metric("Clientes", f"{metrics['total_clientes']}")
# m2.metric("En regla", f"{metrics['en_regla']}")
# m3.metric("No en regla", f"{metrics['no_en_regla']}")



# nuevos clientes