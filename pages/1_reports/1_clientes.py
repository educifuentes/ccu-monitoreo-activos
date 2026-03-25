import pandas as pd
import streamlit as st
import altair as alt

from models.exposures._exp_clientes import exp_clientes
from models.exposures._exp_censos import exp_censos
from models.exposures._exp_activos_ccu_y_censos import exp_activos_ccu_y_censos
from models.exposures._exp_asset_evolution import exp_asset_evolution
from models.exposures._exp_contratos import exp_contratos

# marts
from models.marts.metrics.general_metrics import calculate_general_metrics, get_latest_classification

# helpers
from helpers.ui_components.ui_components import display_compliance_badge
from helpers.ui_components.icons import render_icon
from helpers.ui_components.ui_config import CLASIFICACION_COLORS, MARCAS_COLORS
from helpers.transformations.date_formatting import format_date_spanish

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
clientes_df = exp_clientes()
censos_df = exp_censos()
activos_df = exp_activos_ccu_y_censos()
contratos_df = exp_contratos()


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
contratos_cliente = contratos_df[contratos_df['cliente_id'] == selected_cliente_id]


if cliente_master.empty:
    st.error("No se encontró información maestra para este cliente.")
else:
    cliente_master = cliente_master.iloc[0]

    # Latest Classification
    latest_clasificacion = get_latest_classification(selected_cliente_id, censos_df)
    
    # Assets History
    cliente_assets_history = activos_df[activos_df['cliente_id'] == selected_cliente_id].sort_values('fecha', ascending=False)

    # 3. Cliente Card (Ficha)
    st.subheader(f"Ficha: {cliente_master['razon_social']}")
    st.caption(f"ID: {selected_cliente_id} | RUT: {cliente_master['rut']}")

    col_info, col_comp = st.columns([2, 1])

    with col_info:
        st.subheader("Información del Cliente")
        with st.container(border=True):
            st.markdown(f"📍 **Dirección:** {cliente_master['direccion']}")
            st.markdown(f"**Ciudad/Comuna:** {cliente_master['ciudad']}")
            st.markdown(f"**Región:** {cliente_master['region']}")

    with col_comp:
        st.subheader("Contrato")
        with st.container(border=True):
            contrato = contratos_cliente.iloc[0] if not contratos_cliente.empty else None
            if contrato is not None:
                icon = render_icon("check") if contrato['es_local_imagen'] else render_icon("close")
                st.markdown(f"**Local Imagen:** {icon}")
                st.markdown(f"**Suscripción Comodato:** {format_date_spanish(contrato['fecha_suscripcion_comodato'])}")
                st.markdown(f"**Término Contrato:** {format_date_spanish(contrato['fecha_termino_contrato'])}")
            else:
                st.warning("Sin datos de contrato")

    # 5. Assets Evolution
    st.subheader(":material/monitoring: Evolución de Activos")
    st.markdown("Cronología de activos (Schoperas, Salidas, Coolers) según Censos y Bases CCU.")

    asset_evolution = exp_asset_evolution()
    cliente_asset_evolution = asset_evolution[asset_evolution['cliente_id'] == selected_cliente_id]
    st.dataframe(cliente_asset_evolution, width='stretch', hide_index=True, column_config={
            "cliente_id": None,
            "fuente": st.column_config.MultiselectColumn(
                "fuente",
                options=["Censo", "CCU"],
                color=["#D97A2B", "#7FB77E"],
            )
        })


        
        # Trend Chart


    #     if len(cliente_assets_history) > 1:
    #         st.markdown("---")
    #         st.caption("Tendencia Temporal de Activos")
    #         chart_data = cliente_assets_history.melt(id_vars=['fecha'], value_vars=['schoperas_ccu', 'salidas'], var_name='Activo', value_name='Cantidad')
            
    #         line_chart = alt.Chart(chart_data).mark_line(point=True).encode(
    #             x=alt.X('fecha:T', title='Fecha'),
    #             y=alt.Y('Cantidad:Q', title='Cantidad'),
    #             color='Activo:N',
    #             tooltip=['fecha', 'Activo', 'Cantidad']
    #         ).properties(height=250)
            
    #         st.altair_chart(line_chart, width='stretch')
    # else:
    #     st.warning("No hay registros históricos de activos para este cliente.")
