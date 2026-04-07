import streamlit as st
import pandas as pd

from models.marts.gsheets._fct_censos_gsheets import fct_censos_gsheets
from models.marts.gsheets._dim_clientes_gsheets import dim_clientes_gsheets

from helpers.ui_components.ui_components import render_troubled_rows
from helpers.ui_components.ui_icons import ICONS
from helpers.constants.gsheets_ids import SHEETS_IDS

# -----------------------------------------------------------------------------
# DATA LOADING
# -----------------------------------------------------------------------------
df = fct_censos_gsheets()
df_clientes = dim_clientes_gsheets()


def validate_censos(periodo=None):
    st.header("Censos")

    _df = df[df["periodo"] == periodo] if periodo else df
    total_filas = len(_df)
    if total_filas == 0:
        st.warning("La tabla Censos está vacía.")
        return

    # 1. Generales
    st.markdown("### 1. Generales")

    # 1.1 Uniqueness
    st.markdown("#### 1.1 `cliente_id` + `periodo` duplicados")
    _df["key"] = _df["cliente_id"].astype(str) + "_" + _df["periodo"].astype(str)
    ids_unicos = _df["key"].nunique()

    if ids_unicos == total_filas:
        st.success(f"{ICONS['check']} Unicidad por Cliente y Periodo ({total_filas} registros)")
    else:
        st.error(f"{ICONS['close']} Se detectaron {total_filas - ids_unicos} registros duplicados (mismo Cliente y Periodo)")
        dupes = _df[_df.duplicated("key", keep=False)].sort_values(["cliente_id", "periodo"])
        render_troubled_rows(dupes[["cliente_id", "periodo", "schoperas_ccu", "row_index"]], source="gsheets", gid=SHEETS_IDS["censos"])

    # 1.2 Check Foreign Key (cliente_id exists in Clientes)
    st.markdown("#### 1.2 `cliente_id` de censos no presente en tabla Clientes (Clientes Nuevos)")
    ids_maestros = set(df_clientes["cliente_id"].unique())
    ids_censos = set(_df["cliente_id"].unique())
    ids_faltantes = ids_censos - ids_maestros

    if not ids_faltantes:
        st.success(f"{ICONS['check']} Todos los `cliente_id` existen en la tabla Clientes")
    else:
        st.error(f"{ICONS['close']} Se detectaron {len(ids_faltantes)} `cliente_id` que NO existen en Clientes (Clientes Nuevos)")
        missing_df = _df[_df["cliente_id"].isin(ids_faltantes)]
        render_troubled_rows(missing_df[["cliente_id", "periodo", "row_index"]].drop_duplicates(), source="gsheets", gid=SHEETS_IDS["censos"])

    # 2. Activos y Acciones
    st.markdown("### 2. Activos y Acciones")

    cols_to_check = ["salidas", "schoperas_total", "schoperas_ccu", "instalo", "disponibilizo"]
    
    for idx, col in enumerate(cols_to_check, start=1):
        if col in _df.columns:
            st.markdown(f"#### 2.{idx} Valores negativos en `{col}`")
            negativos = _df[_df[col] < 0]
            if not negativos.empty:
                st.error(f"{ICONS['close']} Se detectaron {len(negativos)} registros con {col} negativos")
                render_troubled_rows(negativos[["cliente_id", "periodo", col, "row_index"]], source="gsheets", gid=SHEETS_IDS["censos"])
            else:
                st.success(f"{ICONS['check']} No hay valores negativos en {col}")

