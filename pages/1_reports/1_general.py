import pandas as pd
import streamlit as st
import altair as alt

from models.gsheets.marts.bi_activos import bi_activos
from models.gsheets.marts.bi_locales import bi_locales
from models.gsheets.marts.bi_contratos import bi_contratos
from models.gsheets.marts.bi_censos import bi_censos

from models.raw.marts.metrics.general_metrics import calculate_general_metrics, get_latest_classification

from utilities.ui_components import display_compliance_badge
from utilities.ui_config import CLASIFICACION_COLORS, MARCAS_COLORS
from utilities.transformations.date_formatting import format_date_spanish

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Reportes General y Locales", layout="wide")
st.title("Monitoreo de Activos CCU")
st.markdown("Lectura de datos desde [Google Sheets](https://docs.google.com/spreadsheets/d/11JgW2Z9cFrHvNFw21-zlvylTHHo5tvizJeA9oxHcDHU/edit?gid=2068995815#gid=2068995815)")

# -----------------------------------------------------------------------------
# DATA LOADING
# -----------------------------------------------------------------------------
bi_activos_df = bi_activos()
bi_locales_df = bi_locales()
bi_contratos_df = bi_contratos()
bi_censos_df = bi_censos()

# -----------------------------------------------------------------------------
# FILTERS
# -----------------------------------------------------------------------------
# (Filters are currently commented out or unused, preserving structure)
# selected_periodo = 2025
# periodos = sorted(bi_activos_df['periodo'].unique(), reverse=True)
# selected_periodo = st.selectbox("Seleccionar Periodo", periodos, width=200)
# bi_censos_df = bi_censos_df[bi_censos_df['periodo'] == selected_periodo]

# -----------------------------------------------------------------------------
# METRICS PANEL
# -----------------------------------------------------------------------------
bi_censos_2025_df = bi_censos_df[bi_censos_df['periodo'] == "2025-S2"]
metrics = calculate_general_metrics(bi_activos_df, bi_censos_2025_df, bi_contratos_df, bi_locales_df)

col_metrics, col_chart = st.columns([1, 1.5])

with col_metrics:
    st.subheader("Métricas")
    m1, m2 = st.columns(2)
    m1.metric("Locales", f"{metrics['total_locales']}")
    m2.metric("Contratos Imagen", f"{metrics['total_contratos_imagen']}")
    
    m3, m4 = st.columns(2)
    m3.metric("En regla", f"{metrics['en_regla']}")
    m4.metric("No en regla", f"{metrics['no_en_regla']}")

with col_chart:
    st.subheader("Cumplimiento - Censos")
    chart = alt.Chart(bi_censos_2025_df).mark_bar().encode(
        x=alt.X('periodo:O', title='Periodo'),
        y=alt.Y('count():Q', title='Número de Locales'),
        color=alt.Color(
            'clasificacion:N',
            title='Clasificacion',
            scale=alt.Scale(
                domain=list(CLASIFICACION_COLORS.keys()),
                range=list(CLASIFICACION_COLORS.values())
            )
        ),
        tooltip=[
            alt.Tooltip('periodo:O', title='Periodo'),
            alt.Tooltip('count():Q', title='Número de Locales'),
            alt.Tooltip('clasificacion:N', title='Clasificación')
        ]
    )
    st.altair_chart(chart, use_container_width=True, height=250)


# -----------------------------------------------------------------------------
# LOCAL DETAILS SECTION
# -----------------------------------------------------------------------------
st.divider()
st.header(":material/sports_bar: Locales")
st.markdown("Información detallada de censos, nóminas y contratos por cada establecimiento.")

# 1. Selection
unique_locales_master = bi_locales_df[['local_id', 'razon_social']].drop_duplicates().sort_values('local_id')
locales_options = {
    row['local_id']: f"{row['local_id']} - {row['razon_social']}" 
    for _, row in unique_locales_master.iterrows()
}

# Initialize session state for tracking last interaction
if 'last_selectbox_value' not in st.session_state:
    st.session_state.last_selectbox_value = None
if 'last_text_input_value' not in st.session_state:
    st.session_state.last_text_input_value = ""

