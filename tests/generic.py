from utilities.transformations.gsheet_links import add_gsheet_link

def run_basic_validations(df, name, id_col="local_id", critical_cols=None, gid=None):
    """Executes standard uniqueness and null checks with detailed views and GSheet links."""
    st.subheader(f"🔍 Checks: {name}")
    
    total_filas = len(df)
    if total_filas == 0:
        st.warning(f"La tabla {name} está vacía.")
        return

    # 1. Uniqueness
    st.markdown("### 1. Unicidad de Id de Locales")
    ids_unicos = df[id_col].nunique()
    if ids_unicos == total_filas:
        st.success(f"✅ **{id_col}**: Único ({total_filas} registros)")
    else:
        diff = total_filas - ids_unicos
        st.error(f"❌ **{id_col}**: Se detectaron {diff} duplicados")
        dupes = df[df.duplicated(id_col, keep=False)].sort_values(id_col)
        # Ensure unique columns for display (id_col might be in critical_cols)
        display_cols = [id_col] + [c for c in (critical_cols or []) if c in df.columns and c != id_col]
        
        # Add 'row_index' to display if it exists, to help debug
        if "row_index" in df.columns:
            display_cols = ["row_index"] + display_cols

        dupes_view = add_gsheet_link(dupes[display_cols], gid)
        st.dataframe(
            dupes_view, 
            use_container_width=True,
            column_config={"ir a gsheet": st.column_config.LinkColumn("ir a gsheet")}
        )

    # 2. Nulls
    if critical_cols:
        st.markdown("### 2. Integridad de Columnas Críticas (Nulos)")
        nulos = df[critical_cols].isna().sum()
        for col in critical_cols:
            val = nulos[col]
            label = col.replace("_", " ").title()
            if val == 0:
                st.write(f"✅ **{label}**: Sin nulos")
            else:
                st.write(f"⚠️ **{label}**: {val} nulos detectados")
                nulos_df = df[df[col].isna()]
                
                display_cols = [id_col, col]
                if "row_index" in df.columns:
                    display_cols = ["row_index"] + display_cols

                nulos_view = add_gsheet_link(nulos_df[display_cols], gid)
                st.dataframe(
                    nulos_view, 
                    use_container_width=True,
                    column_config={"ir a gsheet": st.column_config.LinkColumn("ir a gsheet")}
                )
