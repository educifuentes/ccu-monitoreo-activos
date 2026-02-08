import streamlit as st
import pandas as pd
from utilities.transformations.gsheet_links import add_gsheet_link

def validate_bases_ccu(df):
    st.header("Validación: Bases CCU")
    gid = "524359844"
    
    total_filas = len(df)
    if total_filas == 0:
        st.warning("La tabla Bases CCU está vacía.")
        return

    # 1. Unicidad
    st.markdown("### 1. Unicidad (Local y Periodo)")
    # En Bases CCU el local_id debe ser único por periodo
    df['key'] = df['local_id'].astype(str) + "_" + df['periodo'].astype(str)
    ids_unicos = df['key'].nunique()
    
    if ids_unicos == total_filas:
        st.success(f"✅ Registros únicos ({total_filas} filas)")
    else:
        st.error(f"❌ Se detectaron {total_filas - ids_unicos} duplicados")
        dupes = df[df.duplicated('key', keep=False)].sort_values(['local_id', 'periodo'])
        st.dataframe(
            add_gsheet_link(dupes[['row_index', 'local_id', 'periodo']], gid), 
            use_container_width=True,
            column_config={"ir a gsheet": st.column_config.LinkColumn("ir a gsheet")}
        )

    # 2. Integridad de Columnas Críticas
    st.markdown("### 2. Integridad de Columnas Críticas")
    critical_cols = ['local_id', 'periodo']
    for col in critical_cols:
        val = df[col].isna().sum()
        if val > 0:
            st.write(f"⚠️ **{col.title()}**: {val} nulos")
            nulos_df = df[df[col].isna()]
            st.dataframe(
                add_gsheet_link(nulos_df[['row_index', col]], gid), 
                use_container_width=True,
                column_config={"ir a gsheet": st.column_config.LinkColumn("ir a gsheet")}
            )
        else:
            st.write(f"✅ **{col.title()}**: Sin nulos")

    st.markdown("### 3. Validez de Identificadores")
    # Check for non-numeric local_id (already cleaned in model, but good to verify)
    non_numeric = df[pd.to_numeric(df["local_id"], errors="coerce").isna()]
    if non_numeric.empty:
        st.success("✅ Todos los IDs son numéricos válidos.")
    else:
        st.error(f"❌ Se detectaron {len(non_numeric)} IDs no numéricos.")
        
        st.dataframe(
            add_gsheet_link(non_numeric[['local_id', 'periodo']], gid), 
            use_container_width=True,
            column_config={"ir a gsheet": st.column_config.LinkColumn("ir a gsheet")}
        )
