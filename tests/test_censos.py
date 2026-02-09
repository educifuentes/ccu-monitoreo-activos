import streamlit as st
import pandas as pd
from utilities.transformations.gsheet_links import add_gsheet_link
from utilities.ui_icons import ICONS

def validate_censos(df, df_locales):
    st.header("Censos")
    gid = "1636479746"
    
    total_filas = len(df)
    if total_filas == 0:
        st.warning("La tabla Censos está vacía.")
        return

    # 1. local_id + periodo
    st.markdown("### 1. `local_id` + `periodo`")
    df['key'] = df['local_id'].astype(str) + "_" + df['periodo'].astype(str)
    ids_unicos = df['key'].nunique()
    
    if ids_unicos == total_filas:
        st.success(f"{ICONS['check']} Unicidad por Local y Periodo ({total_filas} registros)")
    else:
        st.error(f"{ICONS['close']} Se detectaron {total_filas - ids_unicos} registros duplicados (mismo Local y Periodo)")
        dupes = df[df.duplicated('key', keep=False)].sort_values(['local_id', 'periodo'])
        st.dataframe(
            add_gsheet_link(dupes[['local_id', 'periodo', 'schoperas']], gid, dupes['row_index']), 
            use_container_width=True,
            column_config={"link": st.column_config.LinkColumn("link", display_text="Ir a Gsheet")}
        )

    # check if local_id exists in locales
    

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

    # 2. schoperas
    st.markdown("### 2. `schoperas`")
    
    # Check for Nulls
    nulos = df['schoperas'].isna().sum()
    if nulos > 0:
        st.warning(f"{ICONS['warning']} {nulos} registros con 'schoperas' nulo")
        nulos_df = df[df['schoperas'].isna()]
        st.dataframe(
            add_gsheet_link(nulos_df[['local_id', 'periodo', 'schoperas']], gid, nulos_df['row_index']), 
            use_container_width=True,
            column_config={"link": st.column_config.LinkColumn("link", display_text="Ir a Gsheet")}
        )
    else:
        st.success(f"{ICONS['check']} 'schoperas': Sin nulos")

    # Check for Negative Values
    negativos = df[df['schoperas'] < 0]
    if not negativos.empty:
        st.error(f"{ICONS['close']} Se detectaron {len(negativos)} registros con schoperas negativas")
        st.dataframe(
            add_gsheet_link(negativos[['local_id', 'periodo', 'schoperas']], gid, negativos['row_index']), 
            use_container_width=True,
            column_config={"link": st.column_config.LinkColumn("link", display_text="Ir a Gsheet")}
        )
    else:
        st.success(f"{ICONS['check']} No hay valores negativos en schoperas")
