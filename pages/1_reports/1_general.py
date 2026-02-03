import pandas as pd
import streamlit as st
import altair as alt

from models.marts.dashboard.bi_censo_locales import bi_censo_locales

from utilities.config import CLASIFICACION_COLORS


st.title("Cumplimiento de Competencia CCU - Demo App")

st.markdown("Lectura de datos desde [Google Sheets](https://docs.google.com/spreadsheets/d/11JgW2Z9cFrHvNFw21-zlvylTHHo5tvizJeA9oxHcDHU/edit?gid=2068995815#gid=2068995815)")
st.warning("Conexion a Google Sheets Desactivada", icon="⚠️")


# load dataframe

bi_censo_locales_df = bi_censo_locales()

# -----------------------------------------------------------------------------
# FILTERS
# -----------------------------------------------------------------------------

# selected_periodo = 2025

periodos = sorted(bi_censo_locales_df['periodo'].unique(), reverse=True)
selected_periodo = st.selectbox("Seleccionar Periodo", periodos, width=200)

bi_censo_locales_df_anual = bi_censo_locales_df[bi_censo_locales_df['periodo'] == selected_periodo]


# -----------------------------------------------------------------------------
# PANEL METRICAS
# -----------------------------------------------------------------------------


# Calculate KPIs based on the clasificacion of all census records.
clasificacion_counts = bi_censo_locales_df_anual['clasificacion'].value_counts()

# en_regla = clasificacion_counts.get("En regla", 0)
# no_en_regla = clasificacion_counts.get("No en regla", 0)
# sin_comodato = clasificacion_counts.get("Sin comodato o terminado", 0)
# no_aplica = clasificacion_counts.get("No aplica", 0)

total_locales = bi_censo_locales_df['local_id'].nunique()
total_contratos_vigentes = 999

col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

with col1:
    st.metric("Locales", f"{total_locales}")
with col2:
    st.metric("Contratos Vigentes", f"{total_contratos_vigentes}")
with col3:  
    st.metric("Metrica a definir", f"{total_contratos_vigentes}")
with col4:
    st.metric("Metrica a definir", f"{total_contratos_vigentes}")




# -----------------------------------------------------------------------------
# CENSOS
# -----------------------------------------------------------------------------

st.header("Cumplimiento por Periodo - Censos")

chart = alt.Chart(bi_censo_locales_df).mark_bar().encode(
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
