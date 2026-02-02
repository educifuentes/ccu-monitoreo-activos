import pandas as pd
import numpy as np

def stg_base_norm_censo_1():
    # Define file path
    file_path = "seeds/base_normalizada/base_normalizada - censo_1.csv"
    
    # Load CSV
    df = pd.read_csv(file_path)

    # # rename
    # rename_dict = {
    #     "id": "local_id",
    #     "CATEGORÍA CENSO 1": "categoria",
    #     "CANTIDAD DE SCHOPERAS CCU": "schoperas_ccu",
    #     "CANTIDAD DE SALIDAS": "salidas_totales",
    #     "CANTIDAD DE SHOPERAS COMPETENCIA ": "schoperas_competencia",
    #     "marcas": "marcas",
    # }

    # df.rename(columns=rename_dict, inplace=True)

    # selected_columns = [
    #     "local_id",
    #     "razon_social",
    #     "rut",
    #     "direccion",
    #     "region",
    #     "ciudad",
    #     "nombre_fantasia" ]

    # 3. Output Information
    # print("--- DataFrame Head ---")
    # print(df.iloc[:, :5].head())

    print("\n--- List of Column Names ---")
    for i, col in enumerate(df.columns):
        print(f"{i}: {col}")

    # df = df[selected_columns]
        
    return df