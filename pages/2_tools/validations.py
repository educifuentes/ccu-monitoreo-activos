import streamlit as st
import pandas as pd
from models.marts._dim_locales import dim_locales
from models.marts._fct_censos import fct_censos
from models.marts._fct_bases_ccu import fct_bases_ccu
from models.marts._fct_contratos import fct_contratos_ccu

# --- Page Config & Header ---
st.set_page_config(page_title="Validaciones de Datos", layout="wide")
st.title("📊 Validaciones de Calidad de Datos")
st.markdown("Chequeos automáticos sobre las tablas maestras (Marts) para asegurar la integridad de los reportes.")

def run_basic_validations(df, name, id_col="local_id", critical_cols=None):
    """Executes standard uniqueness and null checks."""
    st.subheader(f"Checks: {name}")
    
    total_filas = len(df)
    if total_filas == 0:
        st.warning(f"La tabla {name} está vacía.")
        return

    # 1. Uniqueness
    ids_unicos = df[id_col].nunique()
    if ids_unicos == total_filas:
        st.success(f"✅ **{id_col}**: Único ({total_filas} registros)")
    else:
        diff = total_filas - ids_unicos
        st.error(f"❌ **{id_col}**: Se detectaron {diff} duplicados")

    # 2. Nulls
    if critical_cols:
        nulos = df[critical_cols].isna().sum()
        for col in critical_cols:
            val = nulos[col]
            label = col.replace("_", " ").title()
            if val == 0:
                st.write(f"✅ **{label}**: Sin nulos")
            else:
                st.write(f"⚠️ **{label}**: {val} nulos detectados")

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
    df_loc = dim_locales()
    
    col1, col2 = st.columns(2)
    with col1:
        run_basic_validations(df_loc, "Dim Locales", critical_cols=['razon_social', 'rut', 'direccion', 'region'])
    
    with col2:
        st.subheader("Búsqueda de Duplicados")
        dupes_name = df_loc[df_loc.duplicated('razon_social', keep=False)].sort_values('razon_social')
        if not dupes_name.empty:
            st.warning(f"Se encontraron {len(dupes_name)} filas con Razón Social compartida.")
            st.dataframe(dupes_name, use_container_width=True)
        else:
            st.success("No se encontraron Razones Sociales duplicadas.")

# --- Tab 2: Censos ---
with tab2:
    st.header("Validación: Fact Censos")
    df_censos = fct_censos()
    
    # Check uniqueness by local_id AND censo period if combined
    run_basic_validations(df_censos, "Fact Censos", critical_cols=['local_id', 'periodo', 'schoperas'])

# --- Tab 3: Bases CCU ---
with tab3:
    st.header("Validación: Fact Bases CCU")
    df_bases = fct_bases_ccu()
    
    # Note: Bases CCU has local_id unique per period
    run_basic_validations(df_bases, "Fact Bases CCU", critical_cols=['local_id', 'periodo'])
    
    # Check for non-numeric local_id (already cleaned in model, but good to verify)
    non_numeric = df_bases[pd.to_numeric(df_bases["local_id"], errors="coerce").isna()]
    if non_numeric.empty:
        st.success("✅ Todos los IDs son numéricos válidos.")
    else:
        st.error(f"❌ Se detectaron {len(non_numeric)} IDs no numéricos.")

# --- Tab 4: Contratos ---
with tab4:
    st.header("Validación: Fact Contratos CCU")
    df_contratos = fct_contratos_ccu()
    
    run_basic_validations(df_contratos, "Fact Contratos", id_col="local_id", critical_cols=['folio', 'fecha_inicio', 'fecha_termino'])
    
    # Check Folios
    nulos_folio = df_contratos['folio'].isna().sum()
    if nulos_folio > 0:
        st.warning(f"⚠️ Hay {nulos_folio} contratos sin Folio asignado.")
