import streamlit as st
import pandas as pd

from models.marts.gsheets._fct_bases_ccu_gsheets import fct_bases_ccu_gsheets
from models.marts.gsheets._dim_clientes_gsheets import dim_clientes_gsheets

from helpers.ui_components.ui_components import render_troubled_rows
from helpers.ui_components.ui_icons import ICONS
from helpers.constants.gsheets_ids import SHEETS_IDS

# -----------------------------------------------------------------------------
# DATA LOADING
# -----------------------------------------------------------------------------
df = fct_bases_ccu_gsheets()
df_locales = dim_clientes_gsheets()


def validate_bases_ccu(periodo=None):
    st.header("Bases CCU")

    _df = df[df["periodo"] == periodo] if periodo else df
    total_filas = len(_df)
    if total_filas == 0:
        st.warning("La tabla Bases CCU está vacía.")
        return

    st.markdown("## 1. Comparacion con tabla Clientes")

    st.markdown("### 1.1 `cliente_id` de Bases CCU no presente en tabla Clientes (Clientes Nuevos)")
    ids_maestros = set(df_locales["cliente_id"].unique())
    ids_bases = set(_df["cliente_id"].unique())
    ids_faltantes = ids_bases - ids_maestros

    if not ids_faltantes:
        st.success(f"{ICONS['check']} Todos los `cliente_id` existen en la tabla Clientes")
    else:
        st.error(f"{ICONS['close']} Se detectaron {len(ids_faltantes)} `cliente_id` que NO existen en Clientes")
        missing_df = _df[_df["cliente_id"].isin(ids_faltantes)]
        render_troubled_rows(missing_df[["cliente_id", "periodo", "row_index"]].drop_duplicates(), source="gsheets", gid=SHEETS_IDS["bases_ccu"])

    st.markdown("#### 1.2 `direccion` diferente entre Bases CCU y Clientes")
    if "direccion" in _df.columns and "direccion" in df_locales.columns:
        merged_df = _df.dropna(subset=["cliente_id"]).merge(
            df_locales[["cliente_id", "direccion"]], 
            on="cliente_id", 
            how="inner", 
            suffixes=("", "_maestro")
        )
        
        # Compare as strings, ignoring case and trailing whitespace
        dir_censo = merged_df["direccion"].fillna("").astype(str).str.strip().str.lower()
        dir_maestro = merged_df["direccion_maestro"].fillna("").astype(str).str.strip().str.lower()
        
        # Flag if both are not empty and they differ
        mismatched = merged_df[(dir_censo != "") & (dir_maestro != "") & (dir_censo != dir_maestro)]
        
        if mismatched.empty:
            st.success(f"{ICONS['check']} Todas las direcciones coinciden entre Bases CCU y Clientes")
        else:
            st.error(f"{ICONS['close']} Se detectaron {len(mismatched)} registros con `direccion` diferente")
            render_troubled_rows(mismatched[["cliente_id", "periodo", "direccion", "direccion_maestro", "row_index"]], source="gsheets", gid=SHEETS_IDS["bases_ccu"])
    else:
        st.warning("La columna `direccion` no existe en ambas tablas para validar.")

    st.markdown("## 2. Integridad Datos")

    st.markdown("#### 2.1 `cliente_id` + `periodo` duplicados")
    _df["key"] = _df["cliente_id"].astype(str) + "_" + _df["periodo"].astype(str)
    ids_unicos = _df["key"].nunique()

    if ids_unicos == total_filas:
        st.success(f"{ICONS['check']} Registros únicos ({total_filas} filas)")
    else:
        st.error(f"{ICONS['close']} Se detectaron {total_filas - ids_unicos} duplicados")
        dupes = _df[_df.duplicated("key", keep=False)].sort_values(["cliente_id", "periodo"])
        render_troubled_rows(dupes[["cliente_id", "periodo", "row_index"]], source="gsheets", gid=SHEETS_IDS["bases_ccu"])

    st.markdown("#### 2.2 Validez de Identificadores")
    non_numeric = _df[pd.to_numeric(_df["cliente_id"], errors="coerce").isna()]
    if non_numeric.empty:
        st.success(f"{ICONS['check']} Todos los IDs son numéricos válidos.")
    else:
        st.error(f"{ICONS['close']} Se detectaron {len(non_numeric)} IDs no numéricos.")
        render_troubled_rows(non_numeric[["cliente_id", "periodo", "row_index"]], source="gsheets", gid=SHEETS_IDS["bases_ccu"])


    st.markdown("#### 2.4 Contratos")

    nulos_id = _df[_df["cliente_id"].isna()]
    if not nulos_id.empty:
        st.error(f"{ICONS['close']} Detectados {len(nulos_id)} filas sin cliente_id")
        render_troubled_rows(nulos_id[["cliente_id", "folio", "row_index"]], source="gsheets", gid=SHEETS_IDS["bases_ccu"])
    else:
        st.success(f"{ICONS['check']} Todos los registros tienen cliente_id")

    nulos_folio = _df[_df["folio"].isna()]
    if not nulos_folio.empty:
        st.warning(f"{ICONS['warning']} Detectados {len(nulos_folio)} registros sin Folio")
        render_troubled_rows(nulos_folio[["cliente_id", "folio", "row_index"]], source="gsheets", gid=SHEETS_IDS["bases_ccu"])
    else:
        st.success(f"{ICONS['check']} Todos los registros tienen Folio")
