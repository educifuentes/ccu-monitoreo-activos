import streamlit as st
import pandas as pd
from utilities.transformations.gsheet_links import add_gsheet_link

def validate_contratos(df):
    st.header("Validación: Fact Contratos CCU")
    gid = "2133854210"

    total_filas = len(df)
    if total_filas == 0:
        st.warning("La tabla Contratos está vacía.")
        return

    # 1. Unicidad
    st.markdown("### 1. Unicidad de Identificadores")
    ids_unicos = df['local_id'].nunique()
    if ids_unicos == total_filas:
        st.success(f"✅ local_id: Único ({total_filas} registros)")
    else:
        st.error(f"❌ local_id: {total_filas - ids_unicos} duplicados")
        dupes = df[df.duplicated('local_id', keep=False)].sort_values('local_id')
        st.dataframe(
            add_gsheet_link(dupes[['local_id', 'folio']], gid, dupes['row_index']), 
            use_container_width=True,
            column_config={"ir a gsheet": st.column_config.LinkColumn("ir a gsheet")}
        )

    # 2. Integridad de Datos
    st.markdown("### 2. Integridad de Columnas Críticas")
    critical_cols = ['folio', 'fecha_inicio', 'fecha_termino']
    for col in critical_cols:
        val = df[col].isna().sum()
        if val > 0:
            st.write(f"⚠️ **{col.replace('_', ' ').title()}**: {val} nulos")
            nulos_df = df[df[col].isna()]
            st.dataframe(
                add_gsheet_link(nulos_df[['local_id', col]], gid, nulos_df['row_index']), 
                use_container_width=True,
                column_config={"ir a gsheet": st.column_config.LinkColumn("ir a gsheet")}
            )
        else:
            st.write(f"✅ **{col.replace('_', ' ').title()}**: Sin nulos")

    st.markdown("### 3. Integridad de Folios")
    # Check Folios
    nulos_folio = df[df['folio'].isna()]
    if nulos_folio.empty:
        st.success("✅ Todos los contratos tienen folio.")
    else:
        st.warning(f"⚠️ Hay {len(nulos_folio)} contratos sin Folio asignado.")
        
        st.dataframe(
            add_gsheet_link(nulos_folio[['local_id', 'folio']], gid, nulos_folio['row_index'] if 'row_index' in nulos_folio.columns else None), 
            use_container_width=True,
            column_config={"ir a gsheet": st.column_config.LinkColumn("ir a gsheet")}
        )
