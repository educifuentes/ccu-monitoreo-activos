import streamlit as st
import pandas as pd
from utilities.transformations.gsheet_links import add_gsheet_link

def validate_censos(df):
    st.header("Validación: Censos")
    gid = "1636479746"
    
    total_filas = len(df)
    if total_filas == 0:
        st.warning("La tabla Censos está vacía.")
        return

    # 1. Uniqueness (local_id + periodo)
    st.markdown("### 1. Unicidad de Registros")
    df['key'] = df['local_id'].astype(str) + "_" + df['periodo'].astype(str)
    ids_unicos = df['key'].nunique()
    
    if ids_unicos == total_filas:
        st.success(f"✅ Unicidad por Local y Periodo ({total_filas} registros)")
    else:
        st.error(f"❌ Se detectaron {total_filas - ids_unicos} registros duplicados (mismo Local y Periodo)")
        dupes = df[df.duplicated('key', keep=False)].sort_values(['local_id', 'periodo'])
        st.dataframe(
            add_gsheet_link(dupes[['row_index', 'local_id', 'periodo', 'schoperas']], gid), 
            use_container_width=True,
            column_config={"ir a gsheet": st.column_config.LinkColumn("ir a gsheet")}
        )

    # 2. Integridad de Datos
    st.markdown("### 2. Integridad de Columnas Críticas")
    critical_cols = ['local_id', 'periodo', 'schoperas']
    nulos = df[critical_cols].isna().sum()
    
    for col in critical_cols:
        val = nulos[col]
        if val > 0:
            st.write(f"⚠️ **{col.title()}**: {val} nulos detectados")
            nulos_df = df[df[col].isna()]
            st.dataframe(
                add_gsheet_link(nulos_df[['row_index', 'local_id', 'periodo', col]], gid), 
                use_container_width=True,
                column_config={"ir a gsheet": st.column_config.LinkColumn("ir a gsheet")}
            )
        else:
            st.write(f"✅ **{col.title()}**: Sin nulos")

    # 3. Audits
    st.markdown("### 3. Auditoría de Valores")
    if 'schoperas' in df.columns:
        negativos = df[df['schoperas'] < 0]
        if not negativos.empty:
            st.error(f"❌ Se detectaron {len(negativos)} registros con schoperas negativas")
            st.dataframe(
                add_gsheet_link(negativos[['row_index', 'local_id', 'periodo', 'schoperas']], gid), 
                use_container_width=True,
                column_config={"ir a gsheet": st.column_config.LinkColumn("ir a gsheet")}
            )
        else:
            st.success("✅ No hay valores negativos en schoperas")
