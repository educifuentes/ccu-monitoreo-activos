import streamlit as st
import pandas as pd
import altair as alt

from src.data_preparation import get_generated_dataframes
from models.marts.dashboard.bi_censo_locales import bi_censo_locales

from utilities.ui_components import display_compliance_badge
from utilities.config import CLASIFICACION_COLORS, MARCAS_COLORS


# -----------------------------------------------------------------------------
# LOAD DATA
# -----------------------------------------------------------------------------
try:
    locales_df, censos_df, activos_df, nominas_df, contratos_df = get_generated_dataframes()
except FileNotFoundError as e:
    st.error(f"Error loading data file: {e}. Please make sure the files are in the 'data/raw/' directory.")
    st.stop()

bi_censo_locales_df = bi_censo_locales()



# -----------------------------------------------------------------------------
# FILTERS
# -----------------------------------------------------------------------------

# Get unique locales to avoid duplicates in the dropdown
unique_locales = bi_censo_locales_df[['local_id', 'razon_social']].drop_duplicates().sort_values('local_id')
locales_options = {row['local_id']: f"{row['local_id']} - {row['razon_social']}" for _, row in unique_locales.iterrows()}

st.title("Locales")
st.markdown("Informacion de censos y nominas de cada local por periodo")
st.markdown(f"Total de Locales: {len(unique_locales)}")


# Filter selection by local


selected_local_id = st.selectbox(
    "Seleccionar Local", 
    options=list(locales_options.keys()), 
    format_func=lambda x: locales_options[x]
)

local_info = bi_censo_locales_df[bi_censo_locales_df['local_id'] == selected_local_id].iloc[0]


# -----------------------------------------------------------------------------
# FICHA DEL LOCAL
# -----------------------------------------------------------------------------

st.subheader("Ficha del Local")

# Get most recent census clasificacion for the badge
local_censos = censos_df[censos_df['local_id'] == selected_local_id].sort_values('fecha', ascending=False)
latest_clasificacion = local_censos.iloc[0]['clasificacion'] if not local_censos.empty else "Sin Datos"

with st.container(border=True):
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"### {local_info['razon_social']}")
        st.caption(f"ID: {selected_local_id} | RUT: {local_info['rut']}")
        st.markdown(f"📍 **{local_info['direccion']}**")
        st.markdown(f"{local_info['ciudad']}, {local_info['region']}")
        
    with col2:
        st.markdown("**Estado de Cumplimiento (Ultimo Censo)**")
        if latest_clasificacion != "Sin Datos":
            display_compliance_badge(latest_clasificacion)
        else:
            st.write("No hay censos registrados")
    
    st.warning("Estado Contrato Aqui")

# -----------------------------------------------------------------------------
# CENSOS
# -----------------------------------------------------------------------------

st.subheader("Censos")
st.markdown("Información detallada de censos por periodo: clasificación de cumplimiento, totales de infraestructura y marcas detectadas.")

censos_filtered = bi_censo_locales_df[bi_censo_locales_df['local_id'] == selected_local_id]
display_columns = ['periodo', 'clasificacion', 'schoperas_ccu', 'salidas_ccu', 'salidas_competencia', 'marcas']
censos_filtered = censos_filtered[display_columns].sort_values('periodo', ascending=False)

st.dataframe(
    censos_filtered,
    column_config={
        "schoperas_ccu": st.column_config.Column("Schoperas", help="Total de schoperas instaladas"),
        "salidas_ccu": st.column_config.Column("Salidas", help="Total de salidas instaladas"),
        "salidas_competencia": st.column_config.Column("Salidas Competencia", help="Total de salidas instaladas de otras marcas"),
        "clasificacion": st.column_config.MultiselectColumn(
            "Clasificación",
            help="Estado de cumplimiento del local",
            options=list(CLASIFICACION_COLORS.keys()),
            color=list(CLASIFICACION_COLORS.values()),
        ),
        "marcas": st.column_config.MultiselectColumn(
            "Marcas Ofrecidas",
            help="Marcas detectadas en el censo",
            options=list(MARCAS_COLORS.keys()),
            color=list(MARCAS_COLORS.values()),
        ),
    },
    hide_index=True,
)


st.subheader("Comodatos")
st.warning("Evolucion de activos segun comodatos trimestrales CCU")

