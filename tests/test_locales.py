import streamlit as st
import pandas as pd
from utilities.ui_components import render_troubled_rows
from utilities.ui_icons import ICONS

def validate_locales(df):
    st.header("Locales")
    gid = "2068995815"
    
    total_filas = len(df)
    if total_filas == 0:
        st.warning("La tabla Dim Locales está vacía.")
        return

    # 1. Column local_id
    st.markdown("### 1. `local_id`")
    
    # Check for Null/NaN IDs
    nulos_id = df[df['local_id'].isna()]

    if not nulos_id.empty:
        st.error(f"{ICONS['close']} Detectados {len(nulos_id)} locales sin ID (None o en Blanco)")
        render_troubled_rows(nulos_id[['local_id', 'razon_social', 'fuente']], gid, nulos_id['row_index'])
    else:
        st.success(f"{ICONS['check']} Todos los locales tienen ID")

    # Check for Numeric IDs
    non_numeric = df[pd.to_numeric(df["local_id"], errors="coerce").isna() & df["local_id"].notna()]
    if not non_numeric.empty:
        st.error(f"{ICONS['close']} Detectados {len(non_numeric)} IDs que no se pueden convertir a número")
        render_troubled_rows(
            non_numeric[['local_id', 'razon_social']], 
            gid, 
            non_numeric['row_index'] if 'row_index' in non_numeric.columns else None
        )

    # Check for Uniqueness
    non_null_df = df[df['local_id'].notna()]
    total_non_null = len(non_null_df)
    ids_unicos = non_null_df['local_id'].nunique()
    
    if ids_unicos == total_non_null:
        st.success(f"{ICONS['check']} IDs únicos ({total_non_null} registros con ID)")
    else:
        st.error(f"{ICONS['close']} Se detectaron {total_non_null - ids_unicos} IDs duplicados")
        dupes = non_null_df[non_null_df.duplicated('local_id', keep=False)].sort_values('local_id')
        render_troubled_rows(dupes[['local_id', 'razon_social']], gid, dupes['row_index'])

    # 2. Razón Social
    st.markdown("### 2. `razon_social`")
    
    # Check for Nulls
    nulos_rs = df[df['razon_social'].isna()]
    if not nulos_rs.empty:
        st.warning(f"{ICONS['warning']} Detectados {len(nulos_rs)} locales sin Razón Social")
        render_troubled_rows(nulos_rs[['local_id', 'razon_social']], gid, nulos_rs['row_index'])
    else:
        st.success(f"{ICONS['check']} Todos los locales tienen Razón Social")

    # Check for Duplicates
    non_null_rs = df[df['razon_social'].notna()]
    dupes_rs = non_null_rs[non_null_rs.duplicated('razon_social', keep=False)].sort_values('razon_social')
    if not dupes_rs.empty:
        st.warning(f"{ICONS['warning']} Se detectaron {len(dupes_rs)} filas con Razón Social compartida")
        render_troubled_rows(dupes_rs[['local_id', 'razon_social', 'rut', 'fuente']], gid, dupes_rs['row_index'])
    else:
        st.success(f"{ICONS['check']} No se encontraron Razones Sociales duplicadas")

    # 3. RUT
    st.markdown("### 3. `rut`")
    nulos_rut = df[df['rut'].isna()]
    if not nulos_rut.empty:
        st.warning(f"{ICONS['warning']} Detectados {len(nulos_rut)} locales sin RUT")
        render_troubled_rows(nulos_rut[['local_id', 'razon_social', 'rut']], gid, nulos_rut['row_index'])
    else:
        st.success(f"{ICONS['check']} Todos los locales tienen RUT")

    # 4. Dirección
    st.markdown("### 4. `direccion`")
    nulos_dir = df[df['direccion'].isna()]
    if not nulos_dir.empty:
        st.warning(f"{ICONS['warning']} Detectados {len(nulos_dir)} locales sin Dirección")
        render_troubled_rows(nulos_dir[['local_id', 'razon_social', 'direccion']], gid, nulos_dir['row_index'])
    else:
        st.success(f"{ICONS['check']} Todos los locales tienen Dirección")

    # 5. Región
    st.markdown("### 5. `region`")
    nulos_reg = df[df['region'].isna()]
    if not nulos_reg.empty:
        st.warning(f"{ICONS['warning']} Detectados {len(nulos_reg)} locales sin Región")
        render_troubled_rows(nulos_reg[['local_id', 'razon_social', 'region']], gid, nulos_reg['row_index'])
    else:
        st.success(f"{ICONS['check']} Todos los locales tienen Región")

    # 6. ciudad
    st.markdown("### 6. `ciudad`")
    nulos_ciudad = df[df['ciudad'].isna()]
    if not nulos_ciudad.empty:
        st.warning(f"{ICONS['warning']} Detectados {len(nulos_ciudad)} locales sin Ciudad")
        render_troubled_rows(nulos_ciudad[['local_id', 'razon_social', 'ciudad']], gid, nulos_ciudad['row_index'])
    else:
        st.success(f"{ICONS['check']} Todos los locales tienen Ciudad")
    
