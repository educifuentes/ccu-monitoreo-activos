import pandas as pd
import streamlit as st
import plotly.express as px
import altair as alt
from src.data_preparation import get_generated_dataframes
from utils.config import CLASIFICACION_COLORS

st.title("Cumplimiento de Competencia CCU - Demo App")

st.markdown("Lectura de datos desde [Google Sheets](https://docs.google.com/spreadsheets/d/11JgW2Z9cFrHvNFw21-zlvylTHHo5tvizJeA9oxHcDHU/edit?gid=2068995815#gid=2068995815)")


# -----------------------------------------------------------------------------
# FILTERS
# -----------------------------------------------------------------------------

selected_periodo = 2025

# periodos = sorted(censos_df['periodo'].unique(), reverse=True)
# selected_periodo = st.selectbox("Seleccionar Periodo", periodos, width=200)

censos_df_anual = censos_df[censos_df['periodo'] == selected_periodo]




# -----------------------------------------------------------------------------
# PANEL METRICAS
# -----------------------------------------------------------------------------


# Calculate KPIs based on the clasificacion of all census records.
clasificacion_counts = censos_df_anual['clasificacion'].value_counts()

en_regla = clasificacion_counts.get("En regla", 0)
no_en_regla = clasificacion_counts.get("No en regla", 0)
sin_comodato = clasificacion_counts.get("Sin comodato o terminado", 0)
no_aplica = clasificacion_counts.get("No aplica", 0)
total_locales = censos_df['local_id'].nunique()
total_contratos_vigentes = contratos_df[contratos_df['vigente'] == True]['local_id'].nunique()

col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

with col1:
    st.metric("Locales", f"{total_locales}")
with col2:
    st.metric("Contratos Vigentes", f"{total_contratos_vigentes}")
with col3:  
    st.metric("Metrica a definir", f"{sin_comodato}")
with col4:
    st.metric("Metrica a definir", f"{no_aplica}")




# -----------------------------------------------------------------------------
# CENSOS
# -----------------------------------------------------------------------------

st.header("Cumplimiento por Periodo - Censos")
chart = alt.Chart(censos_df).mark_bar().encode(
    x=alt.X('periodo:O', title='Periodo'),
    y=alt.Y('count():Q', title='Número de Locales'),
    color=alt.Color(
        'clasificacion:N',
        title='Clasificacion',
        scale=alt.Scale(
            domain=list(CLASIFICACION_COLORS.keys()),
            range=list(CLASIFICACION_COLORS.values())
        )
    )
)

st.altair_chart(chart, width='stretch', height=200)

# -----------------------------------------------------------------------------
# ACTIVOS - DISTRIBUCION POR TRAMO
# -----------------------------------------------------------------------------

st.header("Distribución por Tramo de Salidas - Nominas")

# Prepare tramo data
activos_plot_df = activos_df.copy()

# Filter by selected year (periodo of selectbox)
# activos_plot_df = activos_plot_df[activos_plot_df['fecha'].dt.year == int(selected_periodo)]

# Filter for active venues only if needed
activos_plot_df = activos_plot_df[activos_plot_df['estado'] == 'activo']

def define_tramo(val):
    if pd.isna(val): return None
    return "≤ 3 salidas" if val <= 3 else "≥ 4 salidas"

activos_plot_df['salidas_tramo'] = activos_plot_df['salidas_totales'].apply(define_tramo)

# Create the stacked bar chart
# Order periods chronologically for the X-axis
period_order = sorted(activos_plot_df['periodo'].unique())

tramo_chart = alt.Chart(activos_plot_df).mark_bar().encode(
    x=alt.X('periodo:O', title='Periodo', sort=period_order),
    y=alt.Y('count():Q', title='Número de Locales'),
    color=alt.Color(
        'salidas_tramo:N',
        title='Tramo de Salidas',
        scale=alt.Scale(
            domain=["≤ 3 salidas", "≥ 4 salidas"],
            range=["#CBDCEB", "#83c9ff"] # Grayish for small, CCU blue for large
        )
    ),
    tooltip=['periodo', 'salidas_tramo', 'count()']
).properties(height=300)

st.altair_chart(tramo_chart, width='stretch')

st.subheader("Features posibles")
st.markdown("- Estado de contrato por trimestre segun info de nominas.")
st.markdown("- Cuantos locales tomarcon accion cumplimiento?")
st.markdown("- Cuantos locales no cumplen con el contrato? cual es la brecha de cumplimiento promedio?")
st.markdown("- Filtros: comuuna, trimestre, etc..")
st.markdown("- Tablas con formato customizado con boton de descarga")
st.markdown("-  agregr URL del contrato drive u a otros doucmentos drive")
