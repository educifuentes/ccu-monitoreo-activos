import streamlit as st
import pandas as pd
from utilities.ui_components import render_troubled_rows
from utilities.ui_icons import ICONS

def validate_contratos(df):
    st.header("Contratos")
    gid = "2133854210"

    total_filas = len(df)
    if total_filas == 0:
        st.warning("La tabla Contratos está vacía.")
        return

    # 1. local_id
    st.markdown("### 1. `local_id`")
    
    # Check for Null/NaN IDs
    nulos_id = df[df['local_id'].isna()]
    if not nulos_id.empty:
        st.error(f"{ICONS['close']} Detectados {len(nulos_id)} contratos sin local_id")
        render_troubled_rows(nulos_id[['local_id', 'folio']], gid, nulos_id['row_index'])
    else:
        st.success(f"{ICONS['check']} Todos los contratos tienen local_id")

    # Check for Uniqueness
    non_null_df = df[df['local_id'].notna()]
    total_non_null = len(non_null_df)
    ids_unicos = non_null_df['local_id'].nunique()
    
    if ids_unicos == total_non_null:
        st.success(f"{ICONS['check']} Identificadores únicos ({total_non_null} registros)")
    else:
        st.error(f"{ICONS['close']} Se detectaron {total_non_null - ids_unicos} IDs duplicados")
        dupes = non_null_df[non_null_df.duplicated('local_id', keep=False)].sort_values('local_id')
        render_troubled_rows(dupes[['local_id', 'folio']], gid, dupes['row_index'])

    # 2. folio
    st.markdown("### 2. `folio`")
    nulos_folio = df[df['folio'].isna()]
    if not nulos_folio.empty:
        st.warning(f"{ICONS['warning']} Detectados {len(nulos_folio)} contratos sin Folio")
        render_troubled_rows(nulos_folio[['local_id', 'folio']], gid, nulos_folio['row_index'])
    else:
        st.success(f"{ICONS['check']} Todos los contratos tienen Folio")

    # 3. fecha_inicio
    st.markdown("### 3. `fecha_inicio`")
    nulos_inicio = df[df['fecha_inicio'].isna()]
    if not nulos_inicio.empty:
        st.warning(f"{ICONS['warning']} Detectados {len(nulos_inicio)} contratos sin Fecha de Inicio")
        render_troubled_rows(nulos_inicio[['local_id', 'fecha_inicio']], gid, nulos_inicio['row_index'])
    else:
        st.success(f"{ICONS['check']} Todas las fechas de inicio están completas")

    # 4. fecha_termino
    st.markdown("### 4. `fecha_termino`")
    nulos_termino = df[df['fecha_termino'].isna()]
    if not nulos_termino.empty:
        st.warning(f"{ICONS['warning']} Hay {len(nulos_termino)} registros sin fecha de término registrada")
        render_troubled_rows(nulos_termino[['local_id', 'fecha_termino']], gid, nulos_termino['row_index'])
    else:
        st.success(f"{ICONS['check']} Todas las fechas de término están completas")
