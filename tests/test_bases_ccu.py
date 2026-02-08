import streamlit as st
import pandas as pd
from tests.generic import run_basic_validations

def validate_bases_ccu(df):
    st.header("Validación: Bases CCU")
    
    # Note: Bases CCU has local_id unique per period
    run_basic_validations(
        df, 
        "Bases CCU", 
        critical_cols=['local_id', 'periodo'], 
        gid="524359844"
    )
    
    st.markdown("### 3. Validez de IDs")
    # Check for non-numeric local_id (already cleaned in model, but good to verify)
    non_numeric = df[pd.to_numeric(df["local_id"], errors="coerce").isna()]
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
