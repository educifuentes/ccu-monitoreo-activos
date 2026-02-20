import pandas as pd

from models.raw.intermediate._int_reportes_ccu_base_2024_q1 import int_reportes_ccu_base_2024_q1
from models.raw.intermediate._int_reportes_ccu_base_2026_q1 import int_reportes_ccu_base_2026_q1


def fct_bases_ccu():
    int_reportes_ccu_base_2024_q1_df = int_reportes_ccu_base_2024_q1()
    int_reportes_ccu_base_2026_q1_df = int_reportes_ccu_base_2026_q1()

    select_columns_base_2026 = [
        "local_id",
        "periodo",
        "fecha",
        "schoperas",
        "salidas",
        "coolers"
    ]



    int_reportes_ccu_base_2026_q1_df = int_reportes_ccu_base_2026_q1_df[select_columns_base_2026]

    df = pd.concat([int_reportes_ccu_base_2024_q1_df, int_reportes_ccu_base_2026_q1_df], ignore_index=True)   

    df.sort_values(by=["local_id", "periodo"], ascending=[True, True], inplace=True)

    # Find the local_ids that are in both dataframes
    ids_2024 = set(int_reportes_ccu_base_2024_q1_df["local_id"].unique())
    ids_2026 = set(int_reportes_ccu_base_2026_q1_df["local_id"].unique())
    common_ids = ids_2024.intersection(ids_2026)
    
    # Add a flag for rows that belong to a local_id present in both periods
    df["en_ambos_periodos"] = df["local_id"].isin(common_ids)

    # drop rows where local_id is missing or not numeric
    initial_rows = len(df)
    df.dropna(subset=["local_id"], inplace=True)
    df = df[pd.to_numeric(df["local_id"], errors="coerce").notna()].copy()
    final_rows = len(df)
    
    print(f"--- FCT BASES CCU CLEANING ---")
    print(f"Filas iniciales: {initial_rows}")
    print(f"Filas eliminadas (ID nulo o no numérico): {initial_rows - final_rows}")
    print(f"Filas finales: {final_rows}")

    return df