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

    # 1. local_id + periodo
    st.markdown("### 1. `local_id` + `periodo`")
    df['key'] = df['local_id'].astype(str) + "_" + df['periodo'].astype(str)
    ids_unicos = df['key'].nunique()
    
    if ids_unicos == total_filas:
        st.success(f"{ICONS['check']} Unicidad por Local y Periodo ({total_filas} registros)")
    else:
        st.error(f"{ICONS['close']} Se detectaron {total_filas - ids_unicos} registros duplicados (mismo Local y Periodo)")
        dupes = df[df.duplicated('key', keep=False)].sort_values(['local_id', 'periodo'])
        render_troubled_rows(dupes[['local_id', 'periodo', 'schoperas', 'row_index']], gid)

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
        render_troubled_rows(missing_df[['local_id', 'periodo', 'row_index']].drop_duplicates(), gid)

    # 2. schoperas
    st.markdown("### 2. `schoperas`")
    
    # Check for Nulls
    nulos = df['schoperas'].isna().sum()
    if nulos > 0:
        st.warning(f"{ICONS['warning']} {nulos} registros con 'schoperas' nulo")
        nulos_df = df[df['schoperas'].isna()]
        render_troubled_rows(nulos_df[['local_id', 'periodo', 'schoperas', 'row_index']], gid)
    else:
        st.success(f"{ICONS['check']} 'schoperas': Sin nulos")

    # Check for Negative Values
    negativos = df[df['schoperas'] < 0]
    if not negativos.empty:
        st.error(f"{ICONS['close']} Se detectaron {len(negativos)} registros con schoperas negativas")
        render_troubled_rows(negativos[['local_id', 'periodo', 'schoperas']], gid, negativos['row_index'])
    else:
        st.success(f"{ICONS['check']} No hay valores negativos en schoperas")

    # 3. salidas
    st.markdown("### 3. `salidas`")
    
    # Check for Nulls
    nulos_sal = df['salidas'].isna().sum()
    if nulos_sal > 0:
        st.warning(f"{ICONS['warning']} {nulos_sal} registros con 'salidas' nulo")
        nulos_df = df[df['salidas'].isna()]
        render_troubled_rows(nulos_df[['local_id', 'periodo', 'salidas', 'row_index']], gid)
    else:
        st.success(f"{ICONS['check']} 'salidas': Sin nulos")

    # Check for Negative Values
    negativos_sal = df[df['salidas'] < 0]
    if not negativos_sal.empty:
        st.error(f"{ICONS['close']} Se detectaron {len(negativos_sal)} registros con salidas negativas")
        render_troubled_rows(negativos_sal[['local_id', 'periodo', 'salidas', 'row_index']], gid)
    else:
        st.success(f"{ICONS['check']} No hay valores negativos en salidas")


# solo 2025
    df_2025 = df[df['periodo'] == '2025-S2']

    if df_2025.empty:
        st.warning("No hay datos para el periodo 2025-S2")
    else:
        # 4. instalo
        st.markdown("#### 4. `instalo`")
        st.info("Nota: Solo aplica a registros del periodo 2025-S2")
        
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

        # 5. disponibilizo
        st.markdown("#### 5. `disponibilizo`")
        st.info("Nota: Solo aplica a registros del periodo 2025-S2")
        
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
