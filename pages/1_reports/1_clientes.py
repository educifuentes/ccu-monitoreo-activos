import streamlit as st
import altair as alt

from models.exposures._exp_clientes import exp_clientes
from models.exposures._exp_censos import exp_censos
from models.exposures._exp_bases_ccu import exp_bases_ccu
from models.exposures._exp_activos_ccu_y_censos import exp_activos_ccu_y_censos
from models.exposures._exp_asset_evolution import exp_asset_evolution
from models.exposures._exp_contratos import exp_contratos

from models.metrics.general_metrics import get_latest_classification

from helpers.ui_components.ui_components import display_compliance_badge
from helpers.ui_components.icons import render_icon
from helpers.transformations.date_formatting import format_date_spanish
from helpers.charts.trend_assets import render_trend_assets_chart

# =============================================================================
# PAGE CONFIG
# =============================================================================
st.set_page_config(page_title="Clientes", layout="wide")
st.title(f"{render_icon('clientes')} Clientes")


# =============================================================================
# DATA LOADING  (runs once per session, cached by each exposure function)
# =============================================================================
clientes_df  = exp_clientes()
censos_df    = exp_censos()
activos_df   = exp_activos_ccu_y_censos()
asset_evolution_df = exp_asset_evolution()
contratos_df = exp_contratos()
bases_ccu_df = exp_bases_ccu()

# =============================================================================
# CLIENTE SELECTION
# =============================================================================
st.markdown("Información detallada de cada cliente a aprties de censos y reporets CCU.")

unique_clientes = (
    clientes_df[["cliente_id", "razon_social"]]
    .drop_duplicates()
    .sort_values("cliente_id")
)
clientes_options = {
    row["cliente_id"]: f"{row['cliente_id']} - {row['razon_social']}"
    for _, row in unique_clientes.iterrows()
}

# Session state: track which widget was last changed to resolve priority
if "last_selectbox_value" not in st.session_state:
    st.session_state.last_selectbox_value = None
if "last_text_input_value" not in st.session_state:
    st.session_state.last_text_input_value = ""

col_select, col_input = st.columns([2, 1])

with col_select:
    selected_cliente_id = st.selectbox(
        "Seleccionar Cliente para ver detalles",
        options=list(clientes_options.keys()),
        format_func=lambda x: clientes_options[x],
        key="local_selector",
    )

with col_input:
    text_input_id = st.text_input(
        "O ingrese ID directamente",
        placeholder="Ej: 123",
        key="local_text_input",
    )

# Text input takes priority if it was just modified
text_input_changed = st.session_state.last_text_input_value != text_input_id
if text_input_changed and text_input_id:
    input_id_str = text_input_id.strip()
    if input_id_str in clientes_df["cliente_id"].astype(str).values:
        selected_cliente_id = input_id_str
    else:
        st.warning(f"ID '{input_id_str}' no encontrado")

st.session_state.last_selectbox_value = selected_cliente_id
st.session_state.last_text_input_value = text_input_id

# =============================================================================
# FILTER DATA FOR SELECTED CLIENTE
# =============================================================================
cliente_master_df   = clientes_df[clientes_df["cliente_id"] == selected_cliente_id]
contratos_cliente   = contratos_df[contratos_df["cliente_id"] == selected_cliente_id]
activos_cliente     = activos_df[activos_df["cliente_id"] == selected_cliente_id].sort_values("fecha", ascending=False)
asset_evo_cliente   = asset_evolution_df[asset_evolution_df["cliente_id"] == selected_cliente_id]

# =============================================================================
# CLIENTE DETAIL VIEW
# =============================================================================
if cliente_master_df.empty:
    st.error("No se encontró información maestra para este cliente.")
else:
    cliente = cliente_master_df.iloc[0]
    latest_clasificacion = get_latest_classification(selected_cliente_id, censos_df)

    # ── Header ────────────────────────────────────────────────────────────────
    st.subheader(f"Ficha: {cliente['razon_social']}")
    st.caption(f"ID: {selected_cliente_id} | RUT: {cliente['rut']} | Nombre Fantasia: {cliente['nombre_fantasia']}")

    # ── Info + Contrato columns ───────────────────────────────────────────────
    col_info, col_comp = st.columns([2, 1])

    with col_info:
        st.subheader("Información")
        with st.container(border=True):
            st.markdown(f"📍 **Dirección:** {cliente['direccion']}")
            st.markdown(f"**Ciudad/Comuna:** {cliente['ciudad']}")
            st.markdown(f"**Región:** {cliente['region']}")

    with col_comp:
        st.subheader("Contrato")
        with st.container(border=True):
            contrato = contratos_cliente.iloc[0] if not contratos_cliente.empty else None
            if contrato is not None:
                icon = render_icon("check") if contrato["es_local_imagen"] else render_icon("close")
                st.markdown(f"**Local Imagen:** {icon}")
                st.markdown(f"**Suscripción Comodato:** {format_date_spanish(contrato['fecha_suscripcion_comodato'])}")
                st.markdown(f"**Término Contrato:** {format_date_spanish(contrato['fecha_termino_contrato'])}")
            else:
                st.warning("Sin datos de contrato")

    # ── Assets Evolution table ────────────────────────────────────────────────
    st.subheader(":material/monitoring: Evolución de Activos - Censos + Bases CCU")

    st.dataframe(
        asset_evo_cliente,
        use_container_width=True,
        hide_index=True,
        column_config={
            "cliente_id": None,
            "fuente": st.column_config.MultiselectColumn(
                "fuente",
                options=["Censo", "CCU"],
                color=["#D97A2B", "#7FB77E"],
            ),
        },
    )

    # ── Trend Chart ───────────────────────────────────────────────────────────
    render_trend_assets_chart(activos_cliente)

    st.divider()

    # ── Historial de Censos ───────────────────────────────────────────────────
    st.subheader("Historial de Censos")
    censo_cols = ["periodo", "fecha", "schoperas_total", "schoperas_ccu", "salidas", "marcas"]
    df_c = censos_df[censos_df["cliente_id"] == selected_cliente_id]
    st.dataframe(df_c[censo_cols], hide_index=True, use_container_width=True)

    # ── Historial de Activos (Base CCU) ───────────────────────────────────────
    st.subheader("Historial en Bases CCU")
    ccu_cols = ["periodo", "fecha", "schoperas_ccu", "salidas", "coolers", "es_local_imagen"]
    df_b = bases_ccu_df[bases_ccu_df["cliente_id"] == selected_cliente_id]
    st.dataframe(df_b[ccu_cols], hide_index=True, use_container_width=True)
