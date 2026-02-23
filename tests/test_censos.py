import streamlit as st
import pandas as pd
from utilities.ui_components import render_troubled_rows
from utilities.ui_icons import ICONS

def validate_censos(df, df_locales):
    st.header("Censos")
    gid = "1636479746"
    
    total_filas = len(df)
    if total_filas == 0:
        st.warning("La tabla Censos está vacía.")
        return

    # 1. Generales
    st.markdown("### 1. Generales")
    
    # 1.1 Uniqueness
    st.markdown("#### 1.1 Unicidad (`local_id` + `periodo`)")
    df['key'] = df['local_id'].astype(str) + "_" + df['periodo'].astype(str)
    ids_unicos = df['key'].nunique()
    
    if ids_unicos == total_filas:
        st.success(f"{ICONS['check']} Unicidad por Local y Periodo ({total_filas} registros)")
    else:
        st.error(f"{ICONS['close']} Se detectaron {total_filas - ids_unicos} registros duplicados (mismo Local y Periodo)")
        dupes = df[df.duplicated('key', keep=False)].sort_values(['local_id', 'periodo'])
        render_troubled_rows(dupes[['local_id', 'periodo', 'schoperas', 'row_index']], gid)

    # 1.2 Check Foreign Key (local_id exists in Locales)
    st.markdown("#### 1.2 Integridad Referencial (`local_id` en Locales)")
    ids_maestros = set(df_locales['local_id'].unique())
    ids_censos = set(df['local_id'].unique())
    ids_faltantes = ids_censos - ids_maestros

    if not ids_faltantes:
        st.success(f"{ICONS['check']} Todos los `local_id` existen en la tabla Locales")
    else:
        st.error(f"{ICONS['close']} Se detectaron {len(ids_faltantes)} `local_id` que NO existen en Locales")
        missing_df = df[df['local_id'].isin(ids_faltantes)]
        render_troubled_rows(missing_df[['local_id', 'periodo', 'row_index']].drop_duplicates(), gid)

    # 2.1 Check for Negative Values
    st.markdown("#### 2.1 Valores negativos en `salidas`")
    negativos_sal = df[df['salidas'] < 0]
    if not negativos_sal.empty:
        st.error(f"{ICONS['close']} Se detectaron {len(negativos_sal)} registros con salidas negativas")
        render_troubled_rows(negativos_sal[['local_id', 'periodo', 'salidas', 'row_index']], gid)
    else:
        st.success(f"{ICONS['check']} No hay valores negativos en salidas")


    # 3. Censo 2 (2025-S2) Validations
    st.markdown("### 3. Validaciones - Censo 2 - 2025-S2")
    df_2025 = df[df['periodo'] == '2025-S2']

    if df_2025.empty:
        st.warning("No hay datos para el periodo 2025-S2")
    else:
        # 3.1 instalo
        st.markdown("#### 3.1 Nulos y negativos en `instalo`")
        
        # Check for Nulls
        nulos_ins = df_2025['instalo'].isna().sum()
        if nulos_ins > 0:
            st.warning(f"{ICONS['warning']} {nulos_ins} registros con 'instalo' nulo")
            nulos_df = df_2025[df_2025['instalo'].isna()]
            render_troubled_rows(nulos_df[['local_id', 'periodo', 'instalo', 'row_index']], gid)
        else:
            st.success(f"{ICONS['check']} 'instalo': Sin nulos")

        # Check for Negative Values
        negativos_ins = df_2025[df_2025['instalo'] < 0]
        if not negativos_ins.empty:
            st.error(f"{ICONS['close']} Se detectaron {len(negativos_ins)} registros con instalo negativos")
            render_troubled_rows(negativos_ins[['local_id', 'periodo', 'instalo', 'row_index']], gid)
        else:
            st.success(f"{ICONS['check']} No hay valores negativos en instalo")

        # 3.2 disponibilizo
        st.markdown("#### 3.2 Nulos y negativos en `disponibilizo`")
        
        # Check for Nulls
        nulos_disp = df_2025['disponibilizo'].isna().sum()
        if nulos_disp > 0:
            st.warning(f"{ICONS['warning']} {nulos_disp} registros con 'disponibilizo' nulo")
            nulos_df = df_2025[df_2025['disponibilizo'].isna()]
            render_troubled_rows(nulos_df[['local_id', 'periodo', 'disponibilizo', 'row_index']], gid)
        else:
            st.success(f"{ICONS['check']} 'disponibilizo': Sin nulos")

        # Check for Negative Values
        negativos_disp = df_2025[df_2025['disponibilizo'] < 0]
        if not negativos_disp.empty:
            st.error(f"{ICONS['close']} Se detectaron {len(negativos_disp)} registros con disponibilizo negativos")
            render_troubled_rows(negativos_disp[['local_id', 'periodo', 'disponibilizo', 'row_index']], gid)
        else:
            st.success(f"{ICONS['check']} No hay valores negativos en disponibilizo")
