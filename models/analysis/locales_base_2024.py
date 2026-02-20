import pandas as pd
from models.raw.staging.base_normalizada._stg_base_norm_original import stg_base_norm_original
from models.raw.intermediate._int_reportes_ccu_base_2024_q1 import int_reportes_ccu_base_2024_q1

def analyze_empty_2024_locales():
    """
    Analyzes which locales from the 2024-Q1 CCU Base have no active assets
    (schoperas, coolers, salidas are all null) and checks if those specific
    local_ids exist in the original shared base (stg_base_norm_original).
    """

    # Load dataframes
    df_2024 = int_reportes_ccu_base_2024_q1()
    df_norm_orig = stg_base_norm_original()

    # 1. Identify "empty" 2024 locales
    # Condition: schoperas, coolers, and salidas are all pd.NA/null
    empty_activos_2024 = df_2024[
        df_2024["schoperas"].isna() & 
        df_2024["coolers"].isna() & 
        df_2024["salidas"].isna()
    ].copy()
    
    empty_2024_ids = set(empty_activos_2024["local_id"].unique())
    norm_orig_ids = set(df_norm_orig["ID CLIENTE"].astype(str).unique())
    
    # 2. Match IDs
    matched_ids = empty_2024_ids.intersection(norm_orig_ids)
    missing_ids = empty_2024_ids - norm_orig_ids
    
    # 3. Create resulting dataframes for the UI
    df_matched = empty_activos_2024[empty_activos_2024["local_id"].isin(matched_ids)]
    df_missing = empty_activos_2024[empty_activos_2024["local_id"].isin(missing_ids)]
    
    return {
        "total_empty_2024": len(empty_2024_ids),
        "total_matched_in_base": len(matched_ids),
        "total_missing_in_base": len(missing_ids),
        "df_matched": df_matched,
        "df_missing": df_missing
    }
