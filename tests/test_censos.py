import streamlit as st
from tests.generic import run_basic_validations

def validate_censos(df):
    st.header("Validación: Censos")
    
    # Check uniqueness by local_id AND censo period if combined
    run_basic_validations(
        df, 
        "Censos", 
        critical_cols=['local_id', 'periodo', 'schoperas'], 
        gid="1636479746"
    )
