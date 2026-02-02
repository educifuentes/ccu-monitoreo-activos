from models.staging._stg_base_norm_censo_1 import stg_base_norm_censo_1
import pandas as pd
from utilities.transformations.process_marcas import process_marcas


def int_base_norm_censo_1():

    df = stg_base_norm_censo_1()

    # drop rows with null value on id
    initial_rows = len(df)
    df = df.dropna(subset=["id"])
    dropped_rows = initial_rows - len(df)
    print(f"Dropped {dropped_rows} rows with null id")

    # drop rows with null value on agencia column
    initial_rows = len(df)
    df = df.dropna(subset=["agencia"])
    dropped_rows = initial_rows - len(df)
    print(f"Dropped {dropped_rows} rows with null agencia")

    # Apply brand processing
    brands_col = "CCU/ABINBEV/OTRAS MARCAS COMPETENCIA"
    if brands_col in df.columns:
        df["marcas"] = df[brands_col].apply(process_marcas)

    # # rename
    rename_dict = {
        "id": "local_id",
        "CATEGORÍA CENSO 1": "categoria",
        "CANTIDAD DE SCHOPERAS CCU": "schoperas_ccu",
        "CANTIDAD DE SALIDAS": "salidas_totales",
        "CANTIDAD DE SHOPERAS COMPETENCIA ": "schoperas_competencia"
    }

    df.rename(columns=rename_dict, inplace=True)


    selected_columns = [
        "local_id",
        "salidas_totales",
        "schoperas_ccu",
        "schoperas_competencia",
        "marcas"
    ]

    # Filter columns that exist
    selected_columns = [col for col in selected_columns if col in df.columns]

    # 3. Output Information
    # print("--- DataFrame Head ---")
    # print(df.iloc[:, :5].head())

    print("\n--- List of Column Names ---")
    for i, col in enumerate(df.columns):
        print(f"{i}: {col}")

    df = df[selected_columns]
        
    return df