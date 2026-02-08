import streamlit as st
import pandas as pd
from utilities.transformations.gsheet_links import add_gsheet_link

def validate_locales(df):
    st.header("Locales")
    gid = "2068995815"
    critical_cols = ['razon_social', 'rut', 'direccion', 'region']
    
    total_filas = len(df)
    if total_filas == 0:
        st.warning("La tabla Dim Locales está vacía.")
        return

    # 1. IDs Quality
    st.markdown("### 1. `local_id`")
    
    # Check for Null/NaN IDs
    nulos_id = df[df['local_id'].isna()]

    if not nulos_id.empty:
        st.error(f"❌ Detectados {len(nulos_id)} locales sin ID (None o en Blanco)")
        st.dataframe(
            add_gsheet_link(nulos_id[['local_id', 'razon_social']], gid, nulos_id['row_index']), 
            use_container_width=True,
            column_config={"ir a gsheet": st.column_config.LinkColumn("ir a gsheet")}
        )
    else:
        st.success("✅ Todos los locales tienen ID")

    # Check for Numeric IDs
    non_numeric = df[pd.to_numeric(df["local_id"], errors="coerce").isna() & df["local_id"].notna()]
    if not non_numeric.empty:
        st.error(f"❌ Detectados {len(non_numeric)} IDs que no se pueden convertir a número")
        st.dataframe(
            add_gsheet_link(non_numeric[['local_id', 'razon_social']], gid, non_numeric['row_index'] if 'row_index' in non_numeric.columns else None), 
            use_container_width=True,
            column_config={"ir a gsheet": st.column_config.LinkColumn("ir a gsheet")}
        )

    # Check for Uniqueness
    ids_unicos = df['local_id'].nunique()
    if ids_unicos == total_filas:
        st.success(f"✅ IDs únicos ({total_filas} registros)")
    else:
        st.error(f"❌ Se detectaron {total_filas - ids_unicos} IDs duplicados")
        dupes = df[df.duplicated('local_id', keep=False)].sort_values('local_id')
        st.dataframe(
            add_gsheet_link(dupes[['local_id', 'razon_social']], gid, dupes['row_index']), 
            use_container_width=True,
            column_config={"ir a gsheet": st.column_config.LinkColumn("ir a gsheet")}
        )




    # 2. Integridad de Columnas Críticas
    st.markdown("### 2. Integridad de Columnas Críticas")
    nulos = df[critical_cols].isna().sum()
    for col in critical_cols:
        val = nulos[col]
        label = col.replace("_", " ").title()
        if val == 0:
            st.write(f"✅ **{label}**: Sin nulos")
        else:
            st.write(f"⚠️ **{label}**: {val} nulos detectados")
            nulos_df = df[df[col].isna()]
            display_cols = ['row_index', 'local_id', col]
            st.dataframe(
                add_gsheet_link(nulos_df[['local_id', col]], gid, nulos_df['row_index']), 
                use_container_width=True,
                column_config={"ir a gsheet": st.column_config.LinkColumn("ir a gsheet")}
            )

    st.markdown("### 3. Duplicados por Razón Social")
    dupes_name = df[df.duplicated('razon_social', keep=False)].sort_values('razon_social')
    if not dupes_name.empty:
        st.warning(f"Se encontraron {len(dupes_name)} filas con Razón Social compartida.")
        
        # Add gsheet link for manual check
        link = "https://docs.google.com/spreadsheets/d/11JgW2Z9cFrHvNFw21-zlvylTHHo5tvizJeA9oxHcDHU/edit#gid=2068995815"
        dupes_name_view = dupes_name[['local_id', 'razon_social', 'rut']].copy()
        dupes_name_view["ir a gsheet"] = link
        
        st.dataframe(
            dupes_name_view, 
            use_container_width=True,
            column_config={"ir a gsheet": st.column_config.LinkColumn("ir a gsheet")}
        )
    else:
        st.success("✅ No se encontraron Razones Sociales duplicadas.")
