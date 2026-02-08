import streamlit as st
import pandas as pd
from .utils import run_basic_validations

def validate_contratos(df):
    st.header("Validación: Fact Contratos CCU")
    
    run_basic_validations(
        df, 
        "Fact Contratos", 
        id_col="local_id", 
        critical_cols=['folio', 'fecha_inicio', 'fecha_termino'], 
        gid="2133854210"
    )
    
    st.markdown("### 3. Integridad de Folios")
    # Check Folios
    nulos_folio = df[df['folio'].isna()]
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
