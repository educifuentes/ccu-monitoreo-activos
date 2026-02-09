import pandas as pd
import streamlit as st
import altair as alt

from models.marts.dashboard.bi_activos import bi_activos
from models.marts.dashboard.bi_locales import bi_locales
from models.marts.dashboard.bi_contratos import bi_contratos
from models.marts.dashboard.bi_censos import bi_censos

from utilities.ui_components import display_compliance_badge
from utilities.ui_config import CLASIFICACION_COLORS, MARCAS_COLORS
from utilities.transformations.date_formatting import format_date_spanish
from models.marts.metrics.general_metrics import calculate_general_metrics

st.set_page_config(page_title="Reportes General y Locales", layout="wide")

st.title("Monitoreo de Activos CCU")

st.markdown("Lectura de datos desde [Google Sheets](https://docs.google.com/spreadsheets/d/11JgW2Z9cFrHvNFw21-zlvylTHHo5tvizJeA9oxHcDHU/edit?gid=2068995815#gid=2068995815)")

# --- Load Data (using cache) ---
bi_activos_df = bi_activos()
bi_locales_df = bi_locales()
bi_contratos_df = bi_contratos()
bi_censos_df = bi_censos()

# -----------------------------------------------------------------------------
# FILTERS
# -----------------------------------------------------------------------------

# selected_periodo = 2025

# periodos = sorted(bi_activos_df['periodo'].unique(), reverse=True)
# selected_periodo = st.selectbox("Seleccionar Periodo", periodos, width=200)

# bi_censos_df = bi_censos_df[bi_censos_df['periodo'] == selected_periodo]


# -----------------------------------------------------------------------------
# PANEL METRICAS
# -----------------------------------------------------------------------------

bi_censos_2025_df = bi_censos_df[bi_censos_df['periodo'] == "2025-S2"]

# Calculate KPIs using the metrics module
metrics = calculate_general_metrics(bi_activos_df, bi_censos_2025_df, bi_contratos_df, bi_locales_df)

col_metrics, col_chart = st.columns([1, 1.5])

with col_metrics:
    st.subheader("Métricas")
    m1, m2 = st.columns(2)
    m1.metric("Locales", f"{metrics['total_locales']}")
    m2.metric("Contratos Vigentes", f"{metrics['total_contratos_vigentes']}")
    
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
# SECCIÓN LOCALES (Detalle por Establecimiento)
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

selected_local_id = st.selectbox(
    "Seleccionar Local para ver detalles", 
    options=list(locales_options.keys()), 
    format_func=lambda x: locales_options[x],
    key="local_selector"
)

# 2. Global Filtering for selection
# Master Info
local_master = bi_locales_df[bi_locales_df['local_id'] == selected_local_id]
if local_master.empty:
    st.error("No se encontró información maestra para este local.")
else:
    local_master = local_master.iloc[0]

    # Censo BI Info (for latest classification)
    local_bi_censos = bi_activos_df[bi_activos_df['local_id'] == selected_local_id].sort_values('periodo', ascending=False)

    

    latest_clasificacion = "no"

    # latest_clasificacion = local_bi_censos.iloc[0]['clasificacion'] if not local_bi_censos.empty else "Sin Datos"

    # Assets History (BI Activos)
    local_assets_history = bi_activos_df[bi_activos_df['local_id'] == selected_local_id].sort_values('fecha', ascending=False)

    # Contract Info
    local_contract = bi_contratos_df[bi_contratos_df['local_id'] == selected_local_id].iloc[0] if selected_local_id in bi_contratos_df['local_id'].values else None

    # 3. FICHA DEL LOCAL
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
            st.markdown("**Cumplimiento**")
            if not local_bi_censos.empty:
                st.markdown(f"**Último Censo:** {local_bi_censos.iloc[0]['periodo']}")
                if latest_clasificacion != "no":
                    display_compliance_badge(latest_clasificacion)
            else:
                st.warning("No hay censos registrados")

# -----------------------------------------------------------------------------
# CONTRATO ACTUAL
# -----------------------------------------------------------------------------

    st.subheader(":material/contract: Contrato")
    if local_contract is not None:
        with st.container(border=True):
            c1, c2, c3 = st.columns(3)
            c1.metric("Folio", local_contract['folio'] if pd.notna(local_contract['folio']) else "N/A")
            
            inicio_str = format_date_spanish(local_contract['fecha_inicio']) if 'fecha_inicio' in local_contract else "N/A"
            termino_str = format_date_spanish(local_contract['fecha_termino']) if 'fecha_termino' in local_contract else "N/A"
            periodo_str = f"{inicio_str} - {termino_str}" if inicio_str != "N/A" or termino_str != "N/A" else "N/A"
            
            c2.metric("Periodo contrato", periodo_str)
            c3.metric("Activos Comprometidos", f"{int(local_contract['activos_entregados'])}" if pd.notna(local_contract['activos_entregados']) else "N/A")
            
            if local_contract.get('es_local_imagen?') == True:
                st.info("✨ Este local tiene categoría **Local Imagen** según contrato.")
    else:
        st.info("No se encontró información de contrato para este local")

    # 5. EVOLUCIÓN DE ACTIVOS
    st.subheader(":material/monitoring: Evolución de Activos")
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
        
        st.dataframe(table_df, use_container_width=True, hide_index=True, column_config={
            "Fuente": st.column_config.MultiselectColumn(
                "Fuente",
                help="Fuente de la informacion",
                options=[
                    "Censo",
                    "CCU"
                ],
                color=["#ffa421", "#803df5"],
            )
        })
        
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
