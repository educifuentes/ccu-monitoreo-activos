import pandas as pd

from models.intermediate._int_base_norm_locales import int_base_norm_locales
from models.intermediate._int_reportes_ccu_base_2026_q1 import int_reportes_ccu_base_2026_q1_locales

from utilities.transformations.text_cleaning import clean_text
from utilities.transformations.clean_region import clean_region


def update_with_base_ccu_2026_q1():
    """ 
    Consolidates locales by prioritizing the 2026 CCU report.
    Adds records from the normalized base that are missing in the 2026 report.
    """
    # load df
    df_norm = int_base_norm_locales()
    df_ccu = int_reportes_ccu_base_2026_q1_locales()

    # columns
    locales_columns = ["local_id", "razon_social", "rut", "direccion", "region", "ciudad", "comuna", "nombre_fantasia"]

    df_norm["comuna"] = None
    df_norm = df_norm[locales_columns]

    # Load both sources
    df_norm = df_norm[locales_columns]
    df_ccu = df_ccu[locales_columns]

    # 1. Start with CCU 2026 records
    df_ccu["fuente"] = "base_ccu_2026"
    
    # 2. Find records in base_norm that are NOT in base_ccu_2026
    missing_ids = df_norm[~df_norm["local_id"].isin(df_ccu["local_id"])].copy()
    missing_ids["fuente"] = "base_norm"
    print(f"Locales en base_norm no presentes en CCU 2026: {len(missing_ids)}")

    # 3. Concatenate (Union)
    df_final = pd.concat([df_ccu, missing_ids], ignore_index=True)

    return df_final
    

def dim_locales():
    """
    Locales con info consolidada de censos y contratos.
    """

    df = update_with_base_ccu_2026_q1()

    # 1. Standardize and clean text columns
    # clean_text now handles:
    # - Conversion to "string" dtype (modern pandas nullable strings)
    # - Stripping whitespace
    # - Title casing (propagates pd.NA correctly)
    # - Converting empty strings to pd.NA
    title_cols = ["razon_social", "direccion", "region", "ciudad", "comuna", "nombre_fantasia"]
    df = clean_text(df, title_cols, title=True)
    df = clean_text(df, ["rut"], title=False)
    
    # 2. Normalize regions using the dedicated mapper
    df = clean_region(df)

    # 3. Debugging/Monitoring (Optional but helpful in logs)
    print("\n--- DIM LOCALES MONITORING ---")
    print(f"Total records: {len(df)}")
    print("\nSource Distribution:")
    print(df["fuente"].value_counts())
    
    print("\nRegion Distribution (post-cleaning):")
    print(df["region"].value_counts(dropna=False))

    # 4. Final cleanups
    df["nombre_fantasia"] = df["nombre_fantasia"].replace("0", pd.NA)

    return df
