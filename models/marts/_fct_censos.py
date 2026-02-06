import pandas as pd
from models.intermediate._int_censos_censo_2 import int_censos_censo_2
from models.intermediate._int_base_norm_censo_1 import int_base_norm_censo_1


def fct_censos():
    """
    Combines Censo 1 and Censo 2 data into a single fact table.
    Standardizes columns across both datasets to ensure a consistent schema.
    """
    # 1. Load intermediate models
    df_censo_1 = int_base_norm_censo_1()
    df_censo_2 = int_censos_censo_2()

    # 2. Standardize Censo 1 columns
    # Censo 1 uses 'schoperas_ccu' and 'salidas_ccu', matching Censo 2 names
    rename_dict_1 = {
        "schoperas_ccu": "schoperas",
        "salidas_ccu": "salidas"
    }
    df_censo_1 = df_censo_1.rename(columns=rename_dict_1)

    # 3. Add missing columns to Censo 1
    # These columns exist in Censo 2 but not in Censo 1
    df_censo_1["instalo"] = pd.NA
    df_censo_1["disponibilizo"] = pd.NA

    # 4. Final Column Selection
    # Define the schema for the unified fact table
    selected_columns = [
        "local_id",
        "periodo",
        "fecha",    
        "schoperas",
        "salidas",
        "instalo",
        "disponibilizo",
        "marcas",
        "marcas_abinbev",
        "marcas_kross",
        "marcas_ccu",
        "marcas_otras"
    ]

    # Ensure all selected columns are present (as NA if missing) before concat
    for df in [df_censo_1, df_censo_2]:
        for col in selected_columns:
            if col not in df.columns:
                df[col] = pd.NA

    # 5. Union and Final Processing
    union_df = pd.concat([df_censo_1[selected_columns], df_censo_2[selected_columns]], ignore_index=True)

    # Ensure numeric types for count columns
    numeric_cols = ["schoperas", "salidas", "instalo", "disponibilizo"]
    for col in numeric_cols:
        union_df[col] = pd.to_numeric(union_df[col], errors='coerce').astype("Int64")

    return union_df