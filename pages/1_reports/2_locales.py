import streamlit as st
import pandas as pd
import altair as alt

from models.marts.dashboard.bi_censo_locales import bi_censo_locales
from models.marts.dashboard.bi_activos import bi_activos
from models.marts.gsheets.gsheets_tables import contratos, locales
from utilities.ui_components import display_compliance_badge
from utilities.config import CLASIFICACION_COLORS, MARCAS_COLORS

# --- Load Data (using cache) ---
bi_censo_locales_df = bi_censo_locales()
bi_activos_df = bi_activos()
contratos_df = contratos()
locales_df = locales()

# -----------------------------------------------------------------------------
# FILTERS & SELECTION
# -----------------------------------------------------------------------------

# We use the master locales_df to build the selection list to ensure we see all locales
# even if they don't have recent censos.
unique_locales_master = locales_df[['local_id', 'razon_social']].drop_duplicates().sort_values('local_id')
locales_options = {
    row['local_id']: f"{row['local_id']} - {row['razon_social']}" 
    for _, row in unique_locales_master.iterrows()
}

st.title("Locales")
st.markdown("Información detallada de censos, nóminas y contratos por cada establecimiento.")

selected_local_id = st.selectbox(
    "Seleccionar Local", 
    options=list(locales_options.keys()), 
    format_func=lambda x: locales_options[x]
)

# -----------------------------------------------------------------------------
# GLOBAL FILTERING
# -----------------------------------------------------------------------------

# 1. Master Info
local_master = locales_df[locales_df['local_id'] == selected_local_id]
if local_master.empty:
    st.error("No se encontró información maestra para este local.")
    st.stop()
local_master = local_master.iloc[0]

# 2. Censo BI Info (for latest classification)
local_bi_censos = bi_censo_locales_df[bi_censo_locales_df['local_id'] == selected_local_id].sort_values('periodo', ascending=False)
latest_clasificacion = local_bi_censos.iloc[0]['clasificacion'] if not local_bi_censos.empty else "Sin Datos"

# 3. Assets History (BI Activos)
local_assets_history = bi_activos_df[bi_activos_df['local_id'] == selected_local_id].sort_values('fecha', ascending=False)

# 4. Contract Info
local_contract = contratos_df[contratos_df['local_id'] == selected_local_id].iloc[0] if selected_local_id in contratos_df['local_id'].values else None

# -----------------------------------------------------------------------------
# FICHA DEL LOCAL
# -----------------------------------------------------------------------------

st.subheader(f"{local_master['razon_social']}")
st.caption(f"ID: {selected_local_id} | RUT: {local_master['rut']}")


col1, col2 = st.columns([2, 1])


with col1:
    
    
    with st.container(border=True):

        st.markdown(f"📍 **Dirección:** {local_master['direccion']}")
        st.markdown(f"**Ciudad/Comuna:** {local_master['ciudad']}")
        st.markdown(f"**Región:** {local_master['region']}")
      

with col2:
    with st.container(border=True):
        st.markdown("**Cumplimiento**")
        st.markdown(f"**Último Censo:** {local_bi_censos.iloc[0]['periodo']}")
        if latest_clasificacion != "Sin Datos":
            display_compliance_badge(latest_clasificacion)
        else:
            st.warning("No hay censos registrados")

# -----------------------------------------------------------------------------
# CONTRATO ACTUAL
# -----------------------------------------------------------------------------

st.subheader("Contrato Actual")
if local_contract is not None:
    with st.container(border=True):
        c1, c2, c3 = st.columns(3)
        c1.metric("Folio", local_contract['folio'] if pd.notna(local_contract['folio']) else "N/A")
        c2.metric("Inicio", local_contract['fecha_inicio'].strftime('%Y-%m') if pd.notna(local_contract['fecha_inicio']) else "N/A")
        c3.metric("Activos Comprometidos", f"{int(local_contract['activos_entregados'])}" if pd.notna(local_contract['activos_entregados']) else "N/A")
        
        if 'fecha_termino' in local_contract and pd.notna(local_contract['fecha_termino']):
            st.markdown(f"📅 **Término de Contrato:** {local_contract['fecha_termino'].strftime('%d/%m/%Y')}")
        
        if local_contract.get('es_local_imagen?') == True:
            st.info("✨ Este local tiene categoría **Local Imagen** según contrato.")
else:
    st.info("No se encontró información de contrato para este local")

# -----------------------------------------------------------------------------
# EVOLUCIÓN DE ACTIVOS
# -----------------------------------------------------------------------------

st.subheader("Evolución de Activos")
st.markdown("Cronología de activos (Schoperas, Salidas, Coolers) según Censos y Nóminas CCU.")

if not local_assets_history.empty:
    # Format dates for table display
    table_df = local_assets_history.copy()
    table_df['fecha'] = pd.to_datetime(table_df['fecha']).dt.strftime('%d/%m/%Y')
    
    # Select and rename columns for clarity
    display_cols = ['fecha', 'periodo', 'fuente', 'schoperas', 'salidas', 'coolers']
    table_df = table_df[display_cols].rename(columns={
        'fecha': 'Fecha',
        'periodo': 'Periodo',
        'fuente': 'Fuente',
        'schoperas': 'Schoperas',
        'salidas': 'Salidas',
        'coolers': 'Coolers'
    })
    
    st.dataframe(table_df, use_container_width=True, hide_index=True)
    
    # Mini trend chart if there is enough data
    if len(local_assets_history) > 1:
        st.markdown("---")
        st.caption("Tendencia Temporal de Activos")
        chart_data = local_assets_history.melt(id_vars=['fecha'], value_vars=['schoperas', 'salidas'], var_name='Activo', value_name='Cantidad')
        
        line_chart = alt.Chart(chart_data).mark_line(point=True).encode(
            x=alt.X('fecha:T', title='Fecha'),
            y=alt.Y('Cantidad:Q', title='Cantidad'),
            color='Activo:N',
            tooltip=['fecha', 'Activo', 'Cantidad']
        ).properties(height=250)
        
        st.altair_chart(line_chart, use_container_width=True)
else:
    st.warning("No hay registros históricos de activos para este local.")
