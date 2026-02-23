import streamlit as st
import pandas as pd
from utilities.ui_components import render_troubled_rows
from utilities.ui_icons import ICONS

def validate_bases_ccu(df, df_locales):
    st.header("Bases CCU")
    gid = "524359844"
    
    total_filas = len(df)
    if total_filas == 0:
        st.warning("La tabla Bases CCU está vacía.")
        return

    # 1. local_id + periodo
    st.markdown("### 1. `local_id` + `periodo`")
    # En Bases CCU el local_id debe ser único por periodo
    df['key'] = df['local_id'].astype(str) + "_" + df['periodo'].astype(str)
    ids_unicos = df['key'].nunique()
    
    if ids_unicos == total_filas:
        st.success(f"{ICONS['check']} Registros únicos ({total_filas} filas)")
    else:
        st.error(f"{ICONS['close']} Se detectaron {total_filas - ids_unicos} duplicados")
        dupes = df[df.duplicated('key', keep=False)].sort_values(['local_id', 'periodo'])
        render_troubled_rows(dupes[['local_id', 'periodo']], gid, dupes['row_index'])

    # Check Foreign Key (local_id exists in Locales)
    st.markdown("### 1.1 local_id de Bases CCU no presente en tabla Locales")
    ids_maestros = set(df_locales['local_id'].unique())
    ids_bases = set(df['local_id'].unique())
    ids_faltantes = ids_bases - ids_maestros

    if not ids_faltantes:
        st.success(f"{ICONS['check']} Todos los `local_id` existen en la tabla Locales")
    else:
        st.error(f"{ICONS['close']} Se detectaron {len(ids_faltantes)} `local_id` que NO existen en Locales")
        missing_df = df[df['local_id'].isin(ids_faltantes)]
        render_troubled_rows(
            missing_df[['local_id', 'periodo']].drop_duplicates(), 
            gid, 
            None
        )

    # 2. Validez de Identificadores
    st.markdown("### 2. Validez de Identificadores")
    # Check for non-numeric local_id
    non_numeric = df[pd.to_numeric(df["local_id"], errors="coerce").isna()]
    if non_numeric.empty:
        st.success(f"{ICONS['check']} Todos los IDs son numéricos válidos.")
    else:
        st.error(f"{ICONS['close']} Se detectaron {len(non_numeric)} IDs no numéricos.")
        render_troubled_rows(
            non_numeric[['local_id', 'periodo']], 
            gid, 
            non_numeric['row_index'] if 'row_index' in non_numeric.columns else None
        )

    # 3. Test for base 2024
    st.markdown("### 3. Activos Vacíos en 2024-Q1")
    df_2024 = df[df["periodo"] == "2024-Q1"]
    
    # Check if 'schoperas', 'coolers', and 'salidas' are all null
    empty_activos = df_2024[
        df_2024["schoperas"].isna() & 
        df_2024["coolers"].isna() & 
        df_2024["salidas"].isna()
    ]
    
    if empty_activos.empty:
        st.success(f"{ICONS['check']} Todos los registros de 2024-Q1 tienen al menos un activo válido.")
    else:
        st.error(f"{ICONS['close']} Se detectaron {len(empty_activos)} registros en 2024-Q1 sin ningún activo reportado (schoperas, coolers, salidas).")
        cols_to_show = ["local_id", "periodo", "schoperas", "coolers", "salidas"]
        render_troubled_rows(
            empty_activos[cols_to_show], 
            gid, 
            empty_activos["row_index"] if "row_index" in empty_activos.columns else None
        )

    # test for base 2024