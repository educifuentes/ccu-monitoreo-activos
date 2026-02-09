import streamlit as st
import pandas as pd
from utilities.transformations.gsheet_links import add_gsheet_link

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
        st.error(f"❌ Detectados {len(nulos_id)} locales sin ID (None o en Blanco)")
        st.dataframe(
            add_gsheet_link(nulos_id[['local_id', 'razon_social', 'fuente']], gid, nulos_id['row_index']), 
            use_container_width=True,
            column_config={"link": st.column_config.LinkColumn("link", display_text="Ir a Gsheet")}
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
            column_config={"link": st.column_config.LinkColumn("link", display_text="Ir a Gsheet")}
        )

    # Check for Uniqueness
    non_null_df = df[df['local_id'].notna()]
    total_non_null = len(non_null_df)
    ids_unicos = non_null_df['local_id'].nunique()
    
    if ids_unicos == total_non_null:
        st.success(f"✅ IDs únicos ({total_non_null} registros con ID)")
    else:
        st.error(f"❌ Se detectaron {total_non_null - ids_unicos} IDs duplicados")
        dupes = non_null_df[non_null_df.duplicated('local_id', keep=False)].sort_values('local_id')
        st.dataframe(
            add_gsheet_link(dupes[['local_id', 'razon_social']], gid, dupes['row_index']), 
            use_container_width=True,
            column_config={"link": st.column_config.LinkColumn("link", display_text="Ir a Gsheet")}
        )



    # 2. Razón Social
    st.markdown("### 2. `razon_social`")
    
    # Check for Nulls
    nulos_rs = df[df['razon_social'].isna()]
    if not nulos_rs.empty:
        st.warning(f"⚠️ Detectados {len(nulos_rs)} locales sin Razón Social")
        st.dataframe(
            add_gsheet_link(nulos_rs[['local_id', 'razon_social']], gid, nulos_rs['row_index']), 
            use_container_width=True,
            column_config={"link": st.column_config.LinkColumn("link", display_text="Ir a Gsheet")}
        )
    else:
        st.success("✅ Todos los locales tienen Razón Social")

    # Check for Duplicates
    non_null_rs = df[df['razon_social'].notna()]
    dupes_rs = non_null_rs[non_null_rs.duplicated('razon_social', keep=False)].sort_values('razon_social')
    if not dupes_rs.empty:
        st.warning(f"⚠️ Se detectaron {len(dupes_rs)} filas con Razón Social compartida")
        st.dataframe(
            add_gsheet_link(dupes_rs[['local_id', 'razon_social', 'rut', 'fuente']], gid, dupes_rs['row_index']), 
            use_container_width=True,
            column_config={"link": st.column_config.LinkColumn("link", display_text="Ir a Gsheet")}
        )
    else:
        st.success("✅ No se encontraron Razones Sociales duplicadas")

    # 3. RUT
    st.markdown("### 3. `rut`")
    nulos_rut = df[df['rut'].isna()]
    if not nulos_rut.empty:
        st.warning(f"⚠️ Detectados {len(nulos_rut)} locales sin RUT")
        st.dataframe(
            add_gsheet_link(nulos_rut[['local_id', 'razon_social', 'rut']], gid, nulos_rut['row_index']), 
            use_container_width=True,
            column_config={"ir a gsheet": st.column_config.LinkColumn("ir a gsheet")}
        )
    else:
        st.success("✅ Todos los locales tienen RUT")

    # 4. Dirección
    st.markdown("### 4. `direccion`")
    nulos_dir = df[df['direccion'].isna()]
    if not nulos_dir.empty:
        st.warning(f"⚠️ Detectados {len(nulos_dir)} locales sin Dirección")
        st.dataframe(
            add_gsheet_link(nulos_dir[['local_id', 'razon_social', 'direccion']], gid, nulos_dir['row_index']), 
            use_container_width=True,
            column_config={"ir a gsheet": st.column_config.LinkColumn("ir a gsheet")}
        )
    else:
        st.success("✅ Todos los locales tienen Dirección")

    # 5. Región
    st.markdown("### 5. `region`")
    nulos_reg = df[df['region'].isna()]
    if not nulos_reg.empty:
        st.warning(f"⚠️ Detectados {len(nulos_reg)} locales sin Región")
        st.dataframe(
            add_gsheet_link(nulos_reg[['local_id', 'razon_social', 'region']], gid, nulos_reg['row_index']), 
            use_container_width=True,
            column_config={"ir a gsheet": st.column_config.LinkColumn("ir a gsheet")}
        )
    else:
        st.success("✅ Todos los locales tienen Región")
