import streamlit as st


from models.exposures._exp_censos_reporte_fne import exp_censos_reporte_fne

from helpers.ui_components.icons import render_icon



st.set_page_config(page_title="Reportes", layout="wide")

st.title(f"{render_icon('report')} Reportes")

st.markdown("Tabla de censos en formato de reporte para FNE")

df = exp_censos_reporte_fne()

periodos_censos = sorted(df["periodo"].dropna().unique(), reverse=True)
selected_periodo_censos = st.selectbox(
    "Filtrar por periodo",
    options=["Todos"] + list(periodos_censos),
    index=1 if len(periodos_censos) > 0 else 0,
    key="periodo_censos", width=400
)

if selected_periodo_censos != "Todos":
    df = df[df["periodo"] == selected_periodo_censos]


fne_columns = [
        "cliente_id",
        "nombre_fantasia",
        "razon_social",
        "rut",
        "comuna",
        "direccion",
        # censo meta
        "permite_censo",
        "motivo_no_censo",
        "schoperas_total",
        "schoperas_ccu",
        "schoperas_competencia",
        "salidas",
        "tiene_coolers",
        "instalo",
        "disponibilizo",
        "marcas_abinbev",
        "marcas_kross",
        "marcas_otras_listado",
        "hay_competencia_en_salida",
        "marca_competidor_en_salida",
    ]




df = df[fne_columns]

st.dataframe(df, hide_index=True, use_container_width=True)