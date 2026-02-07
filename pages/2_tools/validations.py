import streamlit as st
import pandas as pd

from models.marts.gsheets.gsheets_tables import (
    locales, 
    censos, 
    bases_ccu, 
    contratos
)

# --- Page Config & Header ---
st.set_page_config(page_title="Validaciones", layout="wide")
st.title(":material/fact_check: Validaciones de Calidad de Datos")
st.markdown("Chequeos automáticos sobre las tablas maestras (Marts) para asegurar la integridad de los reportes.")

def run_basic_validations(df, name, id_col="local_id", critical_cols=None, gid=None):
    """Executes standard uniqueness and null checks with detailed views and GSheet links."""
    st.subheader(f"🔍 Checks: {name}")
    
    total_filas = len(df)
    if total_filas == 0:
        st.warning(f"La tabla {name} está vacía.")
        return

    # Helper to add gsheet column
    def add_gsheet_link(data_df):
        if gid:
            data_df = data_df.copy()
            data_df["ir a gsheet"] = f"https://docs.google.com/spreadsheets/d/11JgW2Z9cFrHvNFw21-zlvylTHHo5tvizJeA9oxHcDHU/edit#gid={gid}"
            return data_df
        return data_df

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
        dupes_view = add_gsheet_link(dupes[display_cols])
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
                nulos_view = add_gsheet_link(nulos_df[[id_col, col]])
                st.dataframe(
                    nulos_view, 
                    use_container_width=True,
                    column_config={"ir a gsheet": st.column_config.LinkColumn("ir a gsheet")}
                )


# --- Tab Layout ---
tab1, tab2, tab3, tab4 = st.tabs([
    ":material/sports_bar: Locales",
    ":material/checklist_rtl: Censos",
    ":material/assignment: Bases CCU",
    ":material/contract: Contratos"
])

# --- Tab 1: Locales ---
with tab1:
    st.header("Validación: Dim Locales")
    df_loc = locales()
    
    run_basic_validations(df_loc, "Dim Locales", critical_cols=['razon_social', 'rut', 'direccion', 'region'], gid="2068995815")
    
    st.markdown("### 3. Duplicados por Razón Social")
    dupes_name = df_loc[df_loc.duplicated('razon_social', keep=False)].sort_values('razon_social')
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


# --- Tab 2: Censos ---
with tab2:
    st.header("Validación: Censos")
    df_censos = censos()
    
    # Check uniqueness by local_id AND censo period if combined
    run_basic_validations(df_censos, "Censos", critical_cols=['local_id', 'periodo', 'schoperas'], gid="1636479746")

# --- Tab 3: Bases CCU ---
with tab3:
    st.header("Validación: Bases CCU")
    df_bases = bases_ccu()
    
    # Note: Bases CCU has local_id unique per period
    run_basic_validations(df_bases, "Bases CCU", critical_cols=['local_id', 'periodo'], gid="524359844")
    
    st.markdown("### 3. Validez de IDs")
    # Check for non-numeric local_id (already cleaned in model, but good to verify)
    non_numeric = df_bases[pd.to_numeric(df_bases["local_id"], errors="coerce").isna()]
    if non_numeric.empty:
        st.success("✅ Todos los IDs son numéricos válidos.")
    else:
        st.error(f"❌ Se detectaron {len(non_numeric)} IDs no numéricos.")
        
        # Add gsheet link
        link = "https://docs.google.com/spreadsheets/d/11JgW2Z9cFrHvNFw21-zlvylTHHo5tvizJeA9oxHcDHU/edit#gid=524359844"
        non_numeric_view = non_numeric[['local_id', 'periodo']].copy()
        non_numeric_view["ir a gsheet"] = link
        
        st.dataframe(
            non_numeric_view, 
            use_container_width=True,
            column_config={"ir a gsheet": st.column_config.LinkColumn("ir a gsheet")}
        )


# --- Tab 4: Contratos ---
with tab4:
    st.header("Validación: Fact Contratos CCU")
    df_contratos = contratos()
    
    run_basic_validations(df_contratos, "Fact Contratos", id_col="local_id", critical_cols=['folio', 'fecha_inicio', 'fecha_termino'], gid="2133854210")
    
    st.markdown("### 3. Integridad de Folios")
    # Check Folios
    nulos_folio = df_contratos[df_contratos['folio'].isna()]
    if nulos_folio.empty:
        st.success("✅ Todos los contratos tienen folio.")
    else:
        st.warning(f"⚠️ Hay {len(nulos_folio)} contratos sin Folio asignado.")
        
        # Add gsheet link
        link = "https://docs.google.com/spreadsheets/d/11JgW2Z9cFrHvNFw21-zlvylTHHo5tvizJeA9oxHcDHU/edit#gid=2133854210"
        nulos_folio_view = nulos_folio[['local_id', 'folio']].copy()
        nulos_folio_view["ir a gsheet"] = link
        
        st.dataframe(
            nulos_folio_view, 
            use_container_width=True,
            column_config={"ir a gsheet": st.column_config.LinkColumn("ir a gsheet")}
        )

