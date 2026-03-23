import pandas as pd
import streamlit as st
import altair as alt

from models.exposures._exp_activos import exp_activos
from models.exposures._exp_clientes import exp_clientes
from models.exposures._exp_contratos import exp_contratos
from models.exposures._exp_censos import exp_censos

from models.marts.metrics.general_metrics import calculate_general_metrics, get_latest_classification

from utilities.ui_components import display_compliance_badge
from utilities.ui_config import CLASIFICACION_COLORS, MARCAS_COLORS
from utilities.transformations.date_formatting import format_date_spanish

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Reportes General y Clientes", layout="wide")
st.title("Monitoreo de Activos CCU")
st.markdown("Lectura de datos desde csv. Luego ira a [Google Sheets](https://docs.google.com/spreadsheets/d/11JgW2Z9cFrHvNFw21-zlvylTHHo5tvizJeA9oxHcDHU/edit?gid=2068995815#gid=2068995815)")
st.markdown(" ")
# -----------------------------------------------------------------------------
# DATA LOADING
# -----------------------------------------------------------------------------
activos_df = exp_activos()
clientes_df = exp_clientes()
contratos_df = exp_contratos()
censos_df = exp_censos()


# -----------------------------------------------------------------------------
# PANEL METRICAS 
# -----------------------------------------------------------------------------
censos_2025_df = censos_df[censos_df['periodo'] == "2025-S2"]
metrics = calculate_general_metrics(activos_df, censos_2025_df, contratos_df, clientes_df)

m1, m2, m3, m4 = st.columns(4)
m1.metric("Clientes", f"{metrics['total_clientes']}")
m2.metric("Contratos Imagen", f"{metrics['total_contratos_imagen']}")
m3.metric("En regla", f"{metrics['en_regla']}")
m4.metric("No en regla", f"{metrics['no_en_regla']}")



# -----------------------------------------------------------------------------
# LOCAL DETAILS SECTION
# -----------------------------------------------------------------------------

st.header(":material/sports_bar: Clientes")
st.markdown("Información detallada de censos, nóminas y contratos por cada establecimiento.")

# 1. Selection
unique_clientes_master = clientes_df[['cliente_id', 'razon_social']].drop_duplicates().sort_values('cliente_id')
clientes_options = {
    row['cliente_id']: f"{row['cliente_id']} - {row['razon_social']}" 
    for _, row in unique_clientes_master.iterrows()
}

# Initialize session state for tracking last interaction
if 'last_selectbox_value' not in st.session_state:
    st.session_state.last_selectbox_value = None
if 'last_text_input_value' not in st.session_state:
    st.session_state.last_text_input_value = ""

col_select, col_input = st.columns([2, 1])

with col_select:
    selected_cliente_id = st.selectbox(
        "Seleccionar Cliente para ver detalles", 
        options=list(clientes_options.keys()), 
        format_func=lambda x: clientes_options[x],
        key="local_selector"
    )

with col_input:
    text_input_id = st.text_input(
        "O ingrese ID directamente",
        placeholder="Ej: 123",
        key="local_text_input"
    )

# Determine which input to use based on what changed
selectbox_changed = st.session_state.last_selectbox_value != selected_cliente_id
text_input_changed = st.session_state.last_text_input_value != text_input_id

if text_input_changed and text_input_id:
    # Text input was just modified
    input_id_str = text_input_id.strip()
    if input_id_str in clientes_df['cliente_id'].astype(str).values:
        selected_cliente_id = input_id_str
    else:
        st.warning(f"ID '{input_id_str}' no encontrado")

# Update session state
st.session_state.last_selectbox_value = selected_cliente_id
st.session_state.last_text_input_value = text_input_id


# 2. Logic & Data Retrieval
cliente_master = clientes_df[clientes_df['cliente_id'] == selected_cliente_id]

if cliente_master.empty:
    st.error("No se encontró información maestra para este cliente.")
else:
    cliente_master = cliente_master.iloc[0]

    # Latest Classification
    latest_clasificacion = get_latest_classification(selected_cliente_id, censos_df)
    
    # Assets History
    cliente_assets_history = activos_df[activos_df['cliente_id'] == selected_cliente_id].sort_values('fecha', ascending=False)

    # Contract Info
    has_contrato_imagen = selected_cliente_id in contratos_df['cliente_id'].values
    cliente_contract = contratos_df[contratos_df['cliente_id'] == selected_cliente_id].iloc[0] if has_contrato_imagen else None

    # 3. Cliente Card (Ficha)
    st.subheader(f"Ficha: {cliente_master['razon_social']}")
    st.caption(f"ID: {selected_cliente_id} | RUT: {cliente_master['rut']}")

    col_info, col_comp = st.columns([2, 1])

    with col_info:
        with st.container(border=True):
            st.markdown(f"📍 **Dirección:** {cliente_master['direccion']}")
            st.markdown(f"**Ciudad/Comuna:** {cliente_master['ciudad']}")
            st.markdown(f"**Región:** {cliente_master['region']}")

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
        if 'folio' in cliente_contract and pd.notna(cliente_contract['folio']):
            st.markdown(f"**Folio:** {cliente_contract['folio']}")
    else:
        st.info("No tiene contrato Imagen")

    # 5. Assets Evolution
    st.subheader(":material/monitoring: Evolución de Activos")
    st.markdown("Cronología de activos (Schoperas, Salidas, Coolers) según Censos y Bases CCU.")

    if not cliente_assets_history.empty:
        # Format dates
        table_df = cliente_assets_history.copy()
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
        
        st.dataframe(table_df, width='stretch', hide_index=True, column_config={
            "Fuente": st.column_config.MultiselectColumn(
                "Fuente",
                help="Fuente de la informacion",
                options=["Censo", "CCU"],
                color=["#ffa421", "#803df5"],
            )
        })
        
        # Trend Chart
        if len(cliente_assets_history) > 1:
            st.markdown("---")
            st.caption("Tendencia Temporal de Activos")
            chart_data = cliente_assets_history.melt(id_vars=['fecha'], value_vars=['schoperas', 'salidas'], var_name='Activo', value_name='Cantidad')
            
            line_chart = alt.Chart(chart_data).mark_line(point=True).encode(
                x=alt.X('fecha:T', title='Fecha'),
                y=alt.Y('Cantidad:Q', title='Cantidad'),
                color='Activo:N',
                tooltip=['fecha', 'Activo', 'Cantidad']
            ).properties(height=250)
            
            st.altair_chart(line_chart, width='stretch')
    else:
        st.warning("No hay registros históricos de activos para este cliente.")