col_select, col_input = st.columns([2, 1])

with col_select:
    selected_local_id = st.selectbox(
        "Seleccionar Local para ver detalles", 
        options=list(locales_options.keys()), 
        format_func=lambda x: locales_options[x],
        key="local_selector"
    )

with col_input:
    text_input_id = st.text_input(
        "O ingrese ID directamente",
        placeholder="Ej: 123",
        key="local_text_input"
    )

# Determine which input to use based on what changed
selectbox_changed = st.session_state.last_selectbox_value != selected_local_id
text_input_changed = st.session_state.last_text_input_value != text_input_id

if text_input_changed and text_input_id:
    # Text input was just modified
    input_id_str = text_input_id.strip()
    if input_id_str in bi_locales_df['local_id'].astype(str).values:
        selected_local_id = input_id_str
    else:
        st.warning(f"ID '{input_id_str}' no encontrado")

# Update session state
st.session_state.last_selectbox_value = selected_local_id
st.session_state.last_text_input_value = text_input_id


# 2. Logic & Data Retrieval
local_master = bi_locales_df[bi_locales_df['local_id'] == selected_local_id]

if local_master.empty:
    st.error("No se encontró información maestra para este local.")
else:
    local_master = local_master.iloc[0]

    # Latest Classification
    latest_clasificacion = get_latest_classification(selected_local_id, bi_censos_df)
    
    # Assets History
    local_assets_history = bi_activos_df[bi_activos_df['local_id'] == selected_local_id].sort_values('fecha', ascending=False)

    # Contract Info
    has_contrato_imagen = selected_local_id in bi_contratos_df['local_id'].values
    local_contract = bi_contratos_df[bi_contratos_df['local_id'] == selected_local_id].iloc[0] if has_contrato_imagen else None

    # 3. Local Card (Ficha)
    st.subheader(f"Ficha: {local_master['razon_social']}")
    st.caption(f"ID: {selected_local_id} | RUT: {local_master['rut']}")

    col_info, col_comp = st.columns([2, 1])

    with col_info:
        with st.container(border=True):
            st.markdown(f"📍 **Dirección:** {local_master['direccion']}")
            st.markdown(f"**Ciudad/Comuna:** {local_master['ciudad']}")
            st.markdown(f"**Región:** {local_master['region']}")

    with col_comp:
        with st.container(border=True):
            st.markdown("**Cumplimiento (Censo 2025)**") 
            if latest_clasificacion != "Sin Datos":
                display_compliance_badge(latest_clasificacion)
            else:
                st.warning("No hay clasificación disponible")

    # 4. Contract Section
    st.subheader(":material/contract: Contrato Imagen")
    if has_contrato_imagen:
        st.success("✅ Tiene contrato Imagen")
        if 'folio' in local_contract and pd.notna(local_contract['folio']):
            st.markdown(f"**Folio:** {local_contract['folio']}")
    else:
        st.info("No tiene contrato Imagen")

    # 5. Assets Evolution
    st.subheader(":material/monitoring: Evolución de Activos")
    st.markdown("Cronología de activos (Schoperas, Salidas, Coolers) según Censos y Bases CCU.")

    if not local_assets_history.empty:
        # Format dates
        table_df = local_assets_history.copy()
        table_df['fecha'] = pd.to_datetime(table_df['fecha']).dt.strftime('%d/%m/%Y')
        
        # Display Table
        display_cols = ['fecha', 'periodo', 'fuente', 'schoperas', 'salidas', 'coolers']
        table_df = table_df[display_cols].rename(columns={
            'fecha': 'Fecha',
            'periodo': 'Periodo',
            'fuente': 'Fuente',
            'schoperas': 'Schoperas',
            'salidas': 'Salidas',
            'coolers': 'Coolers'
        })
        
        st.dataframe(table_df, use_container_width=True, hide_index=True, column_config={
            "Fuente": st.column_config.MultiselectColumn(
                "Fuente",
                help="Fuente de la informacion",
                options=["Censo", "CCU"],
                color=["#ffa421", "#803df5"],
            )
        })
        
        # Trend Chart
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
