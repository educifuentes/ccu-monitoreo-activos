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

st.title("Locales")
st.markdown("Informacion de censos y nominas de cada local por periodo")

# Filter selection by razon_social
names = bi_censo_locales_df['razon_social'].tolist()
selected_name = st.selectbox("Seleccionar Local", names)
local_info = bi_censo_locales_df[bi_censo_locales_df['razon_social'] == selected_name].iloc[0]
selected_local_id = local_info['local_id']

# -----------------------------------------------------------------------------

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
        st.caption(f"ID: {int(selected_local_id)} | RUT: {local_info['rut']}")
        st.markdown(f"📍 **{local_info['direccion']}**")
        st.markdown(f"{local_info['ciudad']}, {local_info['region']}")
        
    with col2:
        st.markdown("**Estado de Cumplimiento (Ultimo Censo)**")
        if latest_clasificacion != "Sin Datos":
            display_compliance_badge(latest_clasificacion)
        else:
            st.write("No hay censos registrados")

# -----------------------------------------------------------------------------
# CENSOS
# -----------------------------------------------------------------------------

st.subheader("Censos")
st.markdown("Información detallada de censos por periodo: clasificación de cumplimiento, totales de infraestructura y marcas detectadas.")

censos_filtered = censos_df[censos_df['local_id'] == selected_local_id]
display_columns = ['periodo', 'clasificacion', 'schoperas_total', 'salidas_total', 'salidas_otras', 'marcas', 'accion']
censos_filtered = censos_filtered[display_columns].sort_values('periodo', ascending=False)

st.dataframe(
    censos_filtered,
    column_config={
        "schoperas_total": st.column_config.Column("Schoperas", help="Total de schoperas instaladas"),
        "salidas_total": st.column_config.Column("Salidas", help="Total de salidas instaladas"),
        "salidas_otras": st.column_config.Column("Salidas Otras", help="Total de salidas instaladas de otras marcas"),
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


# -----------------------------------------------------------------------------
# CONTRATOS
# -----------------------------------------------------------------------------

st.warning("data demo")

st.subheader("Contrato")
local_contrato = contratos_df[contratos_df['local_id'] == selected_local_id]
if not local_contrato.empty:
    contrato_info = local_contrato.iloc[0]
    
    # Check if reported inactive by CCU
    if contrato_info.get('reportado_inactivo_ccu'):
        st.error(f"🚫 **Contrato finalizado según nominas CCU**")
        if pd.notna(contrato_info.get('motivo_termino')):
            st.markdown(f"**Motivo término:** {contrato_info['motivo_termino']}")
        if pd.notna(contrato_info.get('periodo_termino')):
            st.caption(f"Informado en periodo: {contrato_info['periodo_termino']}")
        st.divider()

    # Check if upcoming expiration
    if contrato_info['proximo_a_vencer']:
        st.badge(
            icon="⚠️", 
            label=f"Contrato próximo a vencer ({contrato_info['dias_restantes']} días)"
        )

contrato_columns = ['fecha_inicio', 'fecha_fin', 'vigente']
st.dataframe(local_contrato[contrato_columns], column_config={
        "fecha_inicio": st.column_config.DateColumn(
            "Fecha Inicio",
            help="Fecha de inicio del contrato"
        ),
        "fecha_fin": st.column_config.DateColumn(
            "Fecha Fin",
            help="Fecha de fin del contrato"    
        )
    }
)

