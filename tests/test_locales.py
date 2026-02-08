import streamlit as st
from tests.generic import run_basic_validations

def validate_locales(df):
    st.header("Validación: Dim Locales")
    
    run_basic_validations(
        df, 
        "Dim Locales", 
        critical_cols=['razon_social', 'rut', 'direccion', 'region'], 
        gid="2068995815"
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
