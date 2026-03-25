import streamlit as st
import pandas as pd

from models.exposures._exp_contratos import exp_contratos

from helpers.ui_components.ui_components import render_troubled_rows
from helpers.ui_components.ui_icons import ICONS

# -----------------------------------------------------------------------------
# DATA LOADING
# -----------------------------------------------------------------------------
df = exp_contratos()


def validate_contratos():
    st.header("Contratos")

    total_filas = len(df)
    if total_filas == 0:
        st.warning("La tabla Contratos está vacía.")
        return

    # 1. cliente_id
    st.markdown("### 1. `cliente_id`")

    nulos_id = df[df["cliente_id"].isna()]
    if not nulos_id.empty:
        st.error(f"{ICONS['close']} Detectados {len(nulos_id)} contratos sin cliente_id")
        render_troubled_rows(nulos_id[["cliente_id", "folio"]])
    else:
        st.success(f"{ICONS['check']} Todos los contratos tienen cliente_id")

    non_null_df = df[df["cliente_id"].notna()]
    total_non_null = len(non_null_df)
    ids_unicos = non_null_df["cliente_id"].nunique()

    if ids_unicos == total_non_null:
        st.success(f"{ICONS['check']} Identificadores únicos ({total_non_null} registros)")
    else:
        st.error(f"{ICONS['close']} Se detectaron {total_non_null - ids_unicos} IDs duplicados")
        dupes = non_null_df[non_null_df.duplicated("cliente_id", keep=False)].sort_values("cliente_id")
        render_troubled_rows(dupes[["cliente_id", "folio"]])

    # 2. folio
    st.markdown("### 2. `folio`")
    nulos_folio = df[df["folio"].isna()]
    if not nulos_folio.empty:
        st.warning(f"{ICONS['warning']} Detectados {len(nulos_folio)} contratos sin Folio")
        render_troubled_rows(nulos_folio[["cliente_id", "folio"]])
    else:
        st.success(f"{ICONS['check']} Todos los contratos tienen Folio")