import streamlit as st
import pandas as pd
from utilities.transformations.gsheet_links import add_gsheet_link
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
        st.dataframe(
            add_gsheet_link(dupes[['local_id', 'periodo']], gid, dupes['row_index']), 
            use_container_width=True,
            column_config={"link": st.column_config.LinkColumn("link", display_text="Ir a Gsheet")}
        )

    # Check Foreign Key (local_id exists in Locales)
    st.markdown("### 1.1 `local_id` en tabla de locales")
    ids_maestros = set(df_locales['local_id'].unique())
    ids_bases = set(df['local_id'].unique())
    ids_faltantes = ids_bases - ids_maestros

    if not ids_faltantes:
        st.success(f"{ICONS['check']} Todos los `local_id` existen en la tabla Locales")
    else:
        st.error(f"{ICONS['close']} Se detectaron {len(ids_faltantes)} `local_id` que NO existen en Locales")
        missing_df = df[df['local_id'].isin(ids_faltantes)]
        st.dataframe(
            add_gsheet_link(missing_df[['local_id', 'periodo']].drop_duplicates(), gid, None),
            use_container_width=True,
            column_config={"link": st.column_config.LinkColumn("link", display_text="Ir a Gsheet")}
        )

    # Check Foreign Key (local_id exists in Locales)
    st.markdown("### 1.1 `local_id` en tabla de locales")
    ids_maestros = set(df_locales['local_id'].unique())
    ids_censos = set(df['local_id'].unique())
    ids_faltantes = ids_censos - ids_maestros

    if not ids_faltantes:
        st.success(f"{ICONS['check']} Todos los `local_id` existen en la tabla Locales")
    else:
        st.error(f"{ICONS['close']} Se detectaron {len(ids_faltantes)} `local_id` que NO existen en Locales")
        missing_df = df[df['local_id'].isin(ids_faltantes)]
        st.dataframe(
            add_gsheet_link(missing_df[['local_id', 'periodo']].drop_duplicates(), gid, None),
            use_container_width=True,
            column_config={"link": st.column_config.LinkColumn("link", display_text="Ir a Gsheet")}
        )